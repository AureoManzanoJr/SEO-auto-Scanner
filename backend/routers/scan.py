"""
Scan router - handles SEO scan requests
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from models.schemas import ScanRequest, ScanResponse, ErrorResponse
from services.scan_service import ScanService

logger = logging.getLogger("seo_scanner")

router = APIRouter()
scan_service = ScanService()


@router.post("/scan", response_model=ScanResponse)
async def scan_url(request: ScanRequest):
    """
    Perform SEO scan of a URL
    
    Args:
        request: ScanRequest with URL and options
        
    Returns:
        ScanResponse with complete SEO analysis
    """
    try:
        url_str = str(request.url)
        result = await scan_service.scan_url(
            url=url_str,
            depth=request.depth or 1,
            include_external=request.include_external or False
        )
        return result
    
    except Exception as e:
        logger.error(f"Error in scan endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error performing SEO scan: {str(e)}"
        )

