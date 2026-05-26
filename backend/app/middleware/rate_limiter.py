import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.redis_service import get_redis

RATE_LIMIT = 100       # max requests
WINDOW_SECONDS = 60    # per 60 seconds


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for docs
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = int(time.time())
        window_key = f"rate_limit:{client_ip}:{current_time // WINDOW_SECONDS}"

        try:
            redis = await get_redis()
            count = await redis.incr(window_key)
            if count == 1:
                await redis.expire(window_key, WINDOW_SECONDS)

            remaining = max(0, RATE_LIMIT - count)

            if count > RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={
                        "status": "error",
                        "code": 429,
                        "message": "Too many requests. Please slow down.",
                        "retry_after": WINDOW_SECONDS
                    },
                    headers={
                        "X-RateLimit-Limit": str(RATE_LIMIT),
                        "X-RateLimit-Remaining": "0",
                        "Retry-After": str(WINDOW_SECONDS)
                    }
                )

            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            return response

        except Exception:
            # If Redis is down, don't block requests
            return await call_next(request)