#!/usr/bin/env python
#Verion 0.1
#Author: Chao
#Created @20150317
#Only support virgina and oregon
import boto.ec2, boto.ec2.elb
import sys, time, argparse, ConfigParser

def get_region(instance_name):
    region_head = instance_name.split('-')[0]
    if region_head == 'ec1':
        region = 'us-east-1'
    elif region_head == 'ec2':
        region = 'us-west-2'
    return region


