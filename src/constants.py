import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')