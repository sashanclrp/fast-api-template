import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mode = os.getenv("MODE", "PROD")

# MODE CREDENTIALS
if mode == "DEV":
    CORS_ALLOW_ALL = True
else:
    CORS_ALLOW_ALL = False
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")

# GENERAL CONFIGURATION
PORT = int(os.getenv("PORT", 5000))

# LOGGING CONFIGURATION
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")  

# WEBHOOK CONFIGURATION
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")

# Validation
REQUIRED_ENV_VARS = [
    "PORT",
    "LOG_LEVEL",
    "WEBHOOK_VERIFY_TOKEN"
]

for var in REQUIRED_ENV_VARS:
    if not locals()[var]:
        raise EnvironmentError(f"Missing required environment variable: {var}")