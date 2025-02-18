import json
from main import handler  # Import the Mangum handler from main.py

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    response = handler(event, context)  # Call the Mangum handler
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }