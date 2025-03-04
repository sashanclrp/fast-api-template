import logging
import sys
import os
from datetime import datetime
import warnings

from config.env import LOG_LEVEL
warnings.filterwarnings('ignore', message='NumExpr defaulting to.*')

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

if LOG_LEVEL == "INFO":
    level = logging.INFO
elif LOG_LEVEL == "DEBUG":
    level = logging.DEBUG
else:
    level = logging.DEBUG

# Configure Logging
logging.basicConfig(
    level=level,  # Set to DEBUG for development, set to INFO for production
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(logs_dir, f'webhook_{datetime.now().strftime("%Y%m%d")}.log'))
    ]
)

logger = logging.getLogger("whatsapp_api")

# Example usage:
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.debug("Debug message")