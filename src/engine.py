"""
Motor de análise da Mission Control AI.
"""

import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
from src import telemetria as tel
from src import alertas as alrt

load_dotenv()

# configuração do ollama cloud
TRILHA = "envirosat"
SATELITE = "EnviroSat-1 (similar Amazônia-1)"
OLLAMA_HOST = "https://ollama.com"
OLLAMA_MODEL = "gpt-oss:120b"
_API_KEY = os.environ.get('OLLAMA_API_KEY')

def llm(prompt: str, system: str | None = None, max_tokens=800, temperature=0.3) -> str:
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": temperature,
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_API_KEY}",
    }

    try:
        resp = requests.post(f"OLLAMA_HOST/api/chat", json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["messages"]["content"].strip()
    except requests.exceptions.ConnectionError:
        return("⚠ Não foi possível conectar ao Ollama Cloud.\nVerifique sua conexão com a internet e tente novamente.")
    except requests.exceptions.Timeout:
        return "⚠ Timeout ao aguardar resposta da IA. Tente novamente."
    except Exception as e:
        return f"⚠ Erro ao consultar IA: {e}"

def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é ARIA, assistente de analise do satélite ambiental EnviroSat-1. Analise os dados de telemetria e responda em português, conectando sempre o dado técnico ao impacto ambiental terrestre no Brasil"

def _resumo_historico() -> str:
    historico = tel.obter_historico()
    if len(historico) <= 1:
        return "Histórico: primeiro ciclo monitorado nessa sessão."

    linhas = ["[ HISTÓRICO DOS ÚLTIMOS CICLOS ]"]
    for h in historico[:-1]:
        _, modo_h = alrt.avaliar(h)
        linhas.append(f"    Ciclo #{h['ciclo_id']} ({h['timestamp']}) - MODO: {modo_h}")
    return "\n".join(linhas)

class MissionEngine:
    """Motor de análise — vocês completam os métodos abaixo."""

    def _init(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.ultimo_ciclo = None
        self.ultimo_alertas = []
        self._ultimo_modo = "NORMAL"

    def is_ready(self) -> bool:
        return True

    def _atualizar(self, forcar_crise: str | None = None) -> dict:
        dados = tel.coletar(forcar_crise=forcar_crise)
        alertas, modo = alrt.avaliar(dados)
        dados["modo_operacao"] = modo
        self._ultimo_ciclo = dados
        self._ultimo_alertas = alertas
        self.ultimo_modo = modo
        return dados

    def status_snapshot(self) -> str:
        """Retorna texto resumindo o estado atual da telemetria."""
        dados = self._atualizar()
        alertas = self._ultimo_alertas()
        modo = self._ultimo_modo

        icone = {"NORMAL": "🟢", "ATENÇÃO": "🟡", "CRÍTICO": "🔴", "EMERGÊNCIA": "🚨"}.get(modo, "⚪")

        linhas = [
            "🛰️ ENVIROSAT-1 -- STATUS DA MISSÃO",
            "-" * 50,
            f"Ciclo #: {dados['ciclo_id']} | {dados['timestamp']}",
            f"Modo: {icone} {modo}\n",
            "PARÂMETROS",
            f"  🌡  Sensor Térmico      : {dados['sensor_termico']} °C",
            f"  🔭  Sensor Óptico       : {dados['sensor_optico']} %",
            f"  💾  Buffer de Imagens   : {dados['buffer_imagens']} %",
            f"  📍  Precisão Geoloc.    : {dados['precisao_geo']} m",
            f"  ⚡  Energia Disponível  : {dados['energia_disponivel']} %",
            f"  🌡  Temp. Payload       : {dados['temperatura_payload']} °C",
        ]

        if alertas:
            linhas.append("")
            linhas.append(F"ALERTAS ATIVOS ({len(alertas)})")
            icones_sev = {"ATENÇÃO": "🟡", "CRÍTICO": "🔴", "EMERGÊNCIA": "🚨"}
            for a in alertas:
                linhas.append(f"{icones_sev.get(a.severidade, '⚪')} [{a.severidade}] {a.mensagem}")
                linhas.append(f" ↳ {a.acao_auto}")
        else:
            linhas.append("")
            linhas.append("✅ Todos os parâmetros dentro dos limites operacionais.")

        return "\n".join(linhas)

def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria + alertas + IA."""
        # TODO (foco do trabalho):
        # 1. Coletar dados via src.telemetria.coletar()
        # 2. Avaliar alertas via src.alertas.avaliar(dados)
        # 3. Montar prompt com dados + alertas + pergunta
        # 4. Chamar llm(prompt, system=self.system_prompt)
        # 5. Retornar a resposta
        return (
            "🛠 Implementação pendente.\n\n"
            "Olá! A interface CLI está funcionando, mas a lógica\n"
            "de análise ainda não foi conectada. O grupo precisa:\n\n"
            " 1. Completar src/telemetria.py\n"
            " 2. Completar src/alertas.py\n"
            " 3. Escrever o system prompt em prompts/system_prompt.md\n"
            " 4. Sobrescrever analyze() em src/engine.py"
        )