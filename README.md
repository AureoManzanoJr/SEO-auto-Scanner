# 🔍 SEO Auto Scanner

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Stars](https://img.shields.io/github/stars/AureoManzanoJr/SEO-auto-Scanner?style=social)](https://github.com/AureoManzanoJr/SEO-auto-Scanner)
[![Forks](https://img.shields.io/github/forks/AureoManzanoJr/SEO-auto-Scanner?style=social)](https://github.com/AureoManzanoJr/SEO-auto-Scanner)

> Ferramenta completa e automatizada para análise de SEO de qualquer site, gerando relatórios detalhados em JSON, PDF e HTML. Desenvolvida para ajudar pequenos negócios a melhorar sua visibilidade online.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [API](#-api)
- [CLI](#-cli)
- [Testes](#-testes)
- [Roadmap](#-roadmap)
- [Contribuindo](#-contribuindo)
- [Autor](#-autor)
- [Licença](#-licença)

## 🎯 Sobre o Projeto

O **SEO Auto Scanner** é uma ferramenta profissional que analisa automaticamente qualquer site e gera relatórios completos de SEO. Ideal para pequenos negócios que precisam melhorar sua visibilidade online sem gastar com ferramentas caras.

### Por que usar?

- ✅ **Gratuito e Open Source** - Sem limites de uso
- ✅ **Análise Completa** - Todos os aspectos de SEO em um só lugar
- ✅ **Relatórios Exportáveis** - JSON, PDF e HTML
- ✅ **Interface Moderna** - Dashboard intuitivo e responsivo
- ✅ **CLI Poderoso** - Integre em seus scripts e automações
- ✅ **API RESTful** - Use em seus próprios projetos
- ✅ **Dark/Light Mode** - Interface adaptável ao seu gosto

## ✨ Funcionalidades

### Análise Completa de SEO

- 📄 **Metadados**: Title, Description, Open Graph, Twitter Cards
- 📑 **Estrutura de Headings**: H1, H2, H3, H4, H5, H6
- 🔗 **Links**: URLs internas, externas e quebrados
- ⚡ **Performance**: Velocidade de carregamento e métricas
- 🖼️ **Imagens**: Verificação de ALT text
- 🗺️ **Sitemap e Robots.txt**: Detecção e análise
- 🔤 **Keyword Density**: Análise de palavras-chave
- 📱 **Mobile-Friendly**: Avaliação de responsividade
- 📊 **Pontuação Geral**: Score de 0-100

### Relatórios

- 📄 **JSON**: Para integração e processamento
- 📑 **PDF**: Relatórios profissionais prontos para impressão
- 🌐 **HTML**: Visualização interativa no navegador

## 🛠️ Tecnologias

### Backend
- **Python 3.9+**
- **FastAPI** - Framework web moderno e rápido
- **Playwright** - Crawling e análise de páginas
- **BeautifulSoup4** - Parsing HTML
- **Jinja2** - Templates para relatórios HTML
- **WeasyPrint** - Geração de PDFs

### Frontend
- **Next.js 14** - Framework React
- **TailwindCSS** - Estilização moderna
- **TypeScript** - Type safety

### CLI
- **Click** - Interface de linha de comando

### Testes
- **Pytest** - Framework de testes

## 📦 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- Node.js 18 ou superior
- npm ou yarn

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/AureoManzanoJr/SEO-auto-Scanner.git
cd SEO-auto-Scanner
```

2. **Instale as dependências do backend**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
playwright install
```

3. **Instale as dependências do frontend**
```bash
cd ../frontend
npm install
```

4. **Instale o CLI (opcional)**
```bash
cd ../cli
pip install -e .
```

## 🚀 Como Usar

### Modo Web (Frontend + Backend)

1. **Inicie o backend**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. **Inicie o frontend**
```bash
cd frontend
npm run dev
```

3. **Acesse no navegador**
```
http://localhost:3000
```

### CLI

```bash
# Análise básica
seo-scan https://exemplo.com

# Exportar como JSON
seo-scan https://exemplo.com --json output.json

# Exportar como PDF
seo-scan https://exemplo.com --pdf output.pdf

# Exportar como HTML
seo-scan https://exemplo.com --html output.html
```

### API

```bash
# Health check
curl http://localhost:8000/health

# Realizar scan
curl -X POST http://localhost:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com"}'

# Obter relatório HTML
curl http://localhost:8000/api/report/html?url=https://exemplo.com

# Obter relatório PDF
curl http://localhost:8000/api/report/pdf?url=https://exemplo.com -o report.pdf
```

## 📡 API

### Endpoints

#### `POST /api/scan`
Realiza uma análise completa de SEO de uma URL.

**Request:**
```json
{
  "url": "https://exemplo.com",
  "depth": 1,
  "include_external": false
}
```

**Response:**
```json
{
  "url": "https://exemplo.com",
  "timestamp": "2024-01-01T12:00:00",
  "score": 85,
  "metadata": {
    "title": "Título da Página",
    "description": "Descrição da página"
  },
  "headings": {
    "h1": ["Título Principal"],
    "h2": ["Subtítulo 1", "Subtítulo 2"]
  },
  "links": {
    "internal": ["/pagina1", "/pagina2"],
    "external": ["https://exemplo2.com"],
    "broken": []
  },
  "images": {
    "total": 10,
    "without_alt": 2
  },
  "performance": {
    "load_time": 1.23
  },
  "keywords": {
    "density": {}
  },
  "mobile_friendly": true,
  "sitemap": "https://exemplo.com/sitemap.xml",
  "robots_txt": "https://exemplo.com/robots.txt"
}
```

#### `GET /health`
Verifica o status da API.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### `GET /api/report/html?url={url}`
Gera relatório HTML.

#### `GET /api/report/pdf?url={url}`
Gera relatório PDF.

#### `GET /api/report/json?url={url}`
Retorna relatório em JSON.

## 🧪 Testes

Execute os testes com:

```bash
cd backend
pytest tests/ -v
```

Para cobertura de código:

```bash
pytest tests/ --cov=. --cov-report=html
```

## 🗺️ Roadmap

- [x] Análise básica de SEO
- [x] Geração de relatórios (JSON, PDF, HTML)
- [x] Interface web moderna
- [x] CLI funcional
- [ ] Suporte a análise de múltiplas URLs
- [ ] Comparação entre versões de relatórios
- [ ] Integração com Google Search Console
- [ ] Análise de Core Web Vitals
- [ ] Dashboard com histórico de análises
- [ ] Suporte a autenticação
- [ ] API rate limiting
- [ ] Cache de resultados
- [ ] Análise de concorrentes
- [ ] Exportação para Excel

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

### Padrões de Código

- Siga PEP 8 para Python
- Use ESLint/Prettier para JavaScript/TypeScript
- Escreva testes para novas funcionalidades
- Documente funções e classes

## 👨‍💻 Autor

**Aureo Manzano Junior**

Desenvolvedor apaixonado por criar soluções que fazem a diferença. Especializado em desenvolvimento web, automação e ferramentas de produtividade.

- 🌐 **Website:** [iadev.pro](https://iadev.pro)
- 📧 **Email:** [aureomanzano@icloud.com](mailto:aureomanzano@icloud.com)
- 💼 **GitHub:** [@AureoManzanoJr](https://github.com/AureoManzanoJr)
- 🚀 **Portfólio:** [iadev.pro](https://iadev.pro)

### Entre em Contato

Tem uma ideia, sugestão ou quer trabalhar junto? Entre em contato!

- 📧 Email: [aureomanzano@icloud.com](mailto:aureomanzano@icloud.com)
- 🌐 Website: [iadev.pro](https://iadev.pro)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ⭐ Suporte

Se este projeto foi útil para você, considere:

- ⭐ **Dar uma estrela** no GitHub
- 🍴 **Fazer um fork**
- 🐛 **Reportar bugs**
- 💡 **Sugerir novas funcionalidades**
- 📢 **Compartilhar com seus amigos**

## 🙏 Agradecimentos

Obrigado por usar o SEO Auto Scanner! Se você gostou do projeto, considere dar uma estrela ⭐ e compartilhar com outros desenvolvedores.

---

**Desenvolvido com ❤️ por [Aureo Manzano Junior](https://iadev.pro)**

*Transformando ideias em código que funciona.*

**Contato:** [aureomanzano@icloud.com](mailto:aureomanzano@icloud.com) | **Portfólio:** [iadev.pro](https://iadev.pro)

