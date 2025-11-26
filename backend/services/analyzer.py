"""
SEO analyzer service
"""

from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging
import re
from urllib.parse import urljoin, urlparse
from collections import Counter
import requests

from models.schemas import Metadata, Headings, Links, Images, ImageInfo, Performance, Keywords

logger = logging.getLogger("seo_scanner")


class SEOAnalyzer:
    """SEO analysis service"""
    
    def __init__(self, base_url: str):
        """
        Initialize analyzer
        
        Args:
            base_url: Base URL of the page being analyzed
        """
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
    
    def analyze_metadata(self, soup: BeautifulSoup) -> Metadata:
        """
        Analyze page metadata
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Metadata object
        """
        metadata = Metadata()
        
        # Title
        title_tag = soup.find("title")
        if title_tag:
            metadata.title = title_tag.get_text(strip=True)
        
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            metadata.description = meta_desc["content"]
        
        # Open Graph
        og_title = soup.find("meta", property="og:title")
        if og_title:
            metadata.og_title = og_title.get("content")
        
        og_desc = soup.find("meta", property="og:description")
        if og_desc:
            metadata.og_description = og_desc.get("content")
        
        og_image = soup.find("meta", property="og:image")
        if og_image:
            metadata.og_image = og_image.get("content")
        
        # Twitter Cards
        twitter_card = soup.find("meta", attrs={"name": "twitter:card"})
        if twitter_card:
            metadata.twitter_card = twitter_card.get("content")
        
        twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
        if twitter_title:
            metadata.twitter_title = twitter_title.get("content")
        
        twitter_desc = soup.find("meta", attrs={"name": "twitter:description"})
        if twitter_desc:
            metadata.twitter_description = twitter_desc.get("content")
        
        # Canonical
        canonical = soup.find("link", rel="canonical")
        if canonical:
            metadata.canonical = canonical.get("href")
        
        # Language
        html_tag = soup.find("html")
        if html_tag:
            metadata.lang = html_tag.get("lang")
        
        return metadata
    
    def analyze_headings(self, soup: BeautifulSoup) -> Headings:
        """
        Analyze heading structure
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Headings object
        """
        headings = Headings()
        
        for level in range(1, 7):
            heading_tags = soup.find_all(f"h{level}")
            headings_list = [h.get_text(strip=True) for h in heading_tags if h.get_text(strip=True)]
            setattr(headings, f"h{level}", headings_list)
        
        return headings
    
    def analyze_images(self, soup: BeautifulSoup) -> Images:
        """
        Analyze images on the page
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Images object
        """
        images_list = []
        without_alt_count = 0
        
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or ""
            
            # Resolve relative URLs
            if src:
                src = urljoin(self.base_url, src)
            
            alt = img.get("alt", "")
            width = img.get("width")
            height = img.get("height")
            
            # Try to get dimensions from attributes or convert to int
            try:
                width = int(width) if width else None
            except (ValueError, TypeError):
                width = None
            
            try:
                height = int(height) if height else None
            except (ValueError, TypeError):
                height = None
            
            if not alt:
                without_alt_count += 1
            
            images_list.append(ImageInfo(
                src=src,
                alt=alt,
                width=width,
                height=height
            ))
        
        return Images(
            total=len(images_list),
            without_alt=without_alt_count,
            list=images_list
        )
    
    def analyze_keywords(self, soup: BeautifulSoup, metadata: Metadata) -> Keywords:
        """
        Analyze keyword density
        
        Args:
            soup: BeautifulSoup object
            metadata: Metadata object
            
        Returns:
            Keywords object
        """
        # Get all text content
        text_content = soup.get_text()
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get clean text
        text = soup.get_text()
        
        # Extract words (alphanumeric, at least 3 characters)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Count word frequency
        word_count = Counter(words)
        total_words = len(words)
        
        # Calculate density
        density = {}
        top_keywords = []
        
        if total_words > 0:
            for word, count in word_count.most_common(20):
                density[word] = (count / total_words) * 100
                top_keywords.append({
                    "word": word,
                    "count": count,
                    "density": density[word]
                })
        
        return Keywords(
            density=density,
            top_keywords=top_keywords
        )
    
    def check_sitemap(self) -> Optional[str]:
        """
        Check for sitemap.xml
        
        Returns:
            Sitemap URL if found, None otherwise
        """
        sitemap_urls = [
            urljoin(self.base_url, "/sitemap.xml"),
            urljoin(self.base_url, "/sitemap_index.xml"),
        ]
        
        for sitemap_url in sitemap_urls:
            try:
                response = requests.head(sitemap_url, timeout=5)
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    if "xml" in content_type.lower():
                        return sitemap_url
            except Exception:
                continue
        
        return None
    
    def check_robots_txt(self) -> Optional[str]:
        """
        Check for robots.txt
        
        Returns:
            Robots.txt URL if found, None otherwise
        """
        robots_url = urljoin(self.base_url, "/robots.txt")
        
        try:
            response = requests.head(robots_url, timeout=5)
            if response.status_code == 200:
                return robots_url
        except Exception:
            pass
        
        return None
    
    def check_mobile_friendly(self, soup: BeautifulSoup) -> bool:
        """
        Check if page is mobile-friendly
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            True if mobile-friendly, False otherwise
        """
        # Check viewport meta tag
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if not viewport:
            return False
        
        viewport_content = viewport.get("content", "").lower()
        
        # Check for responsive design indicators
        has_viewport = "width" in viewport_content
        has_initial_scale = "initial-scale" in viewport_content
        
        # Check for responsive CSS classes (common frameworks)
        responsive_indicators = [
            soup.find(class_=re.compile(r"container|responsive|mobile", re.I)),
            soup.find(attrs={"class": re.compile(r"col-|grid", re.I)})
        ]
        
        has_responsive_classes = any(responsive_indicators)
        
        return has_viewport and (has_initial_scale or has_responsive_classes)
    
    def calculate_seo_score(
        self,
        metadata: Metadata,
        headings: Headings,
        images: Images,
        links: Links,
        mobile_friendly: bool,
        performance: Optional[Performance] = None
    ) -> int:
        """
        Calculate overall SEO score (0-100)
        
        Args:
            metadata: Metadata object
            headings: Headings object
            images: Images object
            links: Links object
            mobile_friendly: Mobile-friendly flag
            performance: Performance metrics (optional)
            
        Returns:
            SEO score (0-100)
        """
        score = 0
        max_score = 100
        
        # Title (10 points)
        if metadata.title:
            if 30 <= len(metadata.title) <= 60:
                score += 10
            elif len(metadata.title) > 0:
                score += 5
        
        # Description (10 points)
        if metadata.description:
            if 120 <= len(metadata.description) <= 160:
                score += 10
            elif len(metadata.description) > 0:
                score += 5
        
        # H1 (10 points)
        if len(headings.h1) == 1:
            score += 10
        elif len(headings.h1) > 1:
            score += 5
        
        # Headings structure (10 points)
        if headings.h1 and headings.h2:
            score += 10
        elif headings.h1 or headings.h2:
            score += 5
        
        # Images with ALT (10 points)
        if images.total > 0:
            alt_ratio = (images.total - images.without_alt) / images.total
            score += int(10 * alt_ratio)
        
        # Links (10 points)
        if links.total > 0:
            broken_ratio = len(links.broken) / links.total if links.total > 0 else 0
            score += int(10 * (1 - broken_ratio))
        
        # Mobile-friendly (10 points)
        if mobile_friendly:
            score += 10
        
        # Performance (20 points)
        if performance:
            if performance.load_time < 2.0:
                score += 20
            elif performance.load_time < 3.0:
                score += 15
            elif performance.load_time < 5.0:
                score += 10
            else:
                score += 5
        
        # Sitemap and Robots.txt (10 points)
        # This will be checked separately in the scan service
        
        return min(score, max_score)

