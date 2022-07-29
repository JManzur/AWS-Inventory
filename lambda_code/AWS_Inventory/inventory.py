import boto3
from botocore.config import Config
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

regions_scope = [
    "us-east-1",
    "us-east-2"
]

def get_regions():
    ec2 = boto3.client('ec2')
    response = ec2.describe_regions()
    region_list = []
    for region in response['Regions']:
        RegionName = region['RegionName']
        region_list.append(RegionName)
    return region_list

def get_availability_zones():
    availability_zones_list = []
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        ec2 = boto3.client('ec2', config=boto3_config)
        response = ec2.describe_availability_zones(
            Filters=[
                {
                    'Name': 'region-name',
                    'Values': [
                        '{}'.format(region)
                        ]
                },
            ],
            AllAvailabilityZones=True,
            DryRun=False
            )

        for az in response['AvailabilityZones']:
            ZoneName = az['ZoneName']
            availability_zones_list.append(ZoneName)
    
    return availability_zones_list

def get_ec2(availability_zones):
    instances_list = []
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        ec2 = boto3.client('ec2', config=boto3_config)
        
        for az in availability_zones:
            response = ec2.describe_instances(Filters=[{'Name': 'availability-zone', 'Values': [ '{}'.format(az) ]}, ])

            if len(response["Reservations"]) > 0:
                i = 0
                while i < len(response['Reservations']):
                    for instance in response['Reservations'][i]['Instances']:
                        instance_details = {
                            'InstanceId': '{}'.format(instance["InstanceId"]),
                            'InstanceType': '{}'.format(instance["InstanceType"]),
                            'AvailabilityZone': '{}'.format(instance["Placement"]["AvailabilityZone"]),
                            'State': '{}'.format(instance["State"]["Name"]),
                            'PlatformDetails': '{}'.format(instance["PlatformDetails"])
                            }
                        instances_list.append(instance_details)
                        i += 1
    logger.info("RDS-Inventory: The number of EC2 instances in the Account is: {}".format(len(instances_list)))
    return instances_list

def get_rds():
    instances_list = []
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        rds = boto3.client('rds', config=boto3_config)
        response = rds.describe_db_instances()
        for instance in response['DBInstances']:
            instance_details = {
                'DBInstanceArn': '{}'.format(instance["DBInstanceArn"]),
                'DBInstanceClass': '{}'.format(instance["DBInstanceClass"]),
                'AvailabilityZone': '{}'.format(instance["AvailabilityZone"]),
                'DBInstanceStatus': '{}'.format(instance["DBInstanceStatus"]),
                'Engine': '{}'.format(instance["Engine"])
            }
            instances_list.append(instance_details)

    logger.info("RDS-Inventory: The number of RDS instances in the Account is: {}".format(len(instances_list)))
    return instances_list