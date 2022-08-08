import boto3
import logging
import json, os, logging, glob
from pathlib import Path
from datetime import datetime

os.chdir('/tmp')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

now = datetime.now()
current_date = now.strftime("%d-%m-%Y-%H%M%S")

def insert_ec2_data(ec2_inventory):
    dynamodb = boto3.resource('dynamodb')
    project_table = dynamodb.Table('AWS_Inventory')
    for i in ec2_inventory:
        try:
            project_table.put_item(
                Item={
                    'ID': '{}'.format(i['InstanceId']),
                    'InstanceType': '{}'.format(i['InstanceType']),
                    'AvailabilityZone': '{}'.format(i['AvailabilityZone']),
                    'State': '{}'.format(i['State'])
                }
            )
        
        except KeyError as error:
            logger.error(error)

def save_json(EC2_Inventory, RDS_Inventory):
    print("Executing: save_json")
    Path("output_files/EC2/").mkdir(parents=True, exist_ok=True)
    
    try:
        with open("output_files/EC2/EC2_Inventory.json", 'w') as outfile:
            json.dump(EC2_Inventory, outfile, ensure_ascii=False, indent=4)
        with open("output_files/EC2/EC2_Inventory-{}.json".format(current_date), 'w') as outfile:
            json.dump(EC2_Inventory, outfile, ensure_ascii=False, indent=4)
    except IOError:
        print("ERROR: Unable to save file")

    Path("output_files/RDS/").mkdir(parents=True, exist_ok=True)
    try:
        with open("output_files/RDS/RDS_Inventory.json", 'w') as outfile:
            json.dump(RDS_Inventory, outfile, ensure_ascii=False, indent=4)
        with open("output_files/RDS/RDS_Inventory-{}.json".format(current_date), 'w') as outfile:
            json.dump(RDS_Inventory, outfile, ensure_ascii=False, indent=4)
    except IOError:
        print("ERROR: Unable to save file")

def push_to_s3(bucket_name):
    print("Executing: push_to_s3")
    EC2_Inventory = glob.glob("output_files/EC2/*.json")
    RDS_Inventory = glob.glob("output_files/RDS/*.json")
    s3 = boto3.resource('s3')

    for filename in EC2_Inventory:
        json_filename = os.path.basename(filename)
        object = s3.Object(bucket_name, 'aws_inventory/ec2/{}'.format(json_filename))
        result = object.put(Body=open(filename, 'rb'),)
        res = result.get('ResponseMetadata')
        logger.info("S3 ResponseMetadata: {}".format(res))
        if res.get('HTTPStatusCode') == 200:
            logger.info('File {} uploaded successfully'.format(json_filename))
        else:
            logger.error('File {} Not Uploaded'.format(json_filename))

    for filename in RDS_Inventory:
        json_filename = os.path.basename(filename)
        object = s3.Object(bucket_name, 'aws_inventory/rds/{}'.format(json_filename))
        result = object.put(Body=open(filename, 'rb'),)
        res = result.get('ResponseMetadata')
        logger.info("S3 ResponseMetadata: {}".format(res))
        if res.get('HTTPStatusCode') == 200:
            logger.info('File {} uploaded successfully'.format(json_filename))
        else:
            logger.error('File {} Not Uploaded'.format(json_filename))