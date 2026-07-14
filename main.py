"""
PK Tracker Regulatório (protótipo demo).

Fluxo:
    [1/3] Carrega atualizações regulatórias (dados de demo).
    [2/3] Analisa cada uma com um modelo local via Ollama (resumo, categoria, urgência).
    [3/3] Gera relatórios em JSON e Markdown na pasta output/.

Uso:
    python main.py            # roda o pipeline completo (modo demo)
    python main.py --demo     # idêntico ao acima (único modo por enquanto)
"""

import argparse
import os

from tracker.analyzer import analyze_all
from tracker.data import get_sample_items
from tracker.reporter import save_json, save_markdown

OUTPUT_DIR = "output"

# Padrões: modelo local servido pelo Ollama, via endpoint OpenAI-compatible.
# Não é preciso arquivo de configuração nem chave de API; roda out of the box.
# Para trocar de modelo/endpoint, exporte as variáveis de ambiente LLM_* (opcionais).
DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_API_KEY = "ollama"  # o Ollama ignora a chave, mas o SDK exige um valor
DEFAULT_MODEL = "llama3.2:1b"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PK Tracker Regulatório (protótipo demo)")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Roda com dados de demonstração (padrão e único modo por enquanto).",
    )
    return parser.parse_args()


def load_config() -> tuple[str, str, str]:
    """Resolve a configuração do modelo, com fallback para os padrões do Ollama.

    Sem nenhuma configuração, o projeto já roda contra o Ollama local. As variáveis
    de ambiente LLM_* (opcionais) permitem apontar para outro modelo ou endpoint.
    """
    api_key = os.getenv("LLM_API_KEY", DEFAULT_API_KEY)
    base_url = os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL)
    model = os.getenv("LLM_MODEL", DEFAULT_MODEL)
    return api_key, base_url, model


def main() -> None:
    parse_args()  # aceita --demo; não altera o fluxo por enquanto
    api_key, base_url, model = load_config()

    print("=" * 64)
    print(" PK Tracker Regulatório (protótipo demo)")
    print("=" * 64)

    print("\n[1/3] Carregando atualizações regulatórias...")
    items = get_sample_items()
    print(f"      {len(items)} atualizações carregadas.")

    print(f"\n[2/3] Analisando com IA (modelo: {model})...")
    analyzed = analyze_all(items, api_key=api_key, base_url=base_url, model=model)

    print("\n[3/3] Gerando relatórios...")
    json_path = save_json(analyzed, OUTPUT_DIR)
    md_path = save_markdown(analyzed, OUTPUT_DIR)

    print("\n" + "=" * 64)
    print(" Relatórios gerados:")
    print(f"   - JSON:     {json_path}")
    print(f"   - Markdown: {md_path}")
    print("=" * 64)


if __name__ == "__main__":
    main()
