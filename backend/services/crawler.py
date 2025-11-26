"""
Web crawler service using Playwright
"""

from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import logging
from urllib.parse import urljoin, urlparse
import asyncio

logger = logging.getLogger("seo_scanner")


class Crawler:
    """Web crawler for SEO analysis"""
    
    def __init__(self, timeout: int = 30000):
        """
        Initialize crawler
        
        Args:
            timeout: Page load timeout in milliseconds
        """
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def fetch_page(self, url: str) -> tuple[Optional[Page], Optional[str], Optional[float]]:
        """
        Fetch a page and return page object, HTML content, and load time
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (page, html_content, load_time)
        """
        try:
            page = await self.browser.new_page()
            
            # Measure load time
            start_time = asyncio.get_event_loop().time()
            
            response = await page.goto(url, wait_until="networkidle", timeout=self.timeout)
            
            load_time = (asyncio.get_event_loop().time() - start_time) * 1000  # Convert to ms
            
            if response and response.status >= 400:
                logger.warning(f"HTTP {response.status} for {url}")
                await page.close()
                return None, None, None
            
            html_content = await page.content()
            
            return page, html_content, load_time
            
        except PlaywrightTimeoutError:
            logger.error(f"Timeout loading {url}")
            return None, None, None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None, None, None
    
    async def get_performance_metrics(self, page: Page) -> Dict:
        """
        Get performance metrics from page
        
        Args:
            page: Playwright page object
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            # Get performance timing
            performance_timing = await page.evaluate("""() => {
                const perf = window.performance.timing;
                return {
                    domContentLoaded: perf.domContentLoadedEventEnd - perf.navigationStart,
                    loadComplete: perf.loadEventEnd - perf.navigationStart
                };
            }""")
            
            # Try to get Web Vitals (if available)
            metrics = {
                "dom_content_loaded": performance_timing.get("domContentLoaded") / 1000,  # Convert to seconds
                "load_complete": performance_timing.get("loadComplete") / 1000
            }
            
            # Try to get Lighthouse metrics via CDP
            try:
                cdp = await page.context.new_cdp_session(page)
                await cdp.send("Performance.enable")
                
                # Get metrics
                perf_metrics = await cdp.send("Performance.getMetrics")
                
                for metric in perf_metrics.get("metrics", []):
                    name = metric.get("name", "")
                    value = metric.get("value", 0)
                    
                    if "FirstContentfulPaint" in name:
                        metrics["first_contentful_paint"] = value / 1000
                    elif "LargestContentfulPaint" in name:
                        metrics["largest_contentful_paint"] = value / 1000
                    elif "TimeToInteractive" in name:
                        metrics["time_to_interactive"] = value / 1000
                    elif "TotalBlockingTime" in name:
                        metrics["total_blocking_time"] = value / 1000
                    elif "CumulativeLayoutShift" in name:
                        metrics["cumulative_layout_shift"] = value
                
                await cdp.detach()
            except Exception as e:
                logger.debug(f"Could not get CDP metrics: {str(e)}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {str(e)}")
            return {}
    
    def parse_html(self, html: str, base_url: str) -> BeautifulSoup:
        """
        Parse HTML with BeautifulSoup
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "lxml")
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, List[str]]:
        """
        Extract all links from page
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            Dictionary with internal and external links
        """
        base_domain = urlparse(base_url).netloc
        internal_links = []
        external_links = []
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            
            # Skip anchors and javascript links
            if href.startswith("#") or href.startswith("javascript:"):
                continue
            
            # Resolve relative URLs
            absolute_url = urljoin(base_url, href)
            parsed = urlparse(absolute_url)
            
            # Categorize links
            if parsed.netloc == base_domain or not parsed.netloc:
                internal_links.append(absolute_url)
            else:
                external_links.append(absolute_url)
        
        return {
            "internal": list(set(internal_links)),
            "external": list(set(external_links))
        }
    
    async def check_link(self, url: str) -> bool:
        """
        Check if a link is accessible
        
        Args:
            url: URL to check
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            page = await self.browser.new_page()
            response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)
            await page.close()
            return response and response.status < 400
        except Exception:
            return False

