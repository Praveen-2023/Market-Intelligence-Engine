"""
Market intelligence endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/market-intelligence")
async def get_market_intelligence():
    """Get market intelligence data"""
    return {
        "status": "success",
        "data": {"message": "Market intelligence endpoint working"},
        "message": "Market intelligence retrieved successfully"
    }