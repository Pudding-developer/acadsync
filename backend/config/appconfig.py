from dotenv import load_dotenv
import os

load_dotenv()

SQLITE_PATH = os.environ.get("SQLITE_PATH")
API_TOKEN_ASSIGNMENT_PATH = os.environ.get("API_TOKEN_ASSIGNMENT_PATH")
