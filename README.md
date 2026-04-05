# IA: Búsquedas — A* y Minimax

Trabajo Corto | Inteligencia Artificial | TEC  
Profesor: Kenneth Obando Rodríguez

## Descripción

Implementación de dos algoritmos clásicos de IA aplicados a juegos de mesa:

- **A\***: resolución automática de Peg Solitaire
- **Minimax**: agente para jugar Timbiriche (Dots and Boxes)

## Estructura

timbiriche/     → Algoritmo Minimax + poda Alpha-Beta
peg-solitaire/  → Algoritmo A* con heurística admisible

## Tecnologías

- Python 3
- Jupyter Notebook (compatible con Google Colab)
- Librerías: `copy`, `math`, `time`, `matplotlib`

## Ejecución

Abre el cuaderno correspondiente en Google Colab y ejecuta las celdas en orden.
.gitignore:
__pycache__/
*.pyc
.ipynb_checkpoints/
.DS_Store
Thumbs.db
*.egg-info/
dist/
build/
Comandos:
bashgit add README.md .gitignore timbiriche/.gitkeep peg-solitaire/.gitkeep
git commit -m "chore: estructura inicial del proyecto"
git push -u origin main