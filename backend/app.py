from flask import Flask, jsonify
from flask_cors import CORS
from database import db
import os
from dotenv import load_dotenv

# Importar função de registro de blueprints
from routes import register_blueprints

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Registrar todas as rotas modularizadas
register_blueprints(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check para verificar se a API está funcionando

    Returns:
        JSON indicando status da API
    """
    return jsonify({
        'status': 'ok',
        'message': 'Junta AÍ API está funcionando',
        'version': '1.0.0'
    }), 200


@app.route('/', methods=['GET'])
def index():
    """
    Rota raiz da API

    Returns:
        JSON com informações sobre a API
    """
    return jsonify({
        'projeto': 'Junta AÍ',
        'descricao': 'API para plataforma de conscientização sobre violência em relacionamentos',
        'versao': '1.0.0',
        'endpoints': {
            'questionario': '/api/perguntas, /api/questionario',
            'estatisticas': '/api/estatisticas',
            'apoio': '/api/recursos-apoio',
            'health': '/api/health'
        },
        'documentacao': 'Acesse os endpoints acima para utilizar a API'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    return jsonify({
        'erro': 'Rota não encontrada',
        'status': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos do servidor"""
    return jsonify({
        'erro': 'Erro interno do servidor',
        'status': 500
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    print(f"""
    ╔══════════════════════════════════════════╗
    ║         JUNTA AÍ - API Backend          ║
    ╠══════════════════════════════════════════╣
    ║  Servidor rodando em:                   ║
    ║  http://localhost:{port}                  ║
    ║                                          ║
    ║  Endpoints disponíveis:                  ║
    ║  • GET  /api/perguntas                   ║
    ║  • POST /api/questionario                ║
    ║  • GET  /api/estatisticas                ║
    ║  • GET  /api/recursos-apoio              ║
    ║  • GET  /api/health                      ║
    ╚══════════════════════════════════════════╝
    """)

    app.run(debug=debug, port=port, host='0.0.0.0')
