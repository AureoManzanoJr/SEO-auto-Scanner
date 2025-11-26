#!/usr/bin/env python3
"""
SEO Scanner CLI
Command-line interface for SEO analysis

Desenvolvido por: Aureo Manzano Junior
Website: https://iadev.pro
Email: aureomanzano@icloud.com
"""

import click
import json
import sys
from pathlib import Path
import requests
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.scan_service import ScanService
from backend.services.report_service import ReportService


@click.command()
@click.argument("url", type=str)
@click.option("--json", "json_output", type=click.Path(), help="Export as JSON file")
@click.option("--pdf", "pdf_output", type=click.Path(), help="Export as PDF file")
@click.option("--html", "html_output", type=click.Path(), help="Export as HTML file")
@click.option("--api", "api_url", default="http://localhost:8000", help="API base URL")
@click.option("--depth", default=1, type=int, help="Crawl depth (1-3)")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.version_option(version="1.0.0", prog_name="seo-scan")
def scan(url: str, json_output: Optional[str], pdf_output: Optional[str], 
         html_output: Optional[str], api_url: str, depth: int, verbose: bool):
    """
    Scan a URL for SEO analysis.
    
    Desenvolvido por: Aureo Manzano Junior (https://iadev.pro)
    
    Examples:
    
    \b
        seo-scan https://example.com
        seo-scan https://example.com --json report.json
        seo-scan https://example.com --pdf report.pdf
        seo-scan https://example.com --html report.html
    """
    if verbose:
        click.echo("SEO Auto Scanner v1.0.0")
        click.echo("Desenvolvido por: Aureo Manzano Junior (https://iadev.pro)")
        click.echo("")
    
    click.echo(f"🔍 Scanning {url}...")
    
    try:
        # Check if API is available
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            use_api = response.status_code == 200
        except:
            use_api = False
            if verbose:
                click.echo("⚠️  API not available, using local scan...")
        
        if use_api:
            # Use API
            scan_result = _scan_via_api(url, api_url, depth, verbose)
        else:
            # Use local scan service
            scan_result = _scan_local(url, depth, verbose)
        
        if not scan_result:
            click.echo("❌ Error: Failed to scan URL", err=True)
            sys.exit(1)
        
        # Display results
        _display_results(scan_result, verbose)
        
        # Export if requested
        if json_output:
            _export_json(scan_result, json_output)
        
        if pdf_output:
            _export_pdf(scan_result, pdf_output, use_api, api_url)
        
        if html_output:
            _export_html(scan_result, html_output, use_api, api_url)
        
        click.echo(f"\n✅ Scan completed! Score: {scan_result.get('score', 0)}/100")
        
    except KeyboardInterrupt:
        click.echo("\n⚠️  Scan interrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _scan_via_api(url: str, api_url: str, depth: int, verbose: bool) -> Optional[dict]:
    """Scan using API"""
    try:
        response = requests.post(
            f"{api_url}/api/scan",
            json={"url": url, "depth": depth},
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        if verbose:
            click.echo(f"API error: {str(e)}", err=True)
        return None


def _scan_local(url: str, depth: int, verbose: bool) -> Optional[dict]:
    """Scan using local service (sync wrapper)"""
    import asyncio
    from backend.services.scan_service import ScanService
    
    service = ScanService()
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    result = loop.run_until_complete(service.scan_url(url, depth=depth))
    return result.model_dump() if result else None


def _display_results(result: dict, verbose: bool):
    """Display scan results"""
    click.echo(f"\n📊 SEO Score: {result.get('score', 0)}/100")
    
    if verbose:
        metadata = result.get("metadata", {})
        if metadata.get("title"):
            click.echo(f"📄 Title: {metadata['title']}")
        if metadata.get("description"):
            click.echo(f"📝 Description: {metadata['description'][:100]}...")
        
        headings = result.get("headings", {})
        click.echo(f"📑 H1: {len(headings.get('h1', []))}")
        click.echo(f"📑 H2: {len(headings.get('h2', []))}")
        
        images = result.get("images", {})
        click.echo(f"🖼️  Images: {images.get('total', 0)} (without ALT: {images.get('without_alt', 0)})")
        
        links = result.get("links", {})
        click.echo(f"🔗 Internal links: {len(links.get('internal', []))}")
        click.echo(f"🔗 External links: {len(links.get('external', []))}")
        click.echo(f"🔗 Broken links: {len(links.get('broken', []))}")


def _export_json(result: dict, output_path: str):
    """Export results as JSON"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    click.echo(f"💾 JSON exported to: {output_path}")


def _export_pdf(result: dict, output_path: str, use_api: bool, api_url: str):
    """Export results as PDF"""
    if use_api:
        try:
            url = result.get("url", "")
            response = requests.get(
                f"{api_url}/api/report/pdf",
                params={"url": url},
                timeout=300
            )
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            click.echo(f"💾 PDF exported to: {output_path}")
        except Exception as e:
            click.echo(f"❌ Error exporting PDF: {str(e)}", err=True)
    else:
        from backend.services.report_service import ReportService
        from backend.models.schemas import ScanResponse
        
        try:
            scan_response = ScanResponse(**result)
            report_service = ReportService()
            pdf_path = report_service.generate_pdf(scan_response)
            
            import shutil
            shutil.move(pdf_path, output_path)
            click.echo(f"💾 PDF exported to: {output_path}")
        except Exception as e:
            click.echo(f"❌ Error exporting PDF: {str(e)}", err=True)


def _export_html(result: dict, output_path: str, use_api: bool, api_url: str):
    """Export results as HTML"""
    if use_api:
        try:
            url = result.get("url", "")
            response = requests.get(
                f"{api_url}/api/report/html",
                params={"url": url},
                timeout=300
            )
            response.raise_for_status()
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            click.echo(f"💾 HTML exported to: {output_path}")
        except Exception as e:
            click.echo(f"❌ Error exporting HTML: {str(e)}", err=True)
    else:
        from backend.services.report_service import ReportService
        from backend.models.schemas import ScanResponse
        
        try:
            scan_response = ScanResponse(**result)
            report_service = ReportService()
            html_content = report_service.generate_html(scan_response)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            click.echo(f"💾 HTML exported to: {output_path}")
        except Exception as e:
            click.echo(f"❌ Error exporting HTML: {str(e)}", err=True)


if __name__ == "__main__":
    scan()

