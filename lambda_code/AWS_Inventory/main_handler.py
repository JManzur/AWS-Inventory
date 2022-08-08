from inventory import *
from store_data import *
import logging, os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
bucket_name = os.environ.get('bucket_name')
scan_local_account = True

def lambda_handler(event, context):
    logger.info(f'event: {event}')

    try:
        #Get Inventory Data:
        availability_zones = get_availability_zones()
        if scan_local_account == True:
            #EC2:
            local_ec2_inventory = get_ec2_local(availability_zones)
            cross_account_ec2_inventory = get_ec2_cross_accounts(availability_zones)
            #RDS:
            local_rds_inventory = get_rds_local()
        else:
            #EC2:
            cross_account_ec2_inventory = get_ec2_cross_accounts(availability_zones)
            #RDS:

        #Create Inventory List:
        EC2_Inventory = []
        for index in local_ec2_inventory:
            EC2_Inventory.append(index)
        for index in cross_account_ec2_inventory:
            EC2_Inventory.append(index)

        RDS_Inventory = []
        for index in local_rds_inventory:
            RDS_Inventory.append(index)
        for index in local_rds_inventory:
            RDS_Inventory.append(index)

        #Store Inventory in S3:
        save_json(EC2_Inventory, RDS_Inventory)
        push_to_s3(bucket_name)

        #Return the full inventory list:
        AWS_Inventory = []
        AWS_Inventory.append(EC2_Inventory)
        AWS_Inventory.append(RDS_Inventory)
        return AWS_Inventory

        # return {
        #     'Message': 'Success!'
        # }

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