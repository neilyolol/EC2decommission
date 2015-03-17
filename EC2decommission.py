#!/usr/bin/env python
# Verion 0.1
# Author: Chao
#Created @20150317
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


def get_elb_with_instanceID(elbconn, instance_id):
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


def get_tomcat_user():
    tomcat_user = run("ps -ef|grep java|grep -v `whoami`|awk '{print $1}'")
    return list(set(java_user.split('\r\n')))


def tomcat_home():
    command = '''ps -fC java --noheaders|awk '{for (i=1;i<=NF;i++) { if ( $i ~ /Dcatalina.home/ ) {split($i,x,"="); print x[2]}}}' '''
    return run(command).splitlines()


def home_log_dir(user):
    path = "/home/" + user + "/"
    command = "find " + path + " \( -type d -o -type l \) -name '*log*' -print 2>/dev/null"
    return sudo(command, user=user).splitlines()


def shutdown_tomcat():


