import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REGISTER_HANDLER_API_KEY = os.getenv("REGISTER_HANDLER_API_KEY")
DRIVE_API_SERVICE_ACCOUNT_FILE = os.getenv("DRIVE_API_SERVICE_ACCOUNT_FILE")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")