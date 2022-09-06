# from inventory import *
# from store_data import *
# import logging, os

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# bucket_name = os.environ.get('bucket_name')

# def lambda_handler(event, context):
#     logger.info(f'event: {event}')
#     scan_local_account = event['scan_local_account']
    
#     try:
#         availability_zones = get_availability_zones()
#         #Get Local and Cross Account Inventory Data:
#         if event['InventoryType'] == 'EC2' and event['ScanLocalAccount'] == True:
#             print("")
#         if event['InventoryType'] == 'RDS' and event['ScanLocalAccount'] == True:
#             print("")
#         if event['InventoryType'] == 'ECS' and event['ScanLocalAccount'] == True:
#             print("")
#         if event['InventoryType'] == 'GetAll' and event['ScanLocalAccount'] == True:
#             print("")

#         #Get Cross Account Inventory Data:
#         if event['InventoryType'] == 'EC2' and event['ScanLocalAccount'] == False:
#             print("")
#         if event['InventoryType'] == 'RDS' and event['ScanLocalAccount'] == False:
#             print("")
#         if event['InventoryType'] == 'ECS' and event['ScanLocalAccount'] == False:
#             print("")
#         if event['InventoryType'] == 'GetAll' and event['ScanLocalAccount'] == False:
#             print("")

#         if scan_local_account == True:
#             #Get Local and Cross Account Inventory Data:
#             local_ec2_inventory = get_ec2_local(availability_zones)
#             cross_account_ec2_inventory = get_ec2_cross_accounts_router(availability_zones)
#             local_rds_inventory = get_rds_local()
#             cross_account_rds_inventory = get_rds_cross_accounts()
#             local_ecs_inventory = get_ecs_local()

#             #Create Local and Cross Account Inventory List:
#             EC2_Inventory = []
#             for index in local_ec2_inventory:
#                 EC2_Inventory.append(index)
#             for index in cross_account_ec2_inventory:
#                 EC2_Inventory.append(index)

#             RDS_Inventory = []
#             for index in local_rds_inventory:
#                 RDS_Inventory.append(index)
#             for index in cross_account_rds_inventory:
#                 RDS_Inventory.append(index)

#             ECS_Inventory = []
#             for index in local_ecs_inventory:
#                 ECS_Inventory.append(index)

#         else:
#             #Get Cross Account Inventory Data:
#             cross_account_ec2_inventory = get_ec2_cross_accounts_router(availability_zones)
#             cross_account_rds_inventory = get_rds_cross_accounts()

#             #Create Cross Account Inventory List:
#             EC2_Inventory = []
#             for index in cross_account_ec2_inventory:
#                 EC2_Inventory.append(index)
#             RDS_Inventory = []
#             for index in cross_account_rds_inventory:
#                 RDS_Inventory.append(index)

#         #Store Inventory in S3:
#         save_json(EC2_Inventory, RDS_Inventory, ECS_Inventory)
#         push_to_s3(bucket_name)

#         #Return the full inventory list:
#         AWS_Inventory = []
#         AWS_Inventory.append(EC2_Inventory)
#         AWS_Inventory.append(RDS_Inventory)
#         AWS_Inventory.append(ECS_Inventory)
#         return AWS_Inventory

#         # return {
#         #     'Message': 'Success!'
#         # }

#     except Exception as error:
#         logger.error(error)
#         return {
#             'statusCode': 400,
#             'message': 'An error has occurred',
# 			'moreInfo': {
# 				'Lambda Request ID': '{}'.format(context.aws_request_id),
# 				'CloudWatch log stream name': '{}'.format(context.log_stream_name),
# 				'CloudWatch log group name': '{}'.format(context.log_group_name)
# 				}
# 			}