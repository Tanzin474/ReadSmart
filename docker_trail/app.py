from flask import Flask
import json

app = Flask(__name__)


def handler(event, context):
    return {
        "statusCode": 200 ,
        "body": json.dumps({"message": "finally"}),
        "headers": {
                "Content-Type": "application/json"
        }
    }
