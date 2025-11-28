import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REGISTER_HANDLER_API_KEY = os.getenv("REGISTER_HANDLER_API_KEY")