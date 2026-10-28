import time
import logging
from fastapi import Request

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def request_logging(request: Request, call_next):

    start_time = time.perf_counter()

    logger.info(f"Request Method: {request.method}")
    logger.info(f"Request URL: {request.url.path}")

    response = await call_next(request)

    execution_time = time.perf_counter() - start_time

    logger.info(f"Response Status: {response.status_code}")
    logger.info(f"Execution Time: {execution_time:.4f} seconds")

    response.headers["X-Process-Time"] = str(round(execution_time, 4))

    return response
