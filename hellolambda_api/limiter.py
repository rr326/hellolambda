from datetime import datetime as dt

import boto3

import hellolambda_api.config as config
from hellolambda_api.config import EMAIL


class daily_limit(object):
    """
    This is a simple way to limit the number of times a function will be called in a day.
    (It requires a DynamoDB table to store its data)
    The wrapped function will return None if it is bypassed.

    Usage:

    @daily_limit('some_function', 1000)
    def some_function():
        pass
    """
    def __init__(self, key, max_per_day):
        self.key = key
        self.max = max_per_day

        self.session = None
        self.dynamodb = None
        self.table = None

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            self.set_session()  # must defer to here so config.is_debug_server is set. TODO - clean up

            num_calls = self.get_todays_calls()

            retval = None
            if num_calls < self.max:
                retval = f(*args, **kwargs)
            elif num_calls == self.max:
                print(f'daily_limit: max calls ({self.max}) reached for {self.key}')
                self.notify_admin()
            else:
                print(f'daily_limit: max calls ({self.max}) reached for {self.key}. on: {num_calls+1}')

            self.set_todays_calls(num_calls + 1)

            return retval

        return wrapped_f

    def set_session(self):
        self.session = self.get_session()
        self.dynamodb = self.session.resource('dynamodb')
        self.table = self.dynamodb.Table(config.DYNAMO_TABLE_NAME)

    def dynamodb_key(self):
        return self.key + '-' + dt.utcnow().strftime('%Y%m%d')

    def get_session(self):
        if config.is_debug_server:
            return boto3.Session(profile_name=config.LOCAL_AWS_PROFILE,
                region_name=config.AWS_REGION)
        else:
            return boto3.Session()

    def get_todays_calls(self):
        rsp = self.table.get_item(Key={'pk': self.dynamodb_key()})
        return rsp.get('Item', {}).get('num_calls', 0)

    def set_todays_calls(self, val):
        rsp = self.table.put_item(
            Item={'pk': self.dynamodb_key(),
                  'num_calls': val}
        )

    def notify_admin(self):
        # Send email
        client = self.session.client('ses')
        response = client.send_email(
            Source=EMAIL['from_addr'],
            Destination={
                'ToAddresses': [EMAIL['notification_addr']]
            },
            Message={
                'Subject': {
                    'Data': f'WARNING! Rate limiter for {config.APP_NAME} -- max events reached',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': f'key: {self.key}\n'
                                f'limit: {self.max}\n'
                                f'explanation: \n More than {self.max} {self.key} events have happened today. Either max is too low or someone is attacking you.\n\nNo more {self.key} events will happen today and there will be no errors.\n(It will fail silently.)',
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
