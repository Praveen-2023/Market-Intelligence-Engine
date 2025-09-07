"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
import asyncio
from datetime import datetime

from ...core.config import get_settings, Settings
from ...services.ai_engine import AIContentGenerator
from ...services.market_intelligence import MarketIntelligenceEngine

router = APIRouter()

# Initialize services (will be dependency injected in production)
ai_engine = None
market_engine = None

def get_ai_engine():
    global ai_engine
    if ai_engine is None:
        ai_engine = AIContentGenerator()
    return ai_engine

def get_market_engine():
    global market_engine
    if market_engine is None:
        market_engine = MarketIntelligenceEngine()
    return market_engine

@router.get("/health")
async def health_check(
    settings: Settings = Depends(get_settings),
    ai_service: AIContentGenerator = Depends(get_ai_engine),
    market_service: MarketIntelligenceEngine = Depends(get_market_engine)
) -> Dict[str, Any]:
    """
    Comprehensive health check for all services
    """

    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {}
    }

    # Check AI service
    try:
        ai_status = await check_ai_service(ai_service)
        health_status["services"]["ai_engine"] = ai_status
    except Exception as e:
        health_status["services"]["ai_engine"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"

    # Check market intelligence service
    try:
        market_status = await check_market_service(market_service)
        health_status["services"]["market_intelligence"] = market_status
    except Exception as e:
        health_status["services"]["market_intelligence"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"

    # Check configuration
    config_status = check_configuration(settings)
    health_status["services"]["configuration"] = config_status

    if config_status["status"] == "unhealthy":
        health_status["status"] = "degraded"

    return health_status

async def check_ai_service(ai_service: AIContentGenerator) -> Dict[str, Any]:
    """Check AI service health"""

    try:
        # Test basic functionality
        test_result = await ai_service.generate_content(
            course="Test",
            city="Test",
            campaign_type="email",
            market_data={"test": True},
            localization_level="basic"
        )

        return {
            "status": "healthy",
            "gemini_api": "connected" if ai_service.model else "fallback",
            "last_check": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.utcnow().isoformat()
        }

async def check_market_service(market_service: MarketIntelligenceEngine) -> Dict[str, Any]:
    """Check market intelligence service health"""

    try:
        # Test data loading
        data = market_service.get_market_overview()

        return {
            "status": "healthy",
            "data_loaded": len(data.get("city_performance", {})) > 0,
            "cities_available": len(data.get("city_performance", {})),
            "last_check": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.utcnow().isoformat()
        }

def check_configuration(settings: Settings) -> Dict[str, Any]:
    """Check configuration health"""

    issues = []

    # Check API keys
    if not settings.gemini_api_key:
        issues.append("Missing Gemini API key")

    if not settings.stability_api_key:
        issues.append("Missing Stability API key")

    # Check paths
    if not settings.data_dir.exists():
        issues.append("Data directory not found")

    if not settings.static_dir.exists():
        issues.append("Static directory not found")

    return {
        "status": "healthy" if not issues else "unhealthy",
        "issues": issues,
        "api_keys_configured": bool(settings.gemini_api_key and settings.stability_api_key),
        "last_check": datetime.utcnow().isoformat()
    }