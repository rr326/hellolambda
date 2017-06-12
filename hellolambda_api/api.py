from flask import Flask, send_from_directory, request
from flask_cors import CORS
import boto3
import time
from datetime import datetime as dt
import json
import hellolambda_api.config as config
from hellolambda_api.config import EMAIL
from functools import wraps
from urllib.parse import urlparse
from hellolambda_api.limiter import daily_limit

app = Flask(__name__)
CORS(app, origins=config.CORS_ACCEPTABLE_ORIGINS)


#
# Support Functoins
#
def catch_errors():
    """
    @catch_errors
    """
    def wrap(func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            try:
                print(f'REQUEST: {request.url}')  # For logging. TODO - remove
                response = func(*args, **kwargs)
            except Exception as err:
                print('error: ', err)
                return str(err), 500
            else:
                return response
        return wrapped_f
    return wrap


def get_session():
    if config.is_debug_server:
        return boto3.Session(profile_name=config.LOCAL_AWS_PROFILE, region_name=config.AWS_REGION)
    else:
        return boto3.Session()

@app.route('/assets/<path:path>')
@catch_errors()
def send_assets(path):
    return send_from_directory(config.SITE_ASSETS_DIR, path)

def dynamodb_key():
    return 'formfield-' + dt.utcnow().isoformat()

def is_test_url(url):
    parsed = urlparse(url)
    return not (parsed.hostname in config.PRODUCTION_DOMAINS)

def make_valid_item(item_dict):
    # Replaces empty values in dict with ' ' (dynamodb.put doesn't accept '')
    # In-place, and returns same value
    for k, v in item_dict.items():
        if v is None or v is '':
            item_dict[k] = ' ' # choosing to store an empty val rather than deleting it
    return item_dict


@daily_limit('dynamo_put', config.MAX_DYNAMO_PER_DAY)
def dynamo_put(*args, **kwargs):
    session = get_session()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(config.DYNAMO_TABLE_NAME)
    response = table.put_item(*args, **kwargs)
    return response

@daily_limit('ses_send', config.MAX_EMAIL_PER_DAY)
def send_email(*args, **kwargs):
    session = get_session()
    client = session.client('ses')
    response = client.send_email(*args, **kwargs)
    return response


#
# Test endpoints
#
@app.route(f'{config.TEST_PATH_PREFIX}/test_dynamo')
@catch_errors()
def test_dynamo():
    item={'pk': dynamodb_key(),
              'note': 'sample data',
              'useragent': request.environ.get('HTTP_USER_AGENT', ' '),
              'remote_addr': request.environ.get('REMOTE_ADDR', ' '),
              'test': 'true' if is_test_url(request.environ.get('HTTP_ORIGIN', '')) else 'false'
              }
    dynamo_put(Item=item)
    return "Success"

@app.route(f'{config.TEST_PATH_PREFIX}/test_ses')
@catch_errors()
def test_ses():
    response = send_email(
        Source=config.EMAIL['from_addr'],
        Destination={
            'ToAddresses': [config.EMAIL['notification_addr']]
        },
        Message={
            'Subject': {
                'Data': 'Test from hellolambda',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Data': 'Test message.<br><b>This is bold</b><br>Last Line.',
                    'Charset': 'UTF-8'
                },
                'Text': {
                    'Data': 'Simple text-only body',
                    'Charset': 'UTF-8'
                }
            }
        }
    )
    return 'Success'


@app.route('/api/ping', methods=['GET', 'POST'])
@catch_errors()
def ping():
    return json.dumps(request.args), 200

#
# Real API functions
#

@app.route('/api/submit_feedback_form', methods=['POST'])
@catch_errors()
def submit_feedback_form():
    """
    Insert form to dynamodb
    Email admin
    """

    # Note: I set charset = "text/plain" in the ajax call to call this. So I need to take the data
    # part and transform it. (This helps with CORS)
    json_data = json.loads(request.data)
    form_data = {
        'email': json_data.get('email', ' ')[:200], # Note: Can not be an empty string
        'note': json_data.get('note', ' ')[:1024]
    }

    # Insert in db
    db_rsp = dynamo_put(
        Item=make_valid_item({'pk': dynamodb_key(),
              **form_data,
              'useragent': request.environ.get('HTTP_USER_AGENT', ' '),
              'remote_addr': request.environ.get('REMOTE_ADDR', ' '),
              'test': 'true' if is_test_url(request.environ.get('HTTP_ORIGIN', '')) else 'false'
              })
        )

    # Send email
    response = send_email(
        Source=EMAIL['from_addr'],
        Destination={
            'ToAddresses': [EMAIL['notification_addr']]
        },
        Message={
            'Subject': {
                'Data': EMAIL['feedback_subject'],
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': f'From: {form_data["email"]}\n'
                            f'Date: {dt.now().isoformat()}\n'
                            f'Notes: \n {form_data["note"]}\n',
                    'Charset': 'UTF-8'
                }
            }
        }
    )
    return 'Success', 200


