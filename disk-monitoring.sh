#! /bin/sh

all_instances=$(aws ec2 describe-instances \
    --query "Reservations[*].Instances[*].{ID:InstanceId}" \
    --no-paginate \
    --output text)

for i in "${all_instances[@]}"; do
    aws cloudwatch put-metric-alarm \
        --alarm-name 'DiskSpaceAbove70' \
        --alarm-description "warn if disk usage is above 70%" \
        --metric-name 'DiskSpaceUtilization' \
        --namespace 'System/Linux' \
        --statistic Average \
        --period 300 \
        --threshold 70 \
        --comparison-operator GreaterThanThreshold  \
        --dimensions "Name=InstanceId,Value=$i" \
        --evaluation-periods 1  \
        --unit Percent \
        --alarm-actions 'arn:aws:sns:us-east-1:511912822958:alert-email'

    aws cloudwatch put-metric-alarm \
        --alarm-name 'DiskSpaceAbove90' \
        --alarm-description "warn if disk usage is above 90%" \
        --metric-name 'DiskSpaceUtilization' \
        --namespace 'System/Linux' \
        --statistic Average \
        --period 300 \
        --threshold 90 \
        --comparison-operator GreaterThanThreshold  \
        --dimensions "Name=InstanceId,Value=$i" \
        --evaluation-periods 1  \
        --unit Percent \
        --alarm-actions 'arn:aws:sns:us-east-1:511912822958:alert-email,\
          arn:aws:sns:us-east-1:511912822958:alert-sms'
done
