import os
import logging
import httpx
from config.env import settings

# Setup logging to see pings in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ping_self():
    """Function that requests the root URL to keep the container awake."""
    app_url = settings.APP_URL
    if not app_url:
        logger.warning("APP_URL is not set. Self-ping skipped.")
        return

    try:
        # Use a sync client inside the background thread
        with httpx.Client() as client:
            response = client.get(app_url + "/hello")
            logger.info(f"Self-ping successful: Status {response.status_code}")
    except Exception as e:
        logger.error(f"Self-ping failed: {e}")
