"""
Main scan service that orchestrates the analysis
"""

from typing import Dict, List
import logging
from datetime import datetime
from urllib.parse import urlparse

from services.crawler import Crawler
from services.analyzer import SEOAnalyzer
from models.schemas import ScanResponse, Metadata, Headings, Links, Images, Performance, Keywords

logger = logging.getLogger("seo_scanner")


class ScanService:
    """Main service for SEO scanning"""
    
    async def scan_url(self, url: str, depth: int = 1, include_external: bool = False) -> ScanResponse:
        """
        Perform complete SEO scan of a URL
        
        Args:
            url: URL to scan
            depth: Crawl depth (1-3)
            include_external: Whether to analyze external links
            
        Returns:
            ScanResponse with all analysis results
        """
        errors = []
        
        # Normalize URL
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        
        logger.info(f"Starting SEO scan for {url}")
        
        try:
            async with Crawler() as crawler:
                # Fetch page
                page, html_content, load_time = await crawler.fetch_page(url)
                
                if not html_content:
                    raise Exception("Failed to fetch page content")
                
                # Parse HTML
                soup = crawler.parse_html(html_content, url)
                
                # Initialize analyzer
                analyzer = SEOAnalyzer(url)
                
                # Analyze metadata
                metadata = analyzer.analyze_metadata(soup)
                
                # Analyze headings
                headings = analyzer.analyze_headings(soup)
                
                # Analyze images
                images = analyzer.analyze_images(soup)
                
                # Extract links
                links_dict = crawler.extract_links(soup, url)
                
                # Check broken links (sample)
                broken_links = []
                if links_dict["internal"]:
                    # Check first 10 internal links
                    sample_links = links_dict["internal"][:10]
                    for link in sample_links:
                        try:
                            is_accessible = await crawler.check_link(link)
                            if not is_accessible:
                                broken_links.append({"url": link, "status": "broken"})
                        except Exception as e:
                            logger.debug(f"Error checking link {link}: {str(e)}")
                            broken_links.append({"url": link, "status": "error"})
                
                links = Links(
                    internal=links_dict["internal"],
                    external=links_dict["external"],
                    broken=broken_links,
                    total=len(links_dict["internal"]) + len(links_dict["external"])
                )
                
                # Get performance metrics
                performance = None
                if page:
                    try:
                        perf_metrics = await crawler.get_performance_metrics(page)
                        performance = Performance(
                            load_time=load_time / 1000 if load_time else 0,  # Convert to seconds
                            dom_content_loaded=perf_metrics.get("dom_content_loaded"),
                            first_contentful_paint=perf_metrics.get("first_contentful_paint"),
                            largest_contentful_paint=perf_metrics.get("largest_contentful_paint"),
                            time_to_interactive=perf_metrics.get("time_to_interactive"),
                            total_blocking_time=perf_metrics.get("total_blocking_time"),
                            cumulative_layout_shift=perf_metrics.get("cumulative_layout_shift")
                        )
                    except Exception as e:
                        logger.warning(f"Could not get performance metrics: {str(e)}")
                        performance = Performance(load_time=load_time / 1000 if load_time else 0)
                
                # Analyze keywords
                keywords = analyzer.analyze_keywords(soup, metadata)
                
                # Check mobile-friendly
                mobile_friendly = analyzer.check_mobile_friendly(soup)
                
                # Check sitemap and robots.txt
                sitemap = analyzer.check_sitemap()
                robots_txt = analyzer.check_robots_txt()
                
                # Calculate SEO score
                score = analyzer.calculate_seo_score(
                    metadata, headings, images, links, mobile_friendly, performance
                )
                
                # Add bonus points for sitemap and robots.txt
                if sitemap:
                    score = min(score + 5, 100)
                if robots_txt:
                    score = min(score + 5, 100)
                
                # Close page
                if page:
                    await page.close()
                
                logger.info(f"SEO scan completed for {url}. Score: {score}")
                
                return ScanResponse(
                    url=url,
                    timestamp=datetime.now(),
                    score=score,
                    metadata=metadata,
                    headings=headings,
                    links=links,
                    images=images,
                    performance=performance,
                    keywords=keywords,
                    mobile_friendly=mobile_friendly,
                    sitemap=sitemap,
                    robots_txt=robots_txt,
                    errors=errors
                )
        
        except Exception as e:
            logger.error(f"Error during SEO scan: {str(e)}")
            errors.append(str(e))
            
            # Return partial response with errors
            return ScanResponse(
                url=url,
                timestamp=datetime.now(),
                score=0,
                metadata=Metadata(),
                headings=Headings(),
                links=Links(),
                images=Images(),
                keywords=Keywords(),
                mobile_friendly=False,
                errors=errors
            )

