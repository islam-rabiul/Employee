import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_user_report(user_email: str):
    """
    This runs inside the separate worker process, completely separate from FastAPI!
    """
    logger.info(f"--- WORKER START --- Generating report for: {user_email}")
    time.sleep(3)  # Simulates heavy background work
    logger.info(f"--- WORKER COMPLETE --- Report successfully generated for: {user_email}")