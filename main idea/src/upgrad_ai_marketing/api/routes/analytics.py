"""
Analytics endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/performance-analytics")
async def get_performance_analytics():
    """Get performance analytics data"""
    return {
        "status": "success",
        "data": {"message": "Analytics endpoint working"},
        "message": "Analytics retrieved successfully"
    }