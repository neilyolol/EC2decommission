#!/usr/bin/env python
# Verion 0.1
# Author: Chao
# Created @20150317
#Only support virgina and oregon
import boto.ec2, boto.ec2.elb
import sys, time, argparse, ConfigParser, requests, getpass, base64
from fabric.api import run, env, sudo, execute, local


def get_region(instance_name):
    region_head = instance_name.split('-')[0]  #instance name always be ecX-xxxx-0X
    if region_head == 'ec1':
        region = 'us-east-1'
    elif region_head == 'ec2':
        region = 'us-west-2'
    return region


def get_elb_with_instanceid(elbconn, instance_id):
    all_elb = elbconn.get_all_load_balancers()  #get all elb
    lb = []
    for each_lb in all_elb:
        under_instances = each_lb.instances  #retun like [InstanceInfo:i-dd0b74d4, InstanceInfo:i-f96f18f0]
        for each_instance in under_instances:
            if each_instance.id == instance_id:
                lb.append(each_lb)
    return lb


def chk_elb_health(elb):
    heathy_count = 0
    instance_states = elb.get_instance_health()  #return like [InstanceState:(i-dd0b74d4,InService), InstanceState:(i-f96f18f0,InService)]
    for each in instance_states:
        if each.state == 'InService':
            heathy_count += 1
    return heathy_count


def deregister_instance_from_elb(elb, instance_id):
    '''
    remove instance from ELB
    :param elb:
    :param instance_id:
    :return:
    '''
    elb.deregister_instance(instance_id)


def create_base64_string():
    script_user = getpass.getuser()
    password = raw_input("Please enter your password")
    string_before = script_user + ':' + password
    string_after = base64.encode(string_before)
    full_base_string = string_after + '=='
    return full_base_string


def remove_instance_from_dns(instance_name):


def query_question(question, defalut='yes'):
    valid = {'yes': True, 'y': True, 'no': False, 'n': False}
    if defalut == None:
        prompt == ' [y/n] '
    elif defalut == 'yes':
        prompt == ' [Y/n] '
    elif defalut == 'no':
        prompt == ' [y/N] '
    else:
        raise ValueError("Invalid default answer: '%s'" % defalut)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if defalut is not None and choice == '':
            return vaild[defalut]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please repond with 'yes'/'y' or 'no'/'n'.\n")


def irc_mark(nickname, message):
    url = '''http://telenav-irc.telenav.com:8081/IRC_Requests/?nick=''' + nickname + '''&msg=''' + message
    r = requests.get(url)

@hosts(decom)
def get_tomcat_user():
    tomcat_user = run("ps -ef|grep java|grep -v `whoami`|awk '{print $1}'")
    return list(set(java_user.split('\r\n')))  #like tnuser

@hosts(decom)
def tomcat_home():
    command = '''ps -fC java --noheaders|awk '{for (i=1;i<=NF;i++) { if ( $i ~ /Dcatalina.home/ ) {split($i,x,"="); print x[2]}}}' '''
    return run(command).splitlines()  #like /usr/local/apache-tomcat-6.0.20

@hosts(decom)
def home_log_dir(user):
    path = "/home/" + user + "/"
    command = "find " + path + " \( -type d -o -type l \) \( -name '*log*' -a ! -name '*login*' \) -print 2>/dev/null"
    return sudo(command, user=user).splitlines()

@hosts(decom)
def shutdown_tomcat():
    tomcat_user = get_tomcat_user()
    for each_user in tomcat_user:
        tomcat_home = tomcat_home()
        for each_tomcat_home in tomcat_home:
            cmd = '''ps aux|grep '%s'|grep -v grep|awk '{print $2}' ''' % each_tomcat_home
            jid = run(cmd, each_user)
            cmd = 'kill -9 %s' % jid
            run(cmd, each_user)

@hosts(decom)
def tar_log_file():
    users = get_tomcat_user()
    for user in users:
        cmd = 'cd /home/%s' % user
        run(cmd)
        home_log_paths = home_log_dir(user)
        if len(home_log_paths)>=1:
            tar_cmd = ''' tar -zcvf /home/%s/%s-logs.tar.gz ''' % (user,time.strftime('%Y-%m-%d'))
            for i in range(0,len(home_log_paths)):
                tar_cmd+='%s '
                tar_cmd = tar_cmd % a[i]
        run("sudo -u "+user+" "+tar_cmd)
        s3_upload = ''' s3cmd put %s s3://noc-archive-oregon/logs/${HOSTNAME}`pwd`/ ''' % ('/home/%s/%s-logs.tar.gz' % (user,time.strftime('%Y-%m-%d')))
        run(s3_upload)
        s3_obj_md5 = run('s3cmd --list-md5 ls s3://noc-archive-oregon/logs/${HOSTNAME}`pwd`%s' % ('/home/%s/%s-logs.tar.gz' % (user,time.strftime('%Y-%m-%d'))) +"|awk '{print $4}' " )
        local_obj_md5 = run('md5sum %s' %('/home/%s/%s-logs.tar.gz' % (user,time.strftime('%Y-%m-%d')))+"|awk '{print $1}'")
        if str(s3_obj_md5) == str(local_obj_md5):
            print "log package has been uploaded to S3 and md5 check pass"
        else:
            print "ERROR message"
            sys.exit(0)




















