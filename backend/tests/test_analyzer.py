"""
Tests for SEO analyzer

Desenvolvido por: Aureo Manzano Junior
Website: https://iadev.pro
Email: aureomanzano@icloud.com
"""

import pytest
from bs4 import BeautifulSoup
from services.analyzer import SEOAnalyzer
from models.schemas import Metadata


class TestSEOAnalyzer:
    """Test cases for SEOAnalyzer"""
    
    def test_analyze_metadata_title(self):
        """Test metadata title extraction"""
        html = "<html><head><title>Test Title</title></head><body></body></html>"
        soup = BeautifulSoup(html, "lxml")
        analyzer = SEOAnalyzer("https://example.com")
        metadata = analyzer.analyze_metadata(soup)
        
        assert metadata.title == "Test Title"
    
    def test_analyze_metadata_description(self):
        """Test metadata description extraction"""
        html = """<html><head>
            <meta name="description" content="Test description">
        </head><body></body></html>"""
        soup = BeautifulSoup(html, "lxml")
        analyzer = SEOAnalyzer("https://example.com")
        metadata = analyzer.analyze_metadata(soup)
        
        assert metadata.description == "Test description"
    
    def test_analyze_headings(self):
        """Test headings extraction"""
        html = """<html><body>
            <h1>Main Title</h1>
            <h2>Subtitle 1</h2>
            <h2>Subtitle 2</h2>
        </body></html>"""
        soup = BeautifulSoup(html, "lxml")
        analyzer = SEOAnalyzer("https://example.com")
        headings = analyzer.analyze_headings(soup)
        
        assert len(headings.h1) == 1
        assert headings.h1[0] == "Main Title"
        assert len(headings.h2) == 2
    
    def test_analyze_images(self):
        """Test images analysis"""
        html = """<html><body>
            <img src="image1.jpg" alt="Image 1">
            <img src="image2.jpg">
            <img src="image3.jpg" alt="Image 3">
        </body></html>"""
        soup = BeautifulSoup(html, "lxml")
        analyzer = SEOAnalyzer("https://example.com")
        images = analyzer.analyze_images(soup)
        
        assert images.total == 3
        assert images.without_alt == 1
    
    def test_check_mobile_friendly(self):
        """Test mobile-friendly check"""
        html = """<html><head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head><body></body></html>"""
        soup = BeautifulSoup(html, "lxml")
        analyzer = SEOAnalyzer("https://example.com")
        is_mobile = analyzer.check_mobile_friendly(soup)
        
        assert is_mobile is True
    
    def test_calculate_seo_score(self):
        """Test SEO score calculation"""
        analyzer = SEOAnalyzer("https://example.com")
        
        metadata = Metadata(
            title="Test Title",
            description="Test description with enough characters"
        )
        
        from models.schemas import Headings, Images, Links, Performance
        
        headings = Headings(h1=["Main Title"], h2=["Subtitle"])
        images = Images(total=10, without_alt=2, list=[])
        links = Links(internal=["/page1"], external=[], broken=[], total=1)
        performance = Performance(load_time=1.5)
        
        score = analyzer.calculate_seo_score(
            metadata, headings, images, links, True, performance
        )
        
        assert 0 <= score <= 100

