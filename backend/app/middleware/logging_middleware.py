import time
import logging
import os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)

logger = logging.getLogger("student_management_system")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        query = str(request.query_params) if request.query_params else ""

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)
        status_code = response.status_code

        log_message = (
            f"IP: {client_ip} | "
            f"Method: {method} | "
            f"Path: {path} | "
            f"Query: {query} | "
            f"Status: {status_code} | "
            f"Duration: {process_time}ms"
        )

        if status_code >= 500:
            logger.error(log_message)
        elif status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        response.headers["X-Process-Time"] = f"{process_time}ms"
        return response
