import boto3
import logging
import json, os, logging, glob
from pathlib import Path

os.chdir('/tmp')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

def save_json(AWS_Inventory):
    print("Executing: save_json")
    Path("output_files/").mkdir(parents=True, exist_ok=True)
    try:
        with open("output_files/aws_inventory.json", 'w') as outfile:
            json.dump(AWS_Inventory, outfile, ensure_ascii=False, indent=4)
            print("INFO: File saved successfully")

    except IOError:
        print("ERROR: Unable to save file")

def push_to_s3(bucket_name):
    print("Executing: push_to_s3")
    json_files = glob.glob("output_files/*.json")
    s3 = boto3.resource('s3')

    for filename in json_files:
        json_filename = os.path.basename(filename)
        object = s3.Object(bucket_name, 'aws_inventory/{}'.format(json_filename))
        result = object.put(Body=open(filename, 'rb'),)
        res = result.get('ResponseMetadata')
        logger.info("S3 ResponseMetadata: {}".format(res))
        if res.get('HTTPStatusCode') == 200:
            logger.info('File {} uploaded successfully'.format(json_filename))
        else:
            logger.error('File {} Not Uploaded'.format(json_filename))