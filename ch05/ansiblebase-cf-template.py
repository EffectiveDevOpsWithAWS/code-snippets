#!/usr/bin/env python

from troposphere import (
    Base64,
    cloudformation,
    ec2,
    GetAtt,
    Join,
    Output,
    Parameter,
    Ref,
    Template,
)

from ipify import get_ip
from ipaddress import ip_network

ApplicationName = "helloworld"
ApplicationPort = "3000"

GithubAccount = "EffectiveDevOpsWithAWS"
GithubAnsibleURL = "https://github.com/%s/ansible" % GithubAccount

AnsiblePullCmd = "/usr/local/bin/ansible-pull -U %s %s.yml -i localhost" \
  % (GithubAnsibleURL, ApplicationName)

PublicCidrIp = str(ip_network(get_ip()))

t = Template()

kp = t.add_parameter(Parameter(
    "KeyPair",
    Description="Name of an existing EC2 KeyPair to SSH",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair.",
))

sg = t.add_resource(ec2.SecurityGroup(
    "SecurityGroup",
    GroupDescription="Allow SSH and TCP/{} access".format(ApplicationPort),
    SecurityGroupIngress=[
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
          ),
    ],
))

ud = Base64(Join('\n', [
        "#!/bin/bash",
        "exec > /var/log/userdata.log 2>&1",
        "sudo yum install --enablerepo=epel -y git",
        "sudo pip install ansible",
        AnsiblePullCmd,
        "echo '*/10 * * * * %s' > /etc/cron.d/ansible-pull" % AnsiblePullCmd
    ]))

instance = t.add_resource(ec2.Instance(
    "instance",
    ImageId="ami-f5f41398",
    InstanceType="t2.micro",
    SecurityGroups=[Ref(sg)],
    KeyName=Ref(kp),
    UserData=ud,
))

t.add_output(Output(
    "InstancePublicIp",
    Description="Public IP of our instance.",
    Value=GetAtt(instance, "PublicIp"),
))

t.add_output(Output(
    "WebUrl",
    Description="Application endpoint",
    Value=Join("", [
        "http://", GetAtt(instance, "PublicDnsName"),
        ":", ApplicationPort
    ]),
))

print t.to_json()
