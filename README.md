# 🚀 Mission Control AI - EnviroSat + ATLAS

## Integrantes
- Caio Marinho Pereira — RM: 572873 — Turma: 1CCPH

## O que o projeto faz
O sistema consiste em um satélite que recebe dados ambientais, especialmente temperatura, e tira fotos de tal área, e uma Inteligência Artificial que, com esses dados, analisa as condições, atribui um nível de severidade para a situação e propõe ações.

## Persona atendida
As personas mais atendidas são:
* Engenheiro
* Coordenador de brigada de incêndio
* Analistas de compliance ambiental

## Tecnologias utilizadas
* Python 3.10+
* Ollama Cloud API (modelo gpt-oss:120b)
* Bibliotecas: ollama, python-dotenv, Rich, PyFiglet, random, datetime, pathlib

## Como executar
1. Clone o repositório
2. Entre no repositório: `cd MISSION_CONTROL_AI`
3. Crie o ambiente virtual:  
   Linux: `python -m venv .venv && source .venv/bin/active`  
   Windows CMD: `python -m venv .venv && .venv\Scripts\activate.bat`
4. Intale as dependências: `pip install -r requirements.txt`
5. Crie arquivo `.env` na raiz com:  
   Linux e Windows CMD: `echo OLLAMA_API_KEY=sua_chave_aqui > .env`
6. Execute: `python main.py`

## Demonstração
![Status normal da missão](assets/ futuro screenshot normal aqui)
![Status crítico com análise de IA](assets/ futuro screenshot de alerta aqui)

## System Prompt
[System Prompt](prompts/system_prompt.md)

## Cenários de testes demonstrados
1. Operação normal — todos os parâmetros dentro do range
2. Temperatura crítica — alerta + análise de IA
3. Baixa energia — resposta automatizada
4. Precisão geológica — alerta + resposta automatizada

## Limitações conhecidas
Fisicamente, sistema não considera perda de comunicação com a central e não especifica os possíveis danos a blindagem do satélite.  
Quanto ao software, a telemetria é completamente "fake", não há conexão com nada real (como APIs meteorológicas ou integração com INPE, IBAMA etc), e é totalmente dependente do Ollama Cloud.

## Vídeo de demonstração
🎥 [Assistir no YouTube](https://www.youtube.com/watch?v= Futuro link aqui)
