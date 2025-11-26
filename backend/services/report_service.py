"""
Report generation service
"""

from jinja2 import Template
from weasyprint import HTML
from pathlib import Path
import tempfile
import json
from typing import Dict
import logging

from models.schemas import ScanResponse

logger = logging.getLogger("seo_scanner")


class ReportService:
    """Service for generating reports"""
    
    def __init__(self):
        """Initialize report service"""
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
    
    def generate_html(self, scan_result: ScanResponse) -> str:
        """
        Generate HTML report
        
        Args:
            scan_result: ScanResponse object
            
        Returns:
            HTML content as string
        """
        # Load template
        template_path = self.templates_dir / "report.html"
        
        if not template_path.exists():
            # Create default template
            self._create_default_template(template_path)
        
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        # Convert scan result to dict for template
        result_dict = scan_result.model_dump()
        
        # Render template
        html_content = template.render(**result_dict)
        
        return html_content
    
    def generate_pdf(self, scan_result: ScanResponse) -> str:
        """
        Generate PDF report
        
        Args:
            scan_result: ScanResponse object
            
        Returns:
            Path to generated PDF file
        """
        # Generate HTML first
        html_content = self.generate_html(scan_result)
        
        # Create temporary file for PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()
        
        try:
            # Convert HTML to PDF
            HTML(string=html_content).write_pdf(temp_path)
            return temp_path
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    def generate_json(self, scan_result: ScanResponse) -> str:
        """
        Generate JSON report
        
        Args:
            scan_result: ScanResponse object
            
        Returns:
            JSON content as string
        """
        return scan_result.model_dump_json(indent=2)
    
    def _create_default_template(self, template_path: Path):
        """Create default HTML template"""
        template_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de SEO - {{ url }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .score {
            font-size: 4em;
            font-weight: bold;
            color: {% if score >= 80 %}#27ae60{% elif score >= 60 %}#f39c12{% else %}#e74c3c{% endif %};
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: {% if score >= 80 %}#d4edda{% elif score >= 60 %}#fff3cd{% else %}#f8d7da{% endif %};
            border-radius: 8px;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        .section h2 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.8em;
        }
        .metadata-item {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 4px;
        }
        .metadata-item strong {
            color: #007bff;
        }
        .heading-list {
            list-style: none;
            padding-left: 0;
        }
        .heading-list li {
            padding: 8px;
            margin: 5px 0;
            background: white;
            border-radius: 4px;
            border-left: 3px solid #007bff;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .badge-success { background: #d4edda; color: #155724; }
        .badge-warning { background: #fff3cd; color: #856404; }
        .badge-danger { background: #f8d7da; color: #721c24; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .info-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .info-card h3 {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .info-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: white;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #007bff;
            color: white;
            font-weight: bold;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Relatório de SEO</h1>
        <p style="color: #666; margin-bottom: 20px;">URL: <strong>{{ url }}</strong></p>
        <p style="color: #666;">Data: <strong>{{ timestamp }}</strong></p>
        
        <div class="score">{{ score }}/100</div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>Links Internos</h3>
                <div class="value">{{ links.internal|length }}</div>
            </div>
            <div class="info-card">
                <h3>Links Externos</h3>
                <div class="value">{{ links.external|length }}</div>
            </div>
            <div class="info-card">
                <h3>Links Quebrados</h3>
                <div class="value">{{ links.broken|length }}</div>
            </div>
            <div class="info-card">
                <h3>Imagens</h3>
                <div class="value">{{ images.total }}</div>
            </div>
            <div class="info-card">
                <h3>Sem ALT</h3>
                <div class="value">{{ images.without_alt }}</div>
            </div>
            <div class="info-card">
                <h3>Mobile-Friendly</h3>
                <div class="value">{% if mobile_friendly %}✓{% else %}✗{% endif %}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📄 Metadados</h2>
            <div class="metadata-item">
                <strong>Título:</strong> {{ metadata.title or 'Não encontrado' }}
            </div>
            <div class="metadata-item">
                <strong>Descrição:</strong> {{ metadata.description or 'Não encontrado' }}
            </div>
            {% if metadata.og_title %}
            <div class="metadata-item">
                <strong>OG Title:</strong> {{ metadata.og_title }}
            </div>
            {% endif %}
            {% if metadata.canonical %}
            <div class="metadata-item">
                <strong>Canonical:</strong> {{ metadata.canonical }}
            </div>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>📑 Estrutura de Headings</h2>
            {% if headings.h1 %}
            <h3>H1 ({{ headings.h1|length }})</h3>
            <ul class="heading-list">
                {% for h1 in headings.h1 %}
                <li>{{ h1 }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            
            {% if headings.h2 %}
            <h3>H2 ({{ headings.h2|length }})</h3>
            <ul class="heading-list">
                {% for h2 in headings.h2 %}
                <li>{{ h2 }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>🖼️ Imagens</h2>
            <p><strong>Total:</strong> {{ images.total }} | <strong>Sem ALT:</strong> {{ images.without_alt }}</p>
            {% if images.list %}
            <table>
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>ALT</th>
                        <th>Dimensões</th>
                    </tr>
                </thead>
                <tbody>
                    {% for img in images.list[:20] %}
                    <tr>
                        <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;">{{ img.src }}</td>
                        <td>{{ img.alt or '<span class="badge badge-danger">Sem ALT</span>'|safe }}</td>
                        <td>{% if img.width and img.height %}{{ img.width }}x{{ img.height }}{% else %}N/A{% endif %}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% endif %}
        </div>
        
        {% if links.broken %}
        <div class="section">
            <h2>🔗 Links Quebrados</h2>
            <ul class="heading-list">
                {% for broken in links.broken %}
                <li>{{ broken.url }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        {% if performance %}
        <div class="section">
            <h2>⚡ Performance</h2>
            <div class="metadata-item">
                <strong>Tempo de Carregamento:</strong> {{ "%.2f"|format(performance.load_time) }}s
            </div>
            {% if performance.first_contentful_paint %}
            <div class="metadata-item">
                <strong>First Contentful Paint:</strong> {{ "%.2f"|format(performance.first_contentful_paint) }}s
            </div>
            {% endif %}
        </div>
        {% endif %}
        
        {% if keywords.top_keywords %}
        <div class="section">
            <h2>🔤 Palavras-chave Principais</h2>
            <table>
                <thead>
                    <tr>
                        <th>Palavra</th>
                        <th>Frequência</th>
                        <th>Densidade (%)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for kw in keywords.top_keywords[:10] %}
                    <tr>
                        <td>{{ kw.word }}</td>
                        <td>{{ kw.count }}</td>
                        <td>{{ "%.2f"|format(kw.density) }}%</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        
        <div class="section">
            <h2>📋 Informações Adicionais</h2>
            <div class="metadata-item">
                <strong>Sitemap:</strong> {{ sitemap or 'Não encontrado' }}
            </div>
            <div class="metadata-item">
                <strong>Robots.txt:</strong> {{ robots_txt or 'Não encontrado' }}
            </div>
            <div class="metadata-item">
                <strong>Mobile-Friendly:</strong> 
                <span class="badge {% if mobile_friendly %}badge-success{% else %}badge-danger{% endif %}">
                    {% if mobile_friendly %}Sim{% else %}Não{% endif %}
                </span>
            </div>
        </div>
        
        {% if errors %}
        <div class="section">
            <h2>⚠️ Erros</h2>
            <ul class="heading-list">
                {% for error in errors %}
                <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <div class="footer">
            <p>Relatório gerado por SEO Auto Scanner</p>
            <p>Desenvolvido por <a href="https://iadev.pro">Aureo Manzano Junior</a></p>
            <p>{{ timestamp }}</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)

