import logging
import sys
import os
from datetime import datetime
import warnings

from config.env import LOG_LEVEL, MODE
warnings.filterwarnings('ignore', message='NumExpr defaulting to.*')

# Configure log level
if LOG_LEVEL == "INFO":
    level = logging.INFO
elif LOG_LEVEL == "DEBUG":
    level = logging.DEBUG
else:
    level = logging.DEBUG

# Default handlers - always use StreamHandler
handlers = [logging.StreamHandler(sys.stdout)]

# Add FileHandler only in development mode
if MODE == "DEV":
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    handlers.append(logging.FileHandler(os.path.join(logs_dir, f'webhook_{datetime.now().strftime("%Y%m%d")}.log')))

# Configure Logging
logging.basicConfig(
    level=level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger("fastapi_template")

# Example usage:
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.debug("Debug message")