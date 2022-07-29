from inventory import *
from store_data import *
import logging, os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
bucket_name = os.environ.get('bucket_name')

def lambda_handler(event, context):
    logger.info(f'event: {event}')

    try:
        #Get Inventory Data:
        availability_zones = get_availability_zones()
        ec2_inventory = get_ec2(availability_zones)
        rds_inventory = get_rds()

        #Create Inventory List:
        AWS_Inventory = []
        for index in ec2_inventory:
            AWS_Inventory.append(index)
        for index in rds_inventory:
            AWS_Inventory.append(index)
        AWS_Inventory.append(rds_inventory)

        #Store Inventory in S3:
        save_json(AWS_Inventory)
        push_to_s3(bucket_name)

        return AWS_Inventory

    except Exception as error:
        logger.error(error)
        return {
            'statusCode': 400,
            'message': 'An error has occurred',
			'moreInfo': {
				'Lambda Request ID': '{}'.format(context.aws_request_id),
				'CloudWatch log stream name': '{}'.format(context.log_stream_name),
				'CloudWatch log group name': '{}'.format(context.log_group_name)
				}
			}