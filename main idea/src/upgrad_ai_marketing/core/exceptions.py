"""
Custom exceptions for upGrad AI Marketing Automation
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class BaseUpGradException(Exception):
    """Base exception for all upGrad AI Marketing exceptions"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class APIException(BaseUpGradException):
    """Base API exception"""

    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        super().__init__(message, details)


class AIServiceException(BaseUpGradException):
    """Exception for AI service errors"""
    pass


class MarketIntelligenceException(BaseUpGradException):
    """Exception for market intelligence errors"""
    pass


class CampaignGenerationException(BaseUpGradException):
    """Exception for campaign generation errors"""
    pass


class ValidationException(BaseUpGradException):
    """Exception for validation errors"""
    pass


class ConfigurationException(BaseUpGradException):
    """Exception for configuration errors"""
    pass


# HTTP Exception handlers
def create_http_exception(
    status_code: int,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized HTTP exception"""
    return HTTPException(
        status_code=status_code,
        detail={
            "error": message,
            "details": details or {},
            "status_code": status_code
        }
    )


# Common HTTP exceptions
class NotFoundError(HTTPException):
    def __init__(self, resource: str, identifier: str = ""):
        detail = f"{resource} not found"
        if identifier:
            detail += f": {identifier}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class UnauthorizedError(HTTPException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class ForbiddenError(HTTPException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class InternalServerError(HTTPException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


class ServiceUnavailableError(HTTPException):
    def __init__(self, service: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{service} service is currently unavailable"
        )