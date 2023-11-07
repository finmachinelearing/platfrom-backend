import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_MAX_POOL = int(os.environ.get('DATABASE_MAX_POOL', 5))
DATABASE_MAX_OVERFLOW = int(os.environ.get('DATABASE_MAX_OVERFLOW', 5))

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

MAIL_SSO_CLIENT_ID = os.environ['MAIL_SSO_CLIENT_ID']
MAIL_SSO_CLIENT_SECRET = os.environ['MAIL_SSO_CLIENT_SECRET']
