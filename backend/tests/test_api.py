"""
Tests for API endpoints

Desenvolvido por: Aureo Manzano Junior
Website: https://iadev.pro
Email: aureomanzano@icloud.com
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPI:
    """Test cases for API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_scan_endpoint_invalid_url(self):
        """Test scan endpoint with invalid URL"""
        response = client.post(
            "/api/scan",
            json={"url": "invalid-url"}
        )
        # Should return 422 (validation error) or handle gracefully
        assert response.status_code in [422, 500]
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

