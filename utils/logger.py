# utils/logger.py

import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with timestamp
log_filename = os.path.join(LOG_DIR, f"sentinelgreen_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configure logger
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    filemode='w'
)

# Global logger instance
logger = logging.getLogger("SentinelGreenLogger")

def log_decision(agent_name: str, input_data: dict, decision: str):
    logger.info(f"[{agent_name}] Input: {input_data} ? Decision: {decision}")