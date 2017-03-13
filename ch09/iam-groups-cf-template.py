#!/usr/bin/env python
"""Generating CloudFormation template."""

from troposphere import (
    Template
)

from troposphere.iam import (
    Group
)

# s , Group, LoginProfile, PolicyType


t = Template()

t.add_description("Effective DevOps in AWS: User Groups")

t.add_resource(Group(
    "Admins",
    GroupName="Admins",
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/AdministratorAccess"
    ]
))

print t.to_json()
