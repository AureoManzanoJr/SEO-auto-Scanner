"""
Setup script for CLI

Desenvolvido por: Aureo Manzano Junior
Website: https://iadev.pro
Email: aureomanzano@icloud.com
"""

from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="seo-auto-scanner",
    version="1.0.0",
    author="Aureo Manzano Junior",
    author_email="aureomanzano@icloud.com",
    description="Ferramenta completa para análise automática de SEO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AureoManzanoJr/SEO-auto-Scanner",
    project_urls={
        "Homepage": "https://github.com/AureoManzanoJr/SEO-auto-Scanner",
        "Documentation": "https://github.com/AureoManzanoJr/SEO-auto-Scanner#readme",
        "Bug Reports": "https://github.com/AureoManzanoJr/SEO-auto-Scanner/issues",
        "Source": "https://github.com/AureoManzanoJr/SEO-auto-Scanner",
        "Author Website": "https://iadev.pro",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "click>=8.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "seo-scan=seo_scan:scan",
        ],
    },
    keywords="seo, scanner, analysis, automation, web, seo-tools",
)

