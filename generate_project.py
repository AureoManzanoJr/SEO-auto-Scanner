"""Script para gerar todos os arquivos do projeto SEO Auto Scanner"""
import os
from pathlib import Path

base_dir = Path(__file__).parent

# Criar estrutura de diretórios
dirs = [
    'backend/routers',
    'backend/services', 
    'backend/models',
    'backend/utils',
    'backend/tests',
    'backend/templates',
    'cli',
    'frontend/app',
    'docs',
    '.github/workflows'
]

for d in dirs:
    (base_dir / d).mkdir(parents=True, exist_ok=True)
    # Criar __init__.py para Python packages
    if 'backend' in d or 'cli' in d:
        init_file = base_dir / d / '__init__.py'
        if not init_file.exists():
            init_file.write_text('', encoding='utf-8')

print("Estrutura de diretórios criada!")
print("Agora você pode copiar os arquivos do projeto para este diretório.")
print("Ou execute os comandos git para fazer push dos arquivos existentes.")

