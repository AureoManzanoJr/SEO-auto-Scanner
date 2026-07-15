# SEO Auto Scanner

[![Python Tests](https://github.com/AureoManzanoJr/SEO-auto-Scanner/actions/workflows/python-tests.yml/badge.svg)](https://github.com/AureoManzanoJr/SEO-auto-Scanner/actions/workflows/python-tests.yml)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An automated technical-SEO scanner: crawl a site, analyze it against SEO best
practices, and produce a structured report. Available both as a REST API
(FastAPI) and a CLI.

## Why

Small businesses rarely know why they don't rank. This tool turns a URL into a
concrete, prioritized report — the kind of audit you'd otherwise pay for — and
exposes it as an API so it can plug into other products.

## What it checks

Crawling and analysis over the signals that actually move technical SEO — titles
and meta descriptions (presence, length, uniqueness), heading structure,
canonicals, indexability, internal links, images/alt text, and page metadata —
consolidated into a report you can act on.

## Architecture

```
backend/
  main.py                 → FastAPI app
  routers/scan.py         → POST a URL, kick off a scan
  routers/reports.py      → fetch/download reports
  services/crawler.py     → fetch and parse pages
  services/analyzer.py    → apply the SEO checks
  services/scan_service.py→ orchestrate a scan run
  services/report_service.py → build the report (JSON/PDF/HTML)
  models/schemas.py       → typed request/response models
cli/seo_scan.py           → run a scan from the terminal
backend/tests/            → analyzer tests
```

## Run

**API**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# POST http://localhost:8000/scan  { "url": "https://example.com" }
```

**CLI**
```bash
python cli/seo_scan.py https://example.com
```

## Tests

```bash
cd backend && python -m pytest
```

## Roadmap

- Core Web Vitals integration
- Scheduled re-scans and diffs over time
- Competitive comparison

## License

MIT © Aureo Manzano Junior
