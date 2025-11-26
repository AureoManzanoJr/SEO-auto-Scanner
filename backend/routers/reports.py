"""
Reports router - handles report generation
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from typing import Optional
import logging
from pathlib import Path
import tempfile

from services.scan_service import ScanService
from services.report_service import ReportService

logger = logging.getLogger("seo_scanner")

router = APIRouter()
scan_service = ScanService()
report_service = ReportService()


@router.get("/report/html")
async def get_html_report(url: str = Query(..., description="URL to generate report for")):
    """
    Generate HTML report for a URL
    
    Args:
        url: URL to analyze
        
    Returns:
        HTML report
    """
    try:
        # Perform scan
        scan_result = await scan_service.scan_url(url)
        
        # Generate HTML report
        html_content = report_service.generate_html(scan_result)
        
        return HTMLResponse(content=html_content)
    
    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating HTML report: {str(e)}"
        )


@router.get("/report/pdf")
async def get_pdf_report(url: str = Query(..., description="URL to generate report for")):
    """
    Generate PDF report for a URL
    
    Args:
        url: URL to analyze
        
    Returns:
        PDF file
    """
    try:
        # Perform scan
        scan_result = await scan_service.scan_url(url)
        
        # Generate PDF report
        pdf_path = report_service.generate_pdf(scan_result)
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"seo-report-{url.replace('https://', '').replace('http://', '').replace('/', '-')}.pdf"
        )
    
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF report: {str(e)}"
        )


@router.get("/report/json")
async def get_json_report(url: str = Query(..., description="URL to generate report for")):
    """
    Get JSON report for a URL
    
    Args:
        url: URL to analyze
        
    Returns:
        JSON scan result
    """
    try:
        scan_result = await scan_service.scan_url(url)
        return scan_result
    
    except Exception as e:
        logger.error(f"Error generating JSON report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating JSON report: {str(e)}"
        )

