"""
Bootstrap do container de dependências.

Ponto de entrada conveniente para obter o container de dependências
completo sem precisar instanciar Settings manualmente.
Usado como atalho em contextos onde a inicialização simplificada é suficiente.
"""

from infra.factory import build_dependencies
from infra.config.settings import Settings

def create_container():
    """Cria e retorna o container de dependências usando as configurações do .env."""
    return build_dependencies(Settings())