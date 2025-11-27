from flask import Blueprint, request, jsonify
from database import db
from models import RecursoApoio

apoio_bp = Blueprint('apoio', __name__)


@apoio_bp.route('/recursos-apoio', methods=['GET'])
def obter_recursos():
    """
    Retorna recursos de apoio disponíveis

    Query params opcionais:
        - estado: Código do estado (ex: 'SP', 'RJ', 'PE')
        - tipo: Tipo de recurso ('emergencia', 'policial', 'apoio')

    Returns:
        JSON com lista de recursos de apoio
    """
    try:
        estado = request.args.get('estado')
        tipo = request.args.get('tipo')

        recursos = db.obter_recursos_apoio(estado)

        # Filtrar por tipo se especificado
        if tipo:
            recursos = [r for r in recursos if r.get('tipo') == tipo]

        return jsonify(recursos), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter recursos: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/<int:recurso_id>', methods=['GET'])
def obter_recurso_especifico(recurso_id):
    """
    Retorna um recurso específico por ID

    Args:
        recurso_id: ID do recurso

    Returns:
        JSON com dados do recurso
    """
    try:
        recursos = db.obter_recursos_apoio()

        recurso = next((r for r in recursos if r.get('id') == recurso_id), None)

        if not recurso:
            return jsonify({'erro': 'Recurso não encontrado'}), 404

        return jsonify(recurso), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter recurso: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/emergencia', methods=['GET'])
def obter_recursos_emergencia():
    """
    Retorna apenas recursos de emergência (linhas telefônicas urgentes)

    Returns:
        JSON com recursos de emergência
    """
    try:
        recursos = db.obter_recursos_apoio()
        recursos_emergencia = [r for r in recursos if r.get('tipo') == 'emergencia']

        return jsonify({
            'recursos': recursos_emergencia,
            'mensagem_urgente': 'Se você está em perigo imediato, ligue 190 ou 180',
            'total': len(recursos_emergencia)
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter recursos de emergência: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/por-estado/<string:estado>', methods=['GET'])
def obter_recursos_por_estado(estado):
    """
    Retorna recursos específicos de um estado

    Args:
        estado: Código do estado (ex: 'PE', 'SP', 'RJ')

    Returns:
        JSON com recursos do estado
    """
    try:
        # Normalizar código do estado
        estado_upper = estado.upper()

        recursos = db.obter_recursos_apoio(estado_upper)

        # Sempre incluir recursos nacionais (BR)
        recursos_nacionais = db.obter_recursos_apoio('BR')

        # Combinar recursos do estado com recursos nacionais
        todos_recursos = recursos + [r for r in recursos_nacionais if r not in recursos]

        return jsonify({
            'estado': estado_upper,
            'recursos': todos_recursos,
            'total': len(todos_recursos)
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter recursos do estado: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/tipos', methods=['GET'])
def listar_tipos():
    """
    Lista todos os tipos de recursos disponíveis

    Returns:
        JSON com tipos de recursos
    """
    try:
        tipos = [
            {
                'tipo': 'emergencia',
                'nome': 'Emergência',
                'descricao': 'Linhas telefônicas de atendimento imediato 24h',
                'icon': '🚨'
            },
            {
                'tipo': 'policial',
                'nome': 'Policial',
                'descricao': 'Delegacias e serviços policiais especializados',
                'icon': '👮'
            },
            {
                'tipo': 'apoio',
                'nome': 'Apoio',
                'descricao': 'Centros de apoio psicológico, social e jurídico',
                'icon': '🤝'
            }
        ]

        return jsonify(tipos), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao listar tipos: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/buscar', methods=['GET'])
def buscar_recursos():
    """
    Busca recursos por palavra-chave

    Query params:
        - q: Termo de busca

    Returns:
        JSON com recursos que correspondem à busca
    """
    try:
        termo = request.args.get('q', '').lower()

        if not termo or len(termo) < 2:
            return jsonify({
                'erro': 'Termo de busca muito curto (mínimo 2 caracteres)'
            }), 400

        recursos = db.obter_recursos_apoio()

        # Buscar em nome e descrição
        resultados = []
        for recurso in recursos:
            nome = recurso.get('nome', '').lower()
            descricao = recurso.get('descricao', '').lower()

            if termo in nome or termo in descricao:
                resultados.append(recurso)

        return jsonify({
            'termo': termo,
            'resultados': resultados,
            'total': len(resultados)
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar recursos: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/dicas-seguranca', methods=['GET'])
def obter_dicas_seguranca():
    """
    Retorna dicas de segurança para pessoas em situação de violência

    Returns:
        JSON com dicas de segurança
    """
    try:
        dicas = {
            'dicas_gerais': [
                'Mantenha documentos importantes em lugar seguro (RG, CPF, certidões)',
                'Tenha um plano de saída caso precise sair rapidamente de casa',
                'Confie em amigos ou familiares de confiança sobre sua situação',
                'Registre evidências (fotos de lesões, mensagens ameaçadoras)',
                'Saiba que você pode solicitar medidas protetivas na delegacia',
                'Não se culpe - a violência nunca é culpa da vítima'
            ],
            'em_caso_emergencia': [
                'Se estiver em perigo imediato, ligue 190 (Polícia Militar)',
                'Ligue 180 para orientações e denúncias (Central da Mulher)',
                'Procure um lugar seguro com pessoas que possam te ajudar',
                'Se possível, grave ou fotografe evidências da violência',
                'Não hesite em pedir ajuda - sua segurança é prioridade'
            ],
            'planejamento_saida': [
                'Tenha sempre um telefone carregado',
                'Guarde uma quantia de dinheiro em local seguro',
                'Prepare uma mala com itens essenciais (se possível)',
                'Identifique rotas de saída seguras da residência',
                'Combine sinais de alerta com vizinhos ou amigos de confiança',
                'Conheça os endereços de casas de acolhimento próximas'
            ],
            'direitos': [
                'Você tem direito a medidas protetivas de urgência',
                'Atendimento pela Polícia e Delegacia da Mulher é seu direito',
                'Acompanhamento psicológico e social gratuito está disponível',
                'Acesso à Defensoria Pública gratuita é garantido',
                'Você pode solicitar abrigo em casas de proteção'
            ]
        }

        return jsonify(dicas), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter dicas: {str(e)}'}), 500


@apoio_bp.route('/recursos-apoio/lei-maria-penha', methods=['GET'])
def obter_info_lei():
    """
    Retorna informações sobre a Lei Maria da Penha

    Returns:
        JSON com informações sobre a lei
    """
    try:
        info = {
            'titulo': 'Lei Maria da Penha',
            'numero': 'Lei 11.340/2006',
            'descricao': 'Lei brasileira que cria mecanismos para coibir a violência doméstica e familiar contra a mulher',
            'principais_pontos': [
                'Define os tipos de violência: física, psicológica, sexual, patrimonial e moral',
                'Cria mecanismos de proteção à mulher vítima de violência',
                'Estabelece medidas protetivas de urgência',
                'Proíbe a aplicação de penas pecuniárias (cestas básicas) aos agressores',
                'Permite a prisão preventiva do agressor',
                'Garante atendimento especializado e humanizado'
            ],
            'medidas_protetivas': [
                'Afastamento do agressor do lar',
                'Proibição de aproximação da vítima e familiares',
                'Proibição de contato por qualquer meio',
                'Restrição ou suspensão de visitas aos dependentes',
                'Prestação de alimentos provisionais'
            ],
            'como_solicitar': 'As medidas protetivas podem ser solicitadas na Delegacia da Mulher, Delegacia comum, Defensoria Pública ou diretamente no Juizado.',
            'link_oficial': 'http://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm'
        }

        return jsonify(info), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao obter informações da lei: {str(e)}'}), 500
