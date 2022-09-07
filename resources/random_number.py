import json
import os
from http import HTTPStatus, client
import numpy as np
import scipy


def lambda_handler(event, context):

    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({"output": np.random.random()}),
    }
