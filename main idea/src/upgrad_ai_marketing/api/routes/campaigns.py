"""
Campaign generation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from ...core.config import get_settings, Settings
from ...core.exceptions import BadRequestError, InternalServerError
from ...services.ai_engine import AIContentGenerator
from ...services.market_intelligence import MarketIntelligenceEngine
from ...services.localization import LocalizationEngine
from ...services.ml_optimizer import MLOptimizer

router = APIRouter()
logger = logging.getLogger(__name__)

# Request/Response models
class CampaignRequest(BaseModel):
    course: str
    city: str
    campaign_type: str
    trend_integration: bool = True
    localization: str = "basic"

class CampaignResponse(BaseModel):
    status: str
    data: Dict[str, Any]
    message: str

# Service dependencies
def get_ai_engine():
    return AIContentGenerator()

def get_market_engine():
    return MarketIntelligenceEngine()

def get_localization_engine():
    return LocalizationEngine()

def get_ml_optimizer():
    return MLOptimizer()

@router.post("/generate-campaign", response_model=CampaignResponse)
async def generate_campaign(
    request: CampaignRequest,
    settings: Settings = Depends(get_settings),
    ai_engine: AIContentGenerator = Depends(get_ai_engine),
    market_engine: MarketIntelligenceEngine = Depends(get_market_engine),
    localization_engine: LocalizationEngine = Depends(get_localization_engine),
    ml_optimizer: MLOptimizer = Depends(get_ml_optimizer)
):
    """
    Generate AI-powered marketing campaign
    """

    try:
        logger.info(f"Generating campaign for {request.course} in {request.city}")

        # Validate inputs
        if request.city not in settings.supported_cities:
            raise BadRequestError(f"City '{request.city}' is not supported")

        # Get market data
        market_data = market_engine.get_city_insights(request.city)

        # Get localization context
        local_context = localization_engine.get_city_context(request.city)

        # Generate AI content
        content = await ai_engine.generate_content(
            course=request.course,
            city=request.city,
            campaign_type=request.campaign_type,
            market_data=market_data,
            localization_level=request.localization
        )

        # Get performance predictions
        predictions = ml_optimizer.predict_performance(
            content=content,
            city=request.city,
            course=request.course,
            campaign_type=request.campaign_type
        )

        # Combine results
        campaign_data = {
            "content": content,
            "market_context": market_data,
            "local_context": local_context,
            "predictions": predictions,
            "metadata": {
                "course": request.course,
                "city": request.city,
                "campaign_type": request.campaign_type,
                "localization_level": request.localization,
                "trend_integration": request.trend_integration
            }
        }

        return CampaignResponse(
            status="success",
            data=campaign_data,
            message="Campaign generated successfully"
        )

    except BadRequestError:
        raise
    except Exception as e:
        logger.error(f"Error generating campaign: {e}", exc_info=True)
        raise InternalServerError(f"Failed to generate campaign: {str(e)}")

@router.get("/campaign-templates")
async def get_campaign_templates():
    """Get available campaign templates"""

    templates = {
        "email": {
            "name": "Email Campaign",
            "description": "Personalized email marketing campaigns",
            "fields": ["subject", "body", "cta"]
        },
        "social": {
            "name": "Social Media Campaign",
            "description": "Social media posts and ads",
            "fields": ["post_text", "hashtags", "image_prompt"]
        },
        "display": {
            "name": "Display Advertising",
            "description": "Banner and display ad campaigns",
            "fields": ["headline", "description", "image_prompt"]
        }
    }

    return {
        "status": "success",
        "data": templates,
        "message": "Campaign templates retrieved successfully"
    }

@router.get("/supported-courses")
async def get_supported_courses():
    """Get list of supported courses"""

    courses = [
        "AI/ML",
        "Data Science",
        "Digital Marketing",
        "Product Management",
        "Software Development",
        "Cloud Computing",
        "Cybersecurity",
        "Business Analytics"
    ]

    return {
        "status": "success",
        "data": courses,
        "message": "Supported courses retrieved successfully"
    }

@router.get("/supported-cities")
async def get_supported_cities(settings: Settings = Depends(get_settings)):
    """Get list of supported cities"""

    return {
        "status": "success",
        "data": settings.supported_cities,
        "message": "Supported cities retrieved successfully"
    }