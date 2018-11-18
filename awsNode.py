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

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

def startGeth(_client):
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        # client.exec_command()

        sshcmd = '"geth --rinkeby"'
        cmd = "gnome-terminal -e 'ssh -i {0} {1}@{2} {3}'".format(key_path, "ubuntu", ip, sshcmd)
        os.system("{0} ".format(cmd))
        print "Geth started..."

    except Exception, e:
        print e

def attachGeth(_client):
    try:
        sshcmd = '"geth attach ipc:/home/ubuntu/.ethereum/rinkeby/geth.ipc"'
        cmd = "gnome-terminal -e 'ssh -i {0} {1}@{2} {3}'".format(key_path, "ubuntu", ip, sshcmd)
        os.system("{0} ".format(cmd))
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
client.connect(hostname=ip, username="ubuntu", pkey=key)

startGeth(client)

time.sleep(3)

attachGeth(client)


exit = raw_input("enter to exit");

'''
cmd = "ssh -i {0} {1}@{2}".format(key_path, username, ip)
print commands.getstatusoutput("{0} 'geth --rinkeby'".format(cmd))
print commands.getstatusoutput("{0} 'geth attach  /home/ubuntu/.ethereum/rinkeby/geth.ipc'".format(cmd))'''
