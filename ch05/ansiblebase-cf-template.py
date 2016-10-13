#!/usr/bin/env python

from troposphere import Ref, Template, ec2, Parameter, Output, Join, GetAtt, Base64, cloudformation
from json import load
from urllib2 import urlopen


ApplicationName = "helloworld"
ApplicationPort = "3000"

GithubAccount = "EffectiveDevOpsWithAWS"
GithubAnsibleURL = "https://github.com/%s/ansible" % GithubAccount

AnsiblePullCmd = "/usr/local/bin/ansible-pull -U %s %s.yml -i localhost" \
  % (GithubAnsibleURL, ApplicationName)

PublicIp = load(urlopen('https://api.ipify.org?format=json'))['ip']
PublicCidrIp = "%s/32" % PublicIp

t = Template()
kp = Parameter(
    "KeyPair",
    Description="Name of an existing EC2 KeyPair to SSH",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair."
  )
t.add_parameter(kp)

sg = ec2.SecurityGroup('SecurityGroup')
sg.GroupDescription = "Allow SSH and TCP/%s access" \
  % ApplicationPort
sg.SecurityGroupIngress = [
ec2.SecurityGroupRule(
    IpProtocol="tcp",
    FromPort="22",
    ToPort="22",
    CidrIp=PublicCidrIp,
  ),
ec2.SecurityGroupRule(
    IpProtocol="tcp",
    FromPort=ApplicationPort,
    ToPort=ApplicationPort,
    CidrIp="0.0.0.0/0",
  )]
t.add_resource(sg)

ud = Base64(Join('\n', [
        "#!/bin/bash",
        "exec > /var/log/userdata.log 2>&1",
        "sudo yum install --enablerepo=epel -y git",
        "sudo pip install ansible",
        AnsiblePullCmd,
        "echo '*/10 * * * * %s' > /etc/cron.d/ansible-pull" % AnsiblePullCmd
    ]))


instance = ec2.Instance("instance",
    ImageId="ami-f5f41398",
    InstanceType="t2.micro",
    SecurityGroups=[Ref(sg)],
    KeyName=Ref(kp),
    UserData=ud
)
t.add_resource(instance)

ip = Output(
    "InstancePublicIp",
    Description="Public IP of our instance.",
    Value=GetAtt(instance, "PublicIp")
  )
t.add_output(ip)

web = Output(
    "WebUrl",
    Description="Application endpoint",
    Value=Join("", ["http://", GetAtt(instance, "PublicDnsName"), \
      ":", ApplicationPort])
  )
t.add_output(web) 

print t.to_json()
