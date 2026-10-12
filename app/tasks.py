# import time
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# def generate_user_report(user_email: str):
#     """
#     This runs inside the separate worker process, completely separate from FastAPI!
#     """
#     logger.info(f"--- WORKER START --- Generating report for: {user_email}")
#     time.sleep(3)  # Simulates heavy background work
#     logger.info(f"--- WORKER COMPLETE --- Report successfully generated for: {user_email}")
import time
import logging

logger = logging.getLogger(__name__)


def generate_user_report(user_email: str):
    """
    Background worker job with full lifecycle tracking and error logging.
    """
    logger.info(f"JOB_START | Event: worker_picked_up_job | User: {user_email}")

    try:
        # Simulate heavy lifting
        time.sleep(3)

        # Simulate an occasional edge-case error for testing error logs
        if user_email == "error@gmail.com":
            raise ValueError("Failed to connect to external report generation API")

        logger.info(f"JOB_SUCCESS | Event: report_generated_successfully | User: {user_email}")

    except Exception as e:
        logger.error(f"JOB_FAILURE | Event: task_failed | User: {user_email} | Error: {str(e)}")
        # Re-raise so RQ knows the job failed
        raise e