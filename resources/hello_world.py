import json
import os
from http import HTTPStatus, client


def lambda_handler(event, context):

    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps(
            {"message": "Hello!!!", "rn": os.environ.get("RANDOM_NUMBER_LAMBDA")}
        ),
    }
