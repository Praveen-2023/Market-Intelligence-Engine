"""
FastAPI Application Factory for upGrad AI Marketing Automation
Industry-standard application structure with proper error handling
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from pathlib import Path

from .core.config import get_settings
from .core.exceptions import create_http_exception
from .api.routes import health, campaigns, analytics, market_intel
from .api.middleware import setup_middleware


def create_app() -> FastAPI:
    """Application factory pattern"""
    
    # Get settings
    settings = get_settings()
    
    # Create FastAPI app
    app = FastAPI(
        title="upGrad AI Marketing Automation",
        description="AI-powered marketing campaign generation with real market intelligence",
        version="1.0.0",
        debug=settings.debug
    )
    
    # Setup middleware
    setup_middleware(app, settings)
    
    # Include routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(campaigns.router, prefix="/api", tags=["campaigns"])
    app.include_router(analytics.router, prefix="/api", tags=["analytics"])
    app.include_router(market_intel.router, prefix="/api", tags=["market-intelligence"])
    
    # Mount static files
    setup_static_files(app, settings)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Root endpoint
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the main dashboard"""
        template_path = settings.templates_dir / "index.html"
        if template_path.exists():
            return HTMLResponse(content=template_path.read_text(), status_code=200)
        return HTMLResponse(content="<h1>upGrad AI Marketing Dashboard</h1><p>Template not found</p>")
    
    return app


def setup_static_files(app: FastAPI, settings):
    """Setup static file serving"""
    
    # Mount frontend static files
    if settings.static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
        
        # Mount CSS and JS directories directly for easier access
        css_dir = settings.static_dir / "css"
        js_dir = settings.static_dir / "js"
        
        if css_dir.exists():
            app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
        if js_dir.exists():
            app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    
    # Mount templates directory
    if settings.templates_dir.exists():
        app.mount("/templates", StaticFiles(directory=str(settings.templates_dir)), name="templates")


def setup_exception_handlers(app: FastAPI):
    """Setup global exception handlers"""
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions"""
        return create_http_exception(
            status_code=exc.status_code,
            message=str(exc.detail),
            details={"path": str(request.url.path)}
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors"""
        return create_http_exception(
            status_code=422,
            message="Validation error",
            details={
                "errors": exc.errors(),
                "body": exc.body if hasattr(exc, 'body') else None
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logging.error(f"Unhandled exception: {exc}", exc_info=True)
        return create_http_exception(
            status_code=500,
            message="Internal server error",
            details={"path": str(request.url.path)}
        )


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "src.upgrad_ai_marketing.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
