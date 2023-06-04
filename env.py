import os
import dotenv

dotenv.load_dotenv()

PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')
PROXY_USERNAME = os.environ.get('PROXY_USERNAME')
