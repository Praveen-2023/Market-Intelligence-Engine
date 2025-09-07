"""
Middleware setup for the FastAPI application
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from typing import Callable

from ..core.config import Settings

logger = logging.getLogger(__name__)

def setup_middleware(app: FastAPI, settings: Settings):
    """Setup all middleware for the application"""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Trusted host middleware (for production)
    if not settings.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
        )

    # Custom middleware
    app.middleware("http")(log_requests)
    app.middleware("http")(add_security_headers)

async def log_requests(request: Request, call_next: Callable) -> Response:
    """Log all requests with timing"""

    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        f"Response: {response.status_code} - "
        f"Time: {process_time:.3f}s - "
        f"Path: {request.url.path}"
    )

    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)

    return response

async def add_security_headers(request: Request, call_next: Callable) -> Response:
    """Add security headers to all responses"""

    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # API identification
    response.headers["X-API-Version"] = "1.0.0"
    response.headers["X-Powered-By"] = "upGrad AI Marketing Automation"

    return response