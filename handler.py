import json
import boto3
import logging
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def createUser(event, context):
    logger.info("Event: " + str(event))
    try:
        body = json.loads(event['body'])
        user_id = body['id']
        user_name = body['name']

        response = table.put_item(
            Item={
                'id': user_id,
                'name': user_name
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except ClientError as e:
        logger.error("ClientError: " + str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error("Exception: " + str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def getUserById(event, context):
    logger.info("Event: " + str(event))
    try:
        user_id = event['pathParameters']['id']

        response = table.get_item(
            Key={
                'id': user_id
            }
        )
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
    except ClientError as e:
        logger.error("ClientError: " + str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error("Exception: " + str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
