import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import logging, json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

regions_scope = [
    "us-east-1",
    "us-east-2"
]

roles_file = open('cross_account_roles.json')
roles_list = json.load(roles_file)
local_account_description = "AWS-Inventory"

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

def get_account_id():
    sts_connection = boto3.client('sts')
    get_account_id = sts_connection.get_caller_identity()
    account_id = get_account_id['Account']

    return account_id

def get_ec2_local(AWS_Inventory, availability_zones):
    #Get the AWS Account ID:
    account_id = get_account_id()

    #Get the EC2 Inventory:
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        ec2 = boto3.client(
            'ec2',
            config=boto3_config
            )
        
        for az in availability_zones:
            response = ec2.describe_instances(Filters=[{'Name': 'availability-zone', 'Values': [ '{}'.format(az) ]}, ])

            if len(response["Reservations"]) > 0:
                i = 0
                while i < len(response['Reservations']):
                    for instance in response['Reservations'][i]['Instances']:
                        instance_details = {
                            'AccountID': '{}'.format(account_id),
                            'AccountDescription': '{}'.format(local_account_description),
                            'InstanceId': '{}'.format(instance["InstanceId"]),
                            'InstanceType': '{}'.format(instance["InstanceType"]),
                            'AvailabilityZone': '{}'.format(instance["Placement"]["AvailabilityZone"]),
                            'State': '{}'.format(instance["State"]["Name"]),
                            'PlatformDetails': '{}'.format(instance["PlatformDetails"])
                            }
                        AWS_Inventory.append(instance_details)
                        i += 1

def get_ec2_cross_accounts_router(AWS_Inventory, availability_zones):
    try:
        for role in roles_list:
             get_ec2_cross_accounts(AWS_Inventory, availability_zones, role)
    except Exception as error:
        logger.error(error)

def get_ec2_cross_accounts(AWS_Inventory, availability_zones, role):
    #Set the Cross Account Credentials: 
    sts_connection = boto3.client('sts')
    cross_account_role = sts_connection.assume_role(
        RoleArn="{}".format(role['RoleArn']),
        RoleSessionName="{}".format(role['RoleSessionName'])
    )
    ACCESS_KEY = cross_account_role['Credentials']['AccessKeyId']
    SECRET_KEY = cross_account_role['Credentials']['SecretAccessKey']
    SESSION_TOKEN = cross_account_role['Credentials']['SessionToken']

    #Get the AWS Account ID:
    sts_connection = boto3.client(
        'sts',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    get_account_id = sts_connection.get_caller_identity()
    account_id = get_account_id['Account']

    #Get the EC2 Inventory:
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            config=boto3_config
            )
        
        for az in availability_zones:
            response = ec2.describe_instances(Filters=[{'Name': 'availability-zone', 'Values': [ '{}'.format(az) ]}, ])

            if len(response["Reservations"]) > 0:
                i = 0
                while i < len(response['Reservations']):
                    for instance in response['Reservations'][i]['Instances']:
                        instance_details = {
                            'AccountID': '{}'.format(account_id),
                            'AccountDescription': '{}'.format(role['Description']),
                            'InstanceId': '{}'.format(instance["InstanceId"]),
                            'InstanceType': '{}'.format(instance["InstanceType"]),
                            'AvailabilityZone': '{}'.format(instance["Placement"]["AvailabilityZone"]),
                            'State': '{}'.format(instance["State"]["Name"]),
                            'PlatformDetails': '{}'.format(instance["PlatformDetails"])
                            }
                        AWS_Inventory.append(instance_details)
                        i += 1

def get_rds_local(AWS_Inventory):
    #Get the AWS Account ID:
    account_id = get_account_id()

    #Get the RDS Inventory:  
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        rds = boto3.client('rds', config=boto3_config)
        response = rds.describe_db_instances()
        for instance in response['DBInstances']:
            instance_details = {
                'AccountID': '{}'.format(account_id),
                'AccountDescription': '{}'.format(local_account_description),
                'DBInstanceArn': '{}'.format(instance["DBInstanceArn"]),
                'DBInstanceClass': '{}'.format(instance["DBInstanceClass"]),
                'AvailabilityZone': '{}'.format(instance["AvailabilityZone"]),
                'DBInstanceStatus': '{}'.format(instance["DBInstanceStatus"]),
                'Engine': '{}'.format(instance["Engine"])
            }
            AWS_Inventory.append(instance_details)

def get_rds_cross_accounts_router(AWS_Inventory):
    try:
        for role in roles_list:
            get_rds_cross_accounts(AWS_Inventory, role)
    except Exception as error:
        logger.error(error)

def get_rds_cross_accounts(AWS_Inventory, role):
    #Set the Cross Account Credentials: 
    sts_connection = boto3.client('sts')
    cross_account_role = sts_connection.assume_role(
        RoleArn="{}".format(role['RoleArn']),
        RoleSessionName="{}".format(role['RoleSessionName'])
    )
    ACCESS_KEY = cross_account_role['Credentials']['AccessKeyId']
    SECRET_KEY = cross_account_role['Credentials']['SecretAccessKey']
    SESSION_TOKEN = cross_account_role['Credentials']['SessionToken']

    #Get the AWS Account ID:
    sts_connection = boto3.client(
        'sts',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    get_account_id = sts_connection.get_caller_identity()
    account_id = get_account_id['Account']

    #Get the RDS Inventory:  
    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        rds = boto3.client(
            'rds',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            config=boto3_config
            )
        response = rds.describe_db_instances()
        for instance in response['DBInstances']:
            instance_details = {
                'AccountID': '{}'.format(account_id),
                'AccountDescription': '{}'.format(role['Description']),
                'DBInstanceArn': '{}'.format(instance["DBInstanceArn"]),
                'DBInstanceClass': '{}'.format(instance["DBInstanceClass"]),
                'AvailabilityZone': '{}'.format(instance["AvailabilityZone"]),
                'DBInstanceStatus': '{}'.format(instance["DBInstanceStatus"]),
                'Engine': '{}'.format(instance["Engine"])
            }
            AWS_Inventory.append(instance_details)

def get_ecs_local(AWS_Inventory):
    account_id = get_account_id()

    for region in regions_scope:
        boto3_config = Config(region_name = '{}'.format(region))
        ecs = boto3.client(
            'ecs',
            config=boto3_config
            )

        list_clusters = ecs.list_clusters()

        for clusterArn in list_clusters['clusterArns']:
            cluster_description = ecs.describe_clusters(clusters=['{}'.format(clusterArn)])
            for cluster in cluster_description['clusters']:
                if len(cluster['capacityProviders']) > 0:
                    capacityProviders  = cluster['capacityProviders']
                    cluster_details = {
                        'AccountID': '{}'.format(account_id),
                        'AccountDescription': '{}'.format(local_account_description),
                        'clusterName': '{}'.format(cluster['clusterName']),
                        'clusterArn': '{}'.format(cluster['clusterArn']),
                        'status': '{}'.format(cluster['status']),
                        'runningTasksCount': '{}'.format(cluster['runningTasksCount']),
                        'capacityProviders': '{}'.format(capacityProviders)
                    }
                
                else:
                    cluster_details = {
                        'AccountID': '{}'.format(account_id),
                        'AccountDescription': '{}'.format(local_account_description),
                        'clusterName': '{}'.format(cluster['clusterName']),
                        'clusterArn': '{}'.format(cluster['clusterArn']),
                        'status': '{}'.format(cluster['status']),
                        'runningTasksCount': '{}'.format(cluster['runningTasksCount'])
                    }

                AWS_Inventory.append(cluster_details)

def get_s3_inventory(AWS_Inventory):
    account_id = get_account_id()
    s3 = boto3.client('s3')
    buckets_list = s3.list_buckets()

    for bucket in buckets_list['Buckets']:
        bucket_name = bucket['Name']

        try:
            versioning = s3.get_bucket_versioning(Bucket='{}'.format(bucket_name))
            if 'Status' in versioning:
                VersioningStatus = versioning['Status']
            else:
                VersioningStatus = 'Not Enabled'
        except ClientError as error:
            if error.response['Error']['Code'] == 'NoSuchBucket':
                logger.error('Error on {}, error message: {}'.format(bucket_name, error))
        try:
            encryption = s3.get_bucket_encryption(Bucket='{}'.format(bucket_name))
            EncryptedEnabled = True

        except ClientError as error:
            if error.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                EncryptedEnabled = True
        try:
            public_access_block = s3.get_public_access_block(Bucket='{}'.format(bucket_name))
            PublicAccessBlockConfiguration = json.dumps(public_access_block['PublicAccessBlockConfiguration'])
            PublicAccessBlockConfiguration =json.loads(PublicAccessBlockConfiguration)
        except ClientError as error:    
            if error.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                PublicAccessBlockConfiguration = 'Not configured'

        s3_object = {
            'AccountID': '{}'.format(account_id),
            'AccountDescription': '{}'.format(local_account_description),
            'BucketName': '{}'.format(bucket_name),
            'Encrypted': '{}'.format(EncryptedEnabled),
            'VersioningStatus': '{}'.format(VersioningStatus),
            'PublicAccessBlockConfiguration': '{}'.format(PublicAccessBlockConfiguration)
        }
        
        AWS_Inventory.append(s3_object)