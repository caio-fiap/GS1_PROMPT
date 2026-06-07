"""
Gerador de banner ASCII art para Mission Control AI
"""

import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

# Gera as duas linhas do banner em ASCII art
BANNER_GS = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
BANNER_MC = pyfiglet.figlet_format("Mission Control AI", font="big")
BANNER_ENVIRO = pyfiglet.figlet_format("EnviroSat", font="big")

# Pinta em ciano (estilo Claude Code) e centraliza
console.print(Align.center(Text(BANNER_GS, style="bold #A855F7")))
console.print(Align.center(Text(BANNER_MC, style="bold #06B6D4")))
console.print(Align.center(Text(BANNER_ENVIRO, style="bold #A855F7")))

console.print(Align.center(Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",style="italic #8484A0")))