#!/usr/bin/python

#This script will START or STOP instances for any region.

import boto3
import os
import sys
import time
import logging
import goto

def get_ec2_con_for_give_region(my_region):
    ec2_con_re=boto3.resource('ec2',region_name=my_region)
    return ec2_con_re

#This function returns all the instances and their info
def list_instances_on_my_region(ec2_con_re):
    for each in ec2_con_re.instances.all():
        print "Instance name        Instance ID         State       Private IP      Public IP"
        print each.tags[0]['Value'],each.id,    each.state['Name'], each.private_ip_address,    each.public_ip_address

#The function returns the current state (running or stopped) of the instance
def get_instant_state(ec2_con_re,in_id):
    for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
        pr_st=each.state['Name']
    return pr_st

#This function starts an instance when provided the instance id
def start_instance(ec2_con_re,in_id):
    pr_st=get_instant_state(ec2_con_re,in_id)
    if pr_st=="running":
            print"Given Instance is already running"
    else:
        for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
                each.start()
                print"Please wait starting the instance, once the instance is started, we will let you know"
                time.sleep(10)
    return

def Thank_you():
    print"\n\n**********Thank you for using this script*************"
    return None

#This function Stops an instance when provided the instance id
def stop_instance(ec2_con_re,in_id):
    pr_st=get_instant_state(ec2_con_re,in_id)
    if pr_st=="stopped":
            print"Given instance is already stopped."
    else:
        for each in ec2_con_re.instances.filter(Filters=[{'Name':'instance-id',"Values":[in_id]}]):
                each.stop()
                print"Please wait stopping the given instance, once the instance stops we will let you know."
                each.wait_until_stopped()
                print"Instance stopped succefully.\n"
                time.sleep(10)
    return

def welcome():
    print"This script will help you to start or stop ec2 instances based on your required region and instance id"
    time.sleep(3)

#The execution starts from here
def main():
    welcome()

    logging.basicConfig(filename='/var/log/aws_automation.log', mode='a', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    my_region=raw_input("Please provide the region: ")
    print"Please wait....connecting to your aws ec2 console...."
    ec2_con_re=get_ec2_con_for_give_region(my_region)
    print"Please wait listing all instances in your region {}".format(my_region)
    print"\n"
    while True:
        #print"InstanceIds         State   PrivateIPAddr PublicIpAddr"
        try:
            list_instances_on_my_region(ec2_con_re)
        except:
            print "Invalid region entered. Exiting the script \n \n"
            time.sleep(2)
            sys.exit()
        logging.info('Listing all instances')


        print"\n Press 1 to start \n Press 2 to stop \n Press 3 to exit \n"
        option=raw_input("What do you wnat to do: ")
        while True:
            if option not in ["1","2","3"]:
                    option=raw_input("Enter only between 1, 2 or 3: ")
                    continue
            else:
                    break

        if option == "1":
            in_id=raw_input("\n Please enter the instance Id to Start:")
            start_instance(ec2_con_re,in_id)
            logging.info('Starting instance %s', in_id)
            continue
        elif option == "2":
            in_id=raw_input("\n Please enter the instance Id to stop:")
            stop_instance(ec2_con_re,in_id)
            logging.info('Stoping instance %s', in_id)
            continue
        elif option == "3":
            False
            sys.exit()
            logging.info('Exited')

    Thank_you()

if __name__=='__main__':
    os.system('clear')
    main()
