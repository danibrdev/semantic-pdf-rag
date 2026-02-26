from infra.factory import build_dependencies
from infra.config.settings import Settings

def create_container():
    return build_dependencies(Settings())