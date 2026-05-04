import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int, window: int):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Clean old requests
        self.requests[client_ip] = [req for req in self.requests[client_ip] if now - req < self.window]

        if len(self.requests[client_ip]) >= self.limit:
            raise HTTPException(status_code=429, detail="Too many requests")

        self.requests[client_ip].append(now)
        return await call_next(request)
