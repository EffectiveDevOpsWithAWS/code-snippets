#!/bin/bash -e

INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
VOLUME_ID=$(aws ec2 --region=us-east-1 describe-instances \
  --query 'Reservations[].Instances[].BlockDeviceMappings[].Ebs[].VolumeId' \
  --filters "Name=instance-id,Values=${INSTANCE_ID}" --output=text)
aws ec2 --region=us-east-1 create-snapshot --volume-id ${VOLUME_ID} \
  --description "Ghost root device automated snapshot from ${INSTANCE_ID}"
