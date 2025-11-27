from flask import Blueprint, request, jsonify
from database import db
from models import Estatistica
from datetime import datetime, timedelta

estatisticas_bp = Blueprint('estatisticas', __name__)


@estatisticas_bp.route('/estatisticas', methods=['GET'])
def obter_estatisticas():
    """
    Retorna estatísticas agregadas e anônimas das respostas

    Query params opcionais:
        - periodo: 'semana', 'mes', 'ano', 'total' (default: 'total')

    Returns:
        JSON com estatísticas agregadas
    """
    try:
        periodo = request.args.get('periodo', 'total')

        stats = db.obter_estatisticas()

        # Adicionar métricas adicionais
        total = stats.get('total_respostas', 0)

        if total > 0:
            analise = stats.get('analise', {})

            # Calcular estatísticas por tipo de violência
            categorias_violencia = {
                'psicologica': [1, 2, 9, 11],  # IDs das perguntas relacionadas
                'fisica': [4, 10],
                'controle': [3, 5, 8],
                'sexual': [6],
                'ameaca': [7, 12]
            }

            stats['analise_categorias'] = {}

            for categoria, perguntas_ids in categorias_violencia.items():
                # Contar respostas preocupantes (Frequentemente, Sempre, etc)
                count_preocupante = 0

                for pid in perguntas_ids:
                    pergunta_key = str(pid)
                    if pergunta_key in analise:
                        respostas_perguntas = analise[pergunta_key]
                        count_preocupante += respostas_perguntas.get('Sempre', 0)
                        count_preocupante += respostas_perguntas.get('Constantemente', 0)
                        count_preocupante += respostas_perguntas.get('Frequentemente', 0)
                        count_preocupante += respostas_perguntas.get('Várias vezes', 0)

                percentual = (count_preocupante / (total * len(perguntas_ids))) * 100 if total > 0 else 0

                stats['analise_categorias'][categoria] = {
                    'total_respostas_preocupantes': count_preocupante,
                    'percentual': round(percentual, 2)
                }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter estatísticas: {str(e)}'}), 500


@estatisticas_bp.route('/estatisticas/resumo', methods=['GET'])
def obter_resumo():
    """
    Retorna um resumo simplificado das estatísticas principais

    Returns:
        JSON com resumo das estatísticas
    """
    try:
        stats = db.obter_estatisticas()
        total = stats.get('total_respostas', 0)

        if total == 0:
            return jsonify({
                'total_respostas': 0,
                'mensagem': 'Ainda não há dados suficientes para análise'
            }), 200

        # Calcular níveis de risco estimados
        analise = stats.get('analise', {})

        respostas_alto_risco = 0
        respostas_medio_risco = 0
        respostas_baixo_risco = 0

        # Lógica simplificada de estimativa
        # Conta quantas pessoas responderam "Sempre" ou "Constantemente" em múltiplas perguntas
        for pergunta_id, respostas_pergunta in analise.items():
            respostas_alto_risco += respostas_pergunta.get('Sempre', 0)
            respostas_alto_risco += respostas_pergunta.get('Constantemente', 0)

            respostas_medio_risco += respostas_pergunta.get('Frequentemente', 0)
            respostas_medio_risco += respostas_pergunta.get('Várias vezes', 0)
            respostas_medio_risco += respostas_pergunta.get('Às vezes', 0)
            respostas_medio_risco += respostas_pergunta.get('Poucas vezes', 0)

        resumo = {
            'total_respostas': total,
            'estimativa_sinais': {
                'alto_risco': respostas_alto_risco,
                'medio_risco': respostas_medio_risco,
                'mensagem': 'Estes são dados agregados e não representam indivíduos específicos'
            },
            'ultima_atualizacao': datetime.now().isoformat()
        }

        return jsonify(resumo), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter resumo: {str(e)}'}), 500


@estatisticas_bp.route('/estatisticas/exportar', methods=['GET'])
def exportar_estatisticas():
    """
    Exporta estatísticas em formato adequado para pesquisa acadêmica
    (mantendo anonimato completo)

    Returns:
        JSON formatado para uso acadêmico
    """
    try:
        stats = db.obter_estatisticas()

        exportacao = {
            'metadata': {
                'projeto': 'Junta AÍ',
                'descricao': 'Dados agregados e anônimos sobre violência em relacionamentos',
                'data_exportacao': datetime.now().isoformat(),
                'total_participantes': stats.get('total_respostas', 0),
                'aviso': 'Todos os dados são completamente anônimos e agregados'
            },
            'dados': {
                'total_respostas': stats.get('total_respostas', 0),
                'analise_respostas': stats.get('analise', {}),
                'categorias': stats.get('analise_categorias', {})
            },
            'referencias': {
                'lei_maria_penha': 'Lei 11.340/2006',
                'oms': 'Organização Mundial da Saúde - Dados sobre violência contra mulheres',
                'forum_seguranca': 'Fórum Brasileiro de Segurança Pública'
            }
        }

        return jsonify(exportacao), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao exportar: {str(e)}'}), 500


@estatisticas_bp.route('/estatisticas/pergunta/<int:pergunta_id>', methods=['GET'])
def obter_estatistica_pergunta(pergunta_id):
    """
    Retorna estatísticas específicas de uma pergunta

    Args:
        pergunta_id: ID da pergunta

    Returns:
        JSON com estatísticas da pergunta específica
    """
    try:
        if pergunta_id < 1 or pergunta_id > 12:
            return jsonify({'erro': 'ID de pergunta inválido'}), 400

        stats = db.obter_estatisticas()
        analise = stats.get('analise', {})

        pergunta_key = str(pergunta_id)

        if pergunta_key not in analise:
            return jsonify({
                'pergunta_id': pergunta_id,
                'respostas': {},
                'total': 0
            }), 200

        respostas_pergunta = analise[pergunta_key]
        total = sum(respostas_pergunta.values())

        # Calcular percentuais
        percentuais = {}
        for resposta, count in respostas_pergunta.items():
            percentuais[resposta] = round((count / total * 100), 2) if total > 0 else 0

        return jsonify({
            'pergunta_id': pergunta_id,
            'respostas': respostas_pergunta,
            'percentuais': percentuais,
            'total': total
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter estatística da pergunta: {str(e)}'}), 500
