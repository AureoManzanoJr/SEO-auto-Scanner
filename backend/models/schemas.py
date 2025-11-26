"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional
from datetime import datetime


class ScanRequest(BaseModel):
    """Request model for scan endpoint"""
    url: HttpUrl = Field(..., description="URL to analyze")
    depth: Optional[int] = Field(1, ge=1, le=3, description="Crawl depth (1-3)")
    include_external: Optional[bool] = Field(False, description="Include external links analysis")


class Metadata(BaseModel):
    """Page metadata"""
    title: Optional[str] = None
    description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    twitter_card: Optional[str] = None
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None
    canonical: Optional[str] = None
    lang: Optional[str] = None


class Headings(BaseModel):
    """Headings structure"""
    h1: List[str] = []
    h2: List[str] = []
    h3: List[str] = []
    h4: List[str] = []
    h5: List[str] = []
    h6: List[str] = []


class Links(BaseModel):
    """Links analysis"""
    internal: List[str] = []
    external: List[str] = []
    broken: List[Dict[str, str]] = []
    total: int = 0


class ImageInfo(BaseModel):
    """Image information"""
    src: str
    alt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class Images(BaseModel):
    """Images analysis"""
    total: int = 0
    without_alt: int = 0
    list: List[ImageInfo] = []


class Performance(BaseModel):
    """Performance metrics"""
    load_time: float
    dom_content_loaded: Optional[float] = None
    first_contentful_paint: Optional[float] = None
    largest_contentful_paint: Optional[float] = None
    time_to_interactive: Optional[float] = None
    total_blocking_time: Optional[float] = None
    cumulative_layout_shift: Optional[float] = None


class Keywords(BaseModel):
    """Keywords analysis"""
    density: Dict[str, float] = {}
    top_keywords: List[Dict[str, any]] = []


class ScanResponse(BaseModel):
    """Response model for scan endpoint"""
    url: str
    timestamp: datetime
    score: int = Field(..., ge=0, le=100, description="SEO score (0-100)")
    metadata: Metadata
    headings: Headings
    links: Links
    images: Images
    performance: Optional[Performance] = None
    keywords: Keywords
    mobile_friendly: bool = False
    sitemap: Optional[str] = None
    robots_txt: Optional[str] = None
    errors: List[str] = []


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

