#! /usr/bin/env python

import boto3

ec2 = boto3.resource('ec2')
client = boto3.client('cloudwatch')

warning_actions = [
'arn:aws:sns:us-east-1:511912822958:alert-email'
]

critical_actions = [
'arn:aws:sns:us-east-1:511912822958:alert-email',
'arn:aws:sns:us-east-1:511912822958:alert-sms'
]

disk_common_alert = dict(
    ActionsEnabled=True,
    MetricName='DiskSpaceUtilization',
    Namespace='System/Linux',
    Statistic='Average',
    Period=300,
    EvaluationPeriods=1,
    ComparisonOperator='GreaterThanThreshold'
) 

def get_dimension( instance_id ):
  dimension = [
    {
      'Name': 'InstanceId',
      'Value': instance_id
    }
  ]
  return dimension  

instances = ec2.instances.all()
instances_id = [instance.id for instance in instances]


for instance_id in instances_id:
  dimension = get_dimension(instance_id)
  
  response = client.put_metric_alarm(
    AlarmName='DiskSpaceAbove70',
    AlarmDescription='warn if disk usage is above 70%',
    Dimensions=dimension,
    AlarmActions=warning_actions,
    OKActions=warning_actions,
    Threshold=70,
    **disk_common_alert
  )
  print response

  response = client.put_metric_alarm(
    AlarmName='DiskSpaceAbove90',
    AlarmDescription='warn if disk usage is above 90%',
    Dimensions=dimension,
    AlarmActions=critical_actions,
    OKActions=critical_actions,
    Threshold=90,
    **disk_common_alert
  )
  print response
  
