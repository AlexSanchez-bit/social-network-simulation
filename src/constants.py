import os
from dotenv import load_dotenv

load_dotenv()

VOYAGE_EMBED_BATCH_SIZE = 128
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
VOYAGE_API_KEY = os.environ.get('VOYAGE_API_KEY')