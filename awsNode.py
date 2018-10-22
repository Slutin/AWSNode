import boto3
import paramiko
import commands
import thread
import os
import subprocess
import time
from multiprocessing import Process, Manager


key_path = "node.pem"#raw_input("Enter KeyPath and KeyName: ")

key = paramiko.RSAKey.from_private_key_file(key_path)
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

aws_key = "" #raw_input("Enter AWS access key: ")
secret_key = ""#raw_input("Enter AWS secret key: ")
ec2 = boto3.client('ec2', aws_access_key_id=aws_key, aws_secret_access_key=secret_key)
image = "ami-064e11d4ce7440c91"

def startGeth(_client, _ip, _key):
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=ip, username="ubuntu", pkey=key)
        client.exec_command('geth --rinkeby')
        print "Geth started..."
    except Exception, e:
        print e

def attachGeth(_key_path, _ip):
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        cmd = "ssh -t -i {0} {1}@{2}".format(key_path, "ubuntu", ip)
        subprocess.call(cmd, shell=True)

    except Exception, e:
        print e

def checkForInstance(_ec2, _image):
    inst = ec2.describe_instances()
    imageid = inst['Reservations'][0]['Instances'][0]['ImageId']
    if(imageid != image):
        print "Instance {0} not found. Creating instance".format(image)
        instances = ec2.create_instances(
            ImageId= image,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='node',
            SecurityGroups=['launch-wizard-1'])
        print "waiting to start instance"
        instance.wait_until_running()
        print "Instance is running"

#checkForInstance(ec2, image)
ip = ec2.describe_instances()['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
print ip
# Connect/ssh to an instance

thread.start_new_thread(startGeth, (client, ip, key))

time.sleep(3)
#thread.start_new_thread(attachGeth, (key_path, ip))'''
#attachGeth(client, ip, key)


exit = raw_input("enter to exit");

'''
cmd = "ssh -i {0} {1}@{2}".format(key_path, username, ip)
print commands.getstatusoutput("{0} 'geth --rinkeby'".format(cmd))
print commands.getstatusoutput("{0} 'geth attach  /home/ubuntu/.ethereum/rinkeby/geth.ipc'".format(cmd))'''
