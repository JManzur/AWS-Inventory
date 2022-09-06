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
        availability_zones = get_availability_zones()
        if scan_local_account == True:
            #Get Local and Cross Account Inventory Data:
            local_ec2_inventory = get_ec2_local(availability_zones)
            cross_account_ec2_inventory = get_ec2_cross_accounts_router(availability_zones)
            local_rds_inventory = get_rds_local()
            cross_account_rds_inventory = get_rds_cross_accounts_router()
            local_ecs_inventory = get_ecs_local()

            #Create Local and Cross Account Inventory List:
            EC2_Inventory_Local = []
            EC2_Inventory_Cross = []
            if len(local_ec2_inventory) > 0:
                for index in local_ec2_inventory:
                    EC2_Inventory_Local.append(index)
            if len(cross_account_ec2_inventory) > 0:
                for index in cross_account_ec2_inventory:
                    EC2_Inventory_Cross.append(index)

            RDS_Inventory_Local = []
            RDS_Inventory_Cross = []
            if len(local_rds_inventory) > 0:
                for index in local_rds_inventory:
                    RDS_Inventory_Local.append(index)
            if len(cross_account_rds_inventory) > 0:
                for index in cross_account_rds_inventory:
                    RDS_Inventory_Cross.append(index)

            ECS_Inventory_Local = []
            ECS_Inventory_Cross = []
            if len(local_ecs_inventory) > 0:
                for index in local_ecs_inventory:
                    ECS_Inventory_Local.append(index)

        else:
            #Get Cross Account Inventory Data:
            cross_account_ec2_inventory = get_ec2_cross_accounts_router(availability_zones)
            cross_account_rds_inventory = get_rds_cross_accounts_router()

            #Create Cross Account Inventory List:
            EC2_Inventory_Cross = []
            if len(cross_account_ec2_inventory) > 0:
                for index in cross_account_ec2_inventory:
                    EC2_Inventory_Cross.append(index)
            RDS_Inventory_Cross = []
            if len(cross_account_rds_inventory) > 0:
                for index in cross_account_rds_inventory:
                    RDS_Inventory_Cross.append(index)

        #Return the full inventory list:
        AWS_Inventory = []
        if len(EC2_Inventory_Local) > 0:
            for index in EC2_Inventory_Local:
                AWS_Inventory.append(index)
        if len(EC2_Inventory_Cross) > 0:
            for index in EC2_Inventory_Cross:
                AWS_Inventory.append(index)
        if len(RDS_Inventory_Local) > 0:
            for index in RDS_Inventory_Local:
                AWS_Inventory.append(index)
        if len(RDS_Inventory_Cross) > 0:
            for index in RDS_Inventory_Cross:
                AWS_Inventory.append(index)
        if len(ECS_Inventory_Local) > 0:
            for index in ECS_Inventory_Local:
                AWS_Inventory.append(index)

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