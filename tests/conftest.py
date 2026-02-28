"""
Configuração global dos testes (conftest.py).

Este arquivo é carregado automaticamente pelo Pytest antes de qualquer teste.
Garante que a raiz do projeto esteja no sys.path do Python, permitindo que
os módulos do projeto (cli, core, domain, infra) sejam importados corretamente
durante a execução dos testes sem necessidade de instalação do pacote.
"""

from pathlib import Path
import sys

# Resolve o diretório raiz do projeto (dois níveis acima de tests/conftest.py)
ROOT = Path(__file__).resolve().parents[1]

# Adiciona a raiz ao sys.path apenas se ainda não estiver presente
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
