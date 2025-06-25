import time
from starlette.middleware.base import BaseHTTPMiddleware


class LogRequestTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        print(f"{request.method} {request.url.path} completed in {
            duration:.4f}s")

        return response
