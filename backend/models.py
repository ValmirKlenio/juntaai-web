from datetime import datetime
from typing import Dict, List, Optional
import json


class Resposta:
    """Model para respostas do questionário"""

    def __init__(self, id: int, respostas: Dict, timestamp: str = None):
        self.id = id
        self.respostas = respostas
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'respostas': self.respostas,
            'timestamp': self.timestamp
        }

    def calcular_pontuacao(self) -> int:
        """Calcula pontuação baseada nas respostas"""
        pontos = 0
        for resposta in self.respostas.values():
            if resposta in ['Sempre', 'Constantemente']:
                pontos += 4
            elif resposta in ['Frequentemente', 'Várias vezes']:
                pontos += 3
            elif resposta in ['Às vezes', 'Poucas vezes']:
                pontos += 2
            elif resposta in ['Raramente', 'Uma vez']:
                pontos += 1
        return pontos

    def avaliar_risco(self) -> Dict:
        """Avalia nível de risco baseado na pontuação"""
        pontos = self.calcular_pontuacao()

        if pontos >= 30:
            return {
                'nivel_risco': 'alto',
                'mensagem': 'Seus resultados indicam sinais significativos de violência. Considere buscar ajuda imediatamente.',
                'pontuacao': pontos
            }
        elif pontos >= 15:
            return {
                'nivel_risco': 'medio',
                'mensagem': 'Seus resultados indicam alguns sinais preocupantes. Recomendamos conversar com alguém de confiança.',
                'pontuacao': pontos
            }
        else:
            return {
                'nivel_risco': 'baixo',
                'mensagem': 'Seus resultados indicam sinais baixos de violência.',
                'pontuacao': pontos
            }


class RecursoApoio:
    """Model para recursos de apoio"""

    def __init__(self, id: int, nome: str, descricao: str, tipo: str,
                 estado: str = 'BR', telefone: str = None, endereco: str = None,
                 site: str = None, horario: str = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo  # 'emergencia', 'policial', 'apoio'
        self.estado = estado
        self.telefone = telefone
        self.endereco = endereco
        self.site = site
        self.horario = horario

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'estado': self.estado,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'site': self.site,
            'horario': self.horario
        }


class Pergunta:
    """Model para perguntas do questionário"""

    def __init__(self, id: int, texto: str, tipo: str, opcoes: List[str]):
        self.id = id
        self.texto = texto
        self.tipo = tipo  # 'multipla', 'aberta'
        self.opcoes = opcoes

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'texto': self.texto,
            'tipo': self.tipo,
            'opcoes': self.opcoes
        }


class Estatistica:
    """Model para estatísticas agregadas"""

    def __init__(self, total_respostas: int, analise: Dict = None):
        self.total_respostas = total_respostas
        self.analise = analise or {}

    def to_dict(self) -> Dict:
        return {
            'total_respostas': self.total_respostas,
            'analise': self.analise
        }

    def adicionar_analise_pergunta(self, pergunta_id: str, resposta: str):
        """Adiciona uma resposta à análise agregada"""
        if pergunta_id not in self.analise:
            self.analise[pergunta_id] = {}

        if resposta not in self.analise[pergunta_id]:
            self.analise[pergunta_id][resposta] = 0

        self.analise[pergunta_id][resposta] += 1

    def calcular_percentual(self, pergunta_id: str, resposta: str) -> float:
        """Calcula percentual de uma resposta específica"""
        if pergunta_id not in self.analise or self.total_respostas == 0:
            return 0.0

        count = self.analise[pergunta_id].get(resposta, 0)
        return (count / self.total_respostas) * 100
