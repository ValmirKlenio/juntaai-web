"""
Módulo de rotas do backend Junta AÍ
"""

from flask import Blueprint

# Importar blueprints das rotas
from .questionario import questionario_bp
from .estatisticas import estatisticas_bp
from .apoio import apoio_bp


def register_blueprints(app):
    """
    Registra todos os blueprints na aplicação Flask

    Args:
        app: Instância da aplicação Flask
    """
    app.register_blueprint(questionario_bp, url_prefix='/api')
    app.register_blueprint(estatisticas_bp, url_prefix='/api')
    app.register_blueprint(apoio_bp, url_prefix='/api')


__all__ = ['register_blueprints', 'questionario_bp', 'estatisticas_bp', 'apoio_bp']
