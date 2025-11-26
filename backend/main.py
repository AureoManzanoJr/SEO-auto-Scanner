"""
SEO Auto Scanner - Backend API
FastAPI application for SEO analysis
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional
import logging
from datetime import datetime

from routers import scan, reports
from utils.logger import setup_logger

# Setup logging
logger = setup_logger()

# Create FastAPI app
app = FastAPI(
    title="SEO Auto Scanner API",
    description="API completa para análise automática de SEO",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scan.router, prefix="/api", tags=["Scan"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    return """
    <html>
        <head>
            <title>SEO Auto Scanner API</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🔍 SEO Auto Scanner API</h1>
            <p>API completa para análise automática de SEO</p>
            <ul>
                <li><a href="/docs">Documentação Swagger</a></li>
                <li><a href="/redoc">Documentação ReDoc</a></li>
                <li><a href="/health">Health Check</a></li>
            </ul>
        </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

