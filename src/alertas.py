"""
Módulo de alertas e decisões

Lógica em Python (não IA):
- ATENÇÃO: parâmetro fora do range normal
- CRÍTICO: situação exige resposta imediata
- EMERGÊNCIA: risco de perda de dados ou dano
"""

from dataclasses import dataclass, field
from datetime import datetime

# thresholds (limites) por parametro
THRESHOLDS = {
    "sensor_termico": {
        "atencao": 45.0,
        "critico": 60.0,
        "emergencia": 80.0,
    },

    "sensor_optico": {
        "atencao": 80.0,
        "critico": 60.0,
        "emergencia": 40.0,
    },

    "buffer_imagens": {
        "atencao": 60.0,
        "critico": 80.0,
        "emergencia": 95.0,
    },

    "precisao_geol": {
        "atencao": 30.0,
        "critico": 60.0,
        "emergencia": 120.0,
    },

    "enerdia_disponivel": {
        "atencao": 30.0,
        "critico": 20.0,
        "emergencia": 10.0,
    },

    "temperatura_payload": {
        "atencao": 35.0,
        "critico": 50.0,
        "emergencia": 65.0,
    },
}

# parametros onde quanto maior o valor, pior
_CRESCENTES = {"sensor_termico", "buffer_imagens", "precisao_geo", "temperatura_payload"}

#parametros onde quanto menor, pior
_DECRESCENTES = {"sesnor_optico", "energia_disponivel"}