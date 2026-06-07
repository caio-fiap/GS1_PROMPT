"""
Módulo de telemetria simulada
Satélite de observação ambiental

Parâmetros:
sensor_termico = temperatura do sensor (°C), detecta focos de calor
sensor_optico = saúde do sensor (%)
buffer_imagens = buffer das imagens transmitidas (%)   //armazena imagens temporariamente, antes dessas serem transmitidas
precisao_geo = erro de geolocalização (metros)
energia_disponivel = energia dos painéis solares (%)
temperatura_payload = temperatura interna do payload optico (°C)  //instrumentos que capturam espectros de luz e imagem
"""

import random
from datetime import datetime

RANGES_NORMAIS = {
    "sensor_termico": (18.0, 45.0),
    "sensor_optico": (80.0, 100.0),
    "buffer_imagens": (0.0, 60.0),
    "precisao_geo": (0.0, 30.0),
    "energia_disponivel": (30.0, 100.0),
    "temperatura_payload": (-10.0, 35.0),
}

# Historico dos ultimos ciclos (e memoria de contexto)
_historico: list = []
MAX_HISTORICO = 5

def _gerar_valor(parametro: str, forcar_crise: str | None = None) -> float:
    """Gera valor simulado - normal ou forçado em estado critico"""
    minimo, maximo = RANGES_NORMAIS[parametro]

    if forcar_crise == parametro:
        mapa_crise = {
            "sensor_termico": (65.0, 95.0),
            "sensor_optico": (20.0, 55.0),
            "buffer_imagens": (85.0, 99.0),
            "precisao_geo": (80.0, 200.0),
            "energia_disponivel": (5.0, 18.0),
            "temperatura_payload": (55.0, 80.0),
        }
        lo, hi = mapa_crise.get(parametro, (minimo * 1.5, maximo * 1.5))
        return round(random.uniform(lo, hi), 1)

    return round(random.uniform(minimo * 0.95, maximo * 0.98), 1)

def coletar(forcar_crise: str | None = None) -> dict:
    """Coleta (simula) um ciclo completo.
    Args: forcar_crise: nome do parametro para crie ou None para operacao normal
    Retorna: dict com todos os parametros e dados do ciclo
    """

    ciclo = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "ciclo_id": len(_historico) + 1,
        "sensor_termico": _gerar_valor("sensor_termico", forcar_crise),
        "sensor_optico": _gerar_valor("sensor_optico", forcar_crise),
        "buffer_imagens": _gerar_valor("buffer_imagens", forcar_crise),
        "precisao_geo": _gerar_valor("precisao_geo", forcar_crise),
        "energia_disponivel": _gerar_valor("energia_disponivel", forcar_crise),
        "temperatura_payload": _gerar_valor("temperatura_payload", forcar_crise),
        "modo_operacao": "NORMAL" #será atualizado por funcao em alertas
    }

    _historico.append(ciclo)

    if len(_historico) > MAX_HISTORICO:
        _historico.pop(0)
    return ciclo

def obter_historico() -> list:
    """retorna os últimos ciclos coletados"""
    return list(_historico)

def formatar_p_prompt(dados: dict) -> str:
    """Formata telemetria em texto para injetar no prompt"""

    def flag(ok: bool) -> str:
        return "✓ normal" if ok else "⚠  ANOMALIA"

    st = dados["sensor_termico"]
    so = dados["sensor_optico"]
    bi = dados["buffer_imagens"]
    pg = dados["precisao_geo"]
    ed = dados["energia_disponivel"]
    tp = dados["temperatura_payload"]

    return "\n".join([
        f"==== TELEMETRIA EnviroSat-1 -- Ciclo #{dados['ciclo_id']} ====",
        f"Timestamp: {dados['timestamp']}",
        f"Modo de Operação: {flag(dados['modo_operacao'])}\n",
        f"[ SENSORES ]",
        f"Sensor Térmico:       {st} °C       -{flag(st <= 45)}",
        f"Sensor Óptico:        {so} %        -{flag(so >= 80)}",
        f"Temperatura Payload:  {tp} °C       -{flag(tp <= 30)}\n",
        f"[ COMUNICAÇÃO E ARMAZENAMENTO ]",
        f"Buffer de Imagens:    {bi} %        -{flag(bi <= 60)}",
        f"Precisão Geológica:   {pg} m erro   -{flag(pg <= 30)}\n",
        f"[ ENERGIA ]"
        f"Energia Disponível:   {ed} %        -{flag(ed >= 30)}",
    ])
