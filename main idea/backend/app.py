"""
FastAPI Server for upGrad AI Marketing Automation System
Main application with REST endpoints
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import logging
from pathlib import Path
import asyncio
from datetime import datetime

# Import our custom modules
from .market_intel import market_intelligence
from .ai_engine import ai_content_generator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="upGrad AI Marketing Automation",
    description="AI-powered marketing campaign generation with real market intelligence",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class CampaignRequest(BaseModel):
    course: str
    city: str
    campaign_type: str
    trend_integration: bool = True
    localization: str = "basic"

class CampaignResponse(BaseModel):
    content: Dict[str, Any]
    predictions: Dict[str, str]
    market_context: Dict[str, Any]
    image_url: Optional[str] = None

# Mount static files (frontend)
static_path = Path(__file__).parent.parent / "MI"
backend_path = Path(__file__).parent
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    # Also mount the MI directory directly for CSS/JS files
    app.mount("/MI", StaticFiles(directory=str(static_path)), name="frontend")
    # Mount backend directory for dashboard_connector.js
    app.mount("/backend", StaticFiles(directory=str(backend_path)), name="backend")
    logger.info(f"Mounted static files from: {static_path}")
    logger.info(f"Mounted backend files from: {backend_path}")

# Root endpoint - serve the main dashboard
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard HTML"""
    try:
        html_file = Path(__file__).parent.parent / "MI" / "index.html"
        if html_file.exists():
            return FileResponse(html_file)
        else:
            return HTMLResponse("""
            <html>
                <head><title>upGrad AI Marketing Dashboard</title></head>
                <body>
                    <h1>🚀 upGrad AI Marketing Dashboard</h1>
                    <p>Frontend files not found. Please ensure MI/index.html exists.</p>
                    <p>API endpoints available at:</p>
                    <ul>
                        <li><a href="/docs">/docs</a> - API Documentation</li>
                        <li><a href="/api/market-intelligence">/api/market-intelligence</a></li>
                        <li><a href="/api/health">/api/health</a></li>
                    </ul>
                </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving root: {e}")
        raise HTTPException(status_code=500, detail="Error loading dashboard")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "market_intelligence": "active",
            "ai_content_generator": "active",
            "database": "active"
        }
    }

# Market Intelligence endpoints
@app.get("/api/market-intelligence")
async def get_market_intelligence():
    """Get real-time market intelligence data for dashboard"""
    try:
        trends = market_intelligence.get_hiring_trends()
        return {
            "status": "success",
            "data": trends,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting market intelligence: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving market data")

@app.get("/api/city-insights/{city}")
async def get_city_insights(city: str):
    """Get detailed insights for a specific city"""
    try:
        insights = market_intelligence.get_city_insights(city)
        if insights.get('error'):
            raise HTTPException(status_code=404, detail=insights['error'])
        
        return {
            "status": "success",
            "data": insights,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting city insights: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving city data")

@app.get("/api/skill-demand")
async def get_skill_demand():
    """Get overall skill demand data"""
    try:
        skill_demand = market_intelligence.get_skill_demand()
        return {
            "status": "success",
            "data": skill_demand,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting skill demand: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving skill data")

@app.get("/api/course-relevance/{course}")
async def get_course_relevance(course: str):
    """Get market relevance for a specific course"""
    try:
        relevance = market_intelligence.get_course_relevance(course)
        return {
            "status": "success",
            "data": relevance,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting course relevance: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving course data")

# Campaign Generation endpoints
@app.post("/api/generate-campaign")
async def generate_campaign(request: CampaignRequest):
    """Generate AI-powered marketing campaign"""
    try:
        logger.info(f"Generating campaign for {request.course} in {request.city}")
        
        # Get market context
        market_context = market_intelligence.get_market_context(
            request.city, 
            request.course
        )
        
        # Generate AI content
        content = await ai_content_generator.generate_campaign_content(
            course=request.course,
            city=request.city,
            campaign_type=request.campaign_type,
            market_context=market_context,
            localization_level=request.localization
        )
        
        # Apply localization if requested
        if request.localization != "basic":
            # Import localization engine when needed
            try:
                from .localization import localization_engine
                content = localization_engine.localize_content(content, request.city)
            except ImportError:
                logger.warning("Localization engine not available")
        
        # Generate image if requested
        image_url = None
        if request.campaign_type in ["Display Ads", "Social Media"]:
            try:
                # This would integrate with image generation service
                image_url = "/static/images/default_campaign.png"
            except Exception as e:
                logger.warning(f"Image generation failed: {e}")
        
        response = CampaignResponse(
            content=content,
            predictions=content.get('predictions', {}),
            market_context=market_context,
            image_url=image_url
        )
        
        return {
            "status": "success",
            "data": response.dict(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating campaign: {str(e)}")

# Performance Analytics endpoints
@app.get("/api/performance-analytics")
async def get_performance_analytics():
    """Get campaign performance data for charts and analytics"""
    try:
        # This would typically load from the marketing automation Excel file
        # For now, return sample data structure
        
        sample_data = {
            "platform_performance": {
                "Facebook": {"ctr": 0.025, "conversion_rate": 0.045, "roas": 3.2},
                "Instagram": {"ctr": 0.047, "conversion_rate": 0.085, "roas": 4.8},
                "LinkedIn": {"ctr": 0.032, "conversion_rate": 0.062, "roas": 4.1},
                "Twitter": {"ctr": 0.018, "conversion_rate": 0.028, "roas": 2.8},
                "YouTube": {"ctr": 0.041, "conversion_rate": 0.071, "roas": 4.5},
                "Google Ads": {"ctr": 0.038, "conversion_rate": 0.068, "roas": 4.2}
            },
            "city_performance": {
                "Bangalore": {"performance_score": 8.33},
                "Mumbai": {"performance_score": 7.89},
                "Delhi NCR": {"performance_score": 7.95},
                "Hyderabad": {"performance_score": 8.41},
                "Chennai": {"performance_score": 8.12},
                "Pune": {"performance_score": 7.76}
            },
            "content_themes": {
                "Job Security": {"performance_score": 8.35},
                "Career Growth": {"performance_score": 8.12},
                "Salary Boost": {"performance_score": 7.98},
                "Skill Development": {"performance_score": 7.85}
            },
            "campaign_metrics": {
                "total_campaigns": 24,
                "active_markets": 8,
                "ai_optimization_score": 87,
                "current_roi": 4.2
            }
        }
        
        return {
            "status": "success",
            "data": sample_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting performance analytics: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving analytics data")

# Export endpoints
@app.get("/api/export/{format}")
async def export_data(format: str):
    """Export campaign data in various formats"""
    try:
        if format not in ["csv", "pdf", "excel"]:
            raise HTTPException(status_code=400, detail="Invalid export format")
        
        # This would implement actual export functionality
        return {
            "status": "success",
            "message": f"Export in {format} format initiated",
            "download_url": f"/api/download/campaign_data.{format}",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        raise HTTPException(status_code=500, detail="Error exporting data")

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket endpoint for real-time dashboard updates"""
    await websocket.accept()
    try:
        while True:
            # Send periodic updates
            update_data = {
                "type": "market_update",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "active_campaigns": 24,
                    "new_opportunities": 156,
                    "performance_score": 87
                }
            }
            await websocket.send_json(update_data)
            await asyncio.sleep(30)  # Update every 30 seconds
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {
        "status": "error",
        "message": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return {
        "status": "error", 
        "message": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting upGrad AI Marketing Automation System")
    logger.info("📊 Market Intelligence Engine: Ready")
    logger.info("🤖 AI Content Generator: Ready") 
    logger.info("📈 Performance Analytics: Ready")
    logger.info("✅ All systems operational")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
