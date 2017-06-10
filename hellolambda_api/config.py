from pathlib import Path

FLASK_PORT = 5285
ROOT_API_AWS = 'https://xxx.execute-api.us-west-2.amazonaws.com/dev'
ROOT_API_FLASK = f'http://localhost:{FLASK_PORT}'
LOCAL_AWS_PROFILE = 'hellolambda'
AWS_REGION = 'us-west-2'
APP_NAME = 'hellolambda'

TEST_PATH_PREFIX = '/test'

ROOTP = Path(__file__).parent.parent
SITE_ASSETS_DIR = ROOTP / 'hellolambdaapi/assets'

EMAIL = {
    'notification_addr': 'test@gmail.com',
    'from_addr': 'test2@gmail.com',
    'feedback_subject': 'Hellolambda Form Content'
}

DYNAMO_TABLE_NAME = 'hellolambda'


# Event limiter
MAX_DYNAMO_PER_DAY = 2000
MAX_EMAIL_PER_DAY = 100

# Global - Ugly but easy, and easier than flask.g
is_debug_server = None

#
# This is I can test my code while still having a clean config file.
# You can ignore it.
#
try:
    from private_config import *
except ImportError:
    pass
