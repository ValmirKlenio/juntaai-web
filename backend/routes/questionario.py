from flask import Blueprint, request, jsonify
from database import db
from models import Resposta

questionario_bp = Blueprint('questionario', __name__)

# Perguntas do questionário
PERGUNTAS = [
    {
        'id': 1,
        'texto': 'Seu parceiro(a) te critica constantemente ou diminui suas conquistas?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 2,
        'texto': 'Você sente medo de expressar suas opiniões ou vontades?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 3,
        'texto': 'Seu parceiro(a) controla suas redes sociais, mensagens ou quem você pode ver?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 4,
        'texto': 'Já sofreu agressão física (empurrões, tapas, socos)?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Uma vez', 'Poucas vezes', 'Várias vezes', 'Constantemente']
    },
    {
        'id': 5,
        'texto': 'Seu parceiro(a) controla o dinheiro que você ganha ou impede que trabalhe?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 6,
        'texto': 'Você já foi forçada(o) a ter relações sexuais contra sua vontade?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Uma vez', 'Poucas vezes', 'Várias vezes', 'Constantemente']
    },
    {
        'id': 7,
        'texto': 'Seu parceiro(a) te ameaça ou ameaça pessoas próximas a você?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 8,
        'texto': 'Você se sente isolada(o) de amigos e familiares por causa do relacionamento?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 9,
        'texto': 'Seu parceiro(a) culpa você pelos problemas do relacionamento ou por suas atitudes violentas?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 10,
        'texto': 'Você tem ferimentos físicos que tenta esconder dos outros?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 11,
        'texto': 'Sente que está "pisando em ovos" ao redor de seu parceiro(a)?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    },
    {
        'id': 12,
        'texto': 'Já pensou em pedir ajuda mas teve medo das consequências?',
        'tipo': 'multipla',
        'opcoes': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre']
    }
]


@questionario_bp.route('/perguntas', methods=['GET'])
def obter_perguntas():
    """
    Retorna todas as perguntas do questionário

    Returns:
        JSON com lista de perguntas
    """
    return jsonify(PERGUNTAS), 200


@questionario_bp.route('/questionario', methods=['POST'])
def enviar_questionario():
    """
    Recebe e processa as respostas do questionário

    Expected JSON:
        {
            "respostas": {
                "1": "Nunca",
                "2": "Às vezes",
                ...
            }
        }

    Returns:
        JSON com resultado da avaliação de risco
    """
    try:
        data = request.get_json()

        if not data or 'respostas' not in data:
            return jsonify({'erro': 'Dados inválidos'}), 400

        respostas_dict = data['respostas']

        # Validar que todas as perguntas foram respondidas
        if len(respostas_dict) != len(PERGUNTAS):
            return jsonify({'erro': 'Respostas incompletas'}), 400

        # Criar objeto Resposta
        resposta = Resposta(
            id=None,  # Será definido pelo database
            respostas=respostas_dict
        )

        # Salvar no banco de dados
        sucesso = db.salvar_resposta(respostas_dict)

        if not sucesso:
            return jsonify({'erro': 'Erro ao salvar respostas'}), 500

        # Avaliar risco
        avaliacao = resposta.avaliar_risco()

        return jsonify({
            'sucesso': True,
            **avaliacao
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500


@questionario_bp.route('/questionario/validar', methods=['POST'])
def validar_respostas():
    """
    Valida as respostas sem salvar (útil para validação frontend)

    Returns:
        JSON indicando se as respostas são válidas
    """
    try:
        data = request.get_json()

        if not data or 'respostas' not in data:
            return jsonify({
                'valido': False,
                'erro': 'Dados inválidos'
            }), 400

        respostas_dict = data['respostas']

        # Verificar quantidade de respostas
        if len(respostas_dict) != len(PERGUNTAS):
            return jsonify({
                'valido': False,
                'erro': f'Esperado {len(PERGUNTAS)} respostas, recebido {len(respostas_dict)}'
            }), 200

        # Verificar se todas as respostas são válidas
        for pergunta in PERGUNTAS:
            pergunta_id = str(pergunta['id'])
            if pergunta_id not in respostas_dict:
                return jsonify({
                    'valido': False,
                    'erro': f'Falta resposta para pergunta {pergunta_id}'
                }), 200

            resposta_valor = respostas_dict[pergunta_id]
            if resposta_valor not in pergunta['opcoes']:
                return jsonify({
                    'valido': False,
                    'erro': f'Resposta inválida para pergunta {pergunta_id}'
                }), 200

        return jsonify({
            'valido': True,
            'mensagem': 'Todas as respostas são válidas'
        }), 200

    except Exception as e:
        return jsonify({
            'valido': False,
            'erro': f'Erro ao validar: {str(e)}'
        }), 500
