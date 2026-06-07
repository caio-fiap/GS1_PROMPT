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

    "precisao_geo": {
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

@dataclass
class Alerta:
    parametro: str
    valor: float
    severidade: str # atencao, critico, emergencia
    mensagem: str
    acao_auto: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# acoes automaticas (logica python, não prompt)
_ACOES = {
    "sensor_termico": {
        "ATENÇÃO": "Aumentando frequência de leitura térmica para 30s.",
        "CRÍTICO": "Protocolo FIRE-ALERT ativado: coordenadas registradas, notificação enviada ao INPE.",
        "EMERGENCIA": "MODO MÁXIMO: suspendendo outros sensores, priorizando mapeamento térmico contínuo.",
    },

    "sensor_optico": {
        "ATENÇÃO": "Iniciando recalibração automática do sensor óptico.",
        "CRÍTICO": "Reduzindo taxa de capturas. Alternando para modo monocromático.",
        "EMERGÊNCIA": "Desativando sensor óptico. Operando apenas com sensor térmico.",
    },

    "buffer_imagens": {
        "ATENÇÃO": "Priorizando downlink na próxima janela de passagem.",
        "CRÍTICO": "Comprimindo imagens no buffer (razão 4:1) para ganhar tempo.",
        "EMERGÊNCIA": "SUSPENDENDO NOVA CAPTURAS. Descartando imagens de menor prioridade.",
    },

    "precisao_geo": {
        "ATENÇÃO": "Solicitando sincronização com constelação GPS de referência.",
        "CRÍTICO": "Adicionando margem de incerteza de 60m nos metadados das imagens.",
        "EMERGÊNCIA": "Marcando imagens como NAO_CONFIAVEIS. Alertando operadores do INPE",
    },

    "energia_disponivel":{
        "ATENÇÃO": "Reduzindo potência de transmissão em 15%",
        "CRÍTICO": "MODO ECONOMIA ATIVADO: reduzindo eficiência de sistemas não-essenciais",
        "EMERGÊNCIA": "EMERGÊNCIA ENERGÉTICA: apenas sistemas vitais ativos. Reorientando painéis solares",
    },

    "temperatura_payload":{
        "ATENÇÃO": "Ativando dissipadores térmicos secundários",
        "CRÍTICO": "Reduzindo ciclo de operação do payload para 50%",
        "EMERGÊNCIA": "DESLIGANDO PAYLOAD para proteção. Resfriamento estimado: 20 min."
    },
}

_LABELS = {
    "sensor_termico": "Sensor Térmico",
    "sensor_optico": "Sensor Óptico",
    "buffer_imagens": "Buffer de Imagens",
    "precisao_geo": "Precisão de Geolocalização",
    "energia_disponivel": "Energia Disponível",
    "temperatura_payload": "Temperatura do Payload",
}

_UNIDADES = {
    "sensor_termico": "°C",
    "sensor_optico": "%",
    "buffer_imagens": "%",
    "precisao_geo": "m",
    "energia_disponivel": "%",
    "temperatura_payload": "°C",
}

def _classificar(parametro: str, valor:float) -> str | None:
    """Retorna severidade do alerta ou None se normal"""
    t = THRESHOLDS[parametro]

    if parametro in _CRESCENTES:
        if valor >= t["emergencia"]: return "EMERGÊNCIA"
        if valor >= t["critico"]: return "CRITICO"
        if valor >= t["atencao"]: return "ATENCAO"
    elif parametro in _DECRESCENTES:
        if valor <= t["emergencia"]: return "EMERGÊNCIA"
        if valor <= t["critico"]: return "CRITICO"
        if valor <= t["atencao"]: return "ATENCAO"

    return None

def avaliar(dados: dict) -> tuple:
    """Avalia todos os parametros e retorna (lista_alertas, modo_operacoa)"""

    alertas = []
    parametros = list(THRESHOLDS.keys())

    for param in parametros:
        valor = dados.get(param)
        if valor is None:
            continue

        severidade = _classificar(param, valor)
        if not severidade:
            continue

        unidade = _UNIDADES.get(param, "")
        label = _LABELS.get(param, param)
        mensagem = f"{label}: {valor}{unidade} - {severidade}"
        acao = _ACOES.get(param, {}).get(severidade, "Anomalia registrada")

        alertas.append(Alerta(
            parametro=param,
            valor=valor,
            severidade=severidade,
            mensagem=mensagem,
            acao_auto=acao,
        ))

    # pior severidade
    sevs = [a.severidade for a in alertas]
    if "EMERGENCIA" in sevs: modo = "EMERGÊNCIA"
    elif "CRITICO" in sevs: modo = "CRITICO"
    elif "ATENCAO" in sevs: modo = "ATENCAO"
    else: modo = "NORMAL"

    return alertas, modo

def alertas_para_prompt(alertas: list) -> str:
    """Formata alertas em texto para injetar no prompt"""

    if not alertas:
        return "Nenhum alerta ativo. Todos os parâmetros dentro dos limites operacionais"

    linhas = [f"==== ALERTAS ATIVOS ({len(alertas)}) ===="]
    for a in alertas:
        linhas.append(f"[{a.severidade}] {a.mensagem}")
        linhas.append(f"    -> Ação automática executada: {a.acao_auto}")
    return "\n".join(linhas)
