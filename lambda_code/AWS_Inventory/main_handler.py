from inventory import *
from store_data import *
import logging, os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
bucket_name = os.environ.get('bucket_name')
scan_local_account = True

def lambda_handler(event, context):
    logger.info(f'event: {event}')
    
    AWS_Inventory = []
    try:
        availability_zones = get_availability_zones()
        if scan_local_account == True:
            get_ec2_local(AWS_Inventory, availability_zones)
            get_ec2_cross_accounts_router(AWS_Inventory, availability_zones)
            get_rds_local(AWS_Inventory)
            get_rds_cross_accounts_router(AWS_Inventory)
            get_ecs_local(AWS_Inventory)

            save_full_inventory(AWS_Inventory)
            push_full_inventory_to_s3(bucket_name)
            return AWS_Inventory
        else:
            #Get Cross Account Inventory Data:
            get_ec2_cross_accounts_router(AWS_Inventory, availability_zones)
            get_rds_cross_accounts_router(AWS_Inventory)

            save_full_inventory(AWS_Inventory)
            push_full_inventory_to_s3(bucket_name)
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