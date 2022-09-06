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

def save_full_inventory(AWS_Inventory):
    print("Executing: save_json")

    Path("output_files/AWS_Inventory/").mkdir(parents=True, exist_ok=True)
    try:
        with open("output_files/AWS_Inventory/AWS_Inventory.json", 'w') as outfile:
            json.dump(AWS_Inventory, outfile, ensure_ascii=False, indent=4)
        with open("output_files/EC2/AWS_Inventory_{}.json".format(current_date), 'w') as outfile:
            json.dump(AWS_Inventory, outfile, ensure_ascii=False, indent=4)
    except IOError:
        print("ERROR: Unable to save file")

def push_full_inventory_to_s3(bucket_name):
    print("Executing: push_to_s3")
    AWS_Inventory = glob.glob("output_files/AWS_Inventory/*.json")
    s3 = boto3.resource('s3')

    for filename in AWS_Inventory:
        json_filename = os.path.basename(filename)
        object = s3.Object(bucket_name, 'aws_inventory/ec2/{}'.format(json_filename))
        result = object.put(Body=open(filename, 'rb'),)
        res = result.get('ResponseMetadata')
        logger.info("S3 ResponseMetadata: {}".format(res))
        if res.get('HTTPStatusCode') == 200:
            logger.info('File {} uploaded successfully'.format(json_filename))
        else:
            logger.error('File {} Not Uploaded'.format(json_filename))