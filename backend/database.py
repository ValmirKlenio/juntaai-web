import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'respostas': [],
            'recursos_apoio': [
                {
                    'id': 1,
                    'nome': '190 - Central de Atendimento à Mulher',
                    'descricao': 'Atendimento 24h para denúncias e orientações',
                    'telefone': '180',
                    'tipo': 'emergencia',
                    'estado': 'BR'
                },
                {
                    'id': 2,
                    'nome': 'Delegacia da Mulher',
                    'descricao': 'Registro de boletim de ocorrência e medidas protetivas',
                    'telefone': '190',
                    'tipo': 'policial',
                    'estado': 'BR'
                },
                {
                    'id': 3,
                    'nome': 'CRAS - Centro de Referência de Assistência Social',
                    'descricao': 'Apoio psicológico e social gratuito',
                    'tipo': 'apoio',
                    'estado': 'BR'
                },
                {
                    'id': 4,
                    'nome': 'Casa da Mulher Brasileira',
                    'descricao': 'Atendimento humanizado e multiprofissional',
                    'tipo': 'apoio',
                    'estado': 'BR'
                }
            ]
        }

    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def salvar_resposta(self, respostas: Dict) -> bool:
        try:
            entrada = {
                'id': len(self.data['respostas']) + 1,
                'respostas': respostas,
                'timestamp': datetime.now().isoformat()
            }
            self.data['respostas'].append(entrada)
            self._save_data()
            return True
        except Exception as e:
            print(f"Erro ao salvar resposta: {e}")
            return False

    def obter_estatisticas(self) -> Dict:
        total = len(self.data['respostas'])
        if total == 0:
            return {
                'total_respostas': 0,
                'analise': {}
            }

        # Análise agregada
        analise = {}
        for resposta_obj in self.data['respostas']:
            for pergunta, resposta in resposta_obj['respostas'].items():
                if pergunta not in analise:
                    analise[pergunta] = {}
                if resposta not in analise[pergunta]:
                    analise[pergunta][resposta] = 0
                analise[pergunta][resposta] += 1

        return {
            'total_respostas': total,
            'analise': analise
        }

    def obter_recursos_apoio(self, estado: Optional[str] = None) -> List[Dict]:
        recursos = self.data['recursos_apoio']
        if estado:
            return [r for r in recursos if r['estado'] == estado or r['estado'] == 'BR']
        return [r for r in recursos if r['estado'] == 'BR']

db = Database()
