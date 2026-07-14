"""
PK Tracker Regulatório — protótipo (modo demo).

Fluxo:
    [1/3] Carrega atualizações regulatórias (dados de demo).
    [2/3] Analisa cada uma com um modelo Qwen (resumo, categoria, urgência).
    [3/3] Gera relatórios em JSON e Markdown na pasta output/.

Uso:
    python main.py            # roda o pipeline completo (modo demo)
    python main.py --demo     # idêntico ao acima (único modo por enquanto)
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from tracker.analyzer import analyze_all
from tracker.data import get_sample_items
from tracker.reporter import save_json, save_markdown

OUTPUT_DIR = "output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PK Tracker Regulatório (protótipo demo)")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Roda com dados de demonstração (padrão e único modo por enquanto).",
    )
    return parser.parse_args()


def load_config() -> tuple[str, str, str]:
    """Lê as variáveis do .env e valida a presença da API key."""
    load_dotenv()
    api_key = os.getenv("QWEN_API_KEY")
    base_url = os.getenv("QWEN_BASE_URL")
    model = os.getenv("QWEN_MODEL")

    if not api_key or api_key == "your_key_here" or not base_url or not model:
        print(
            "ERRO: configuração incompleta.\n"
            "Copie o arquivo de exemplo e preencha as variáveis:\n"
            "    cp .env.example .env\n"
            "Depois escolha um provedor (DashScope ou Ollama) no .env.",
            file=sys.stderr,
        )
        sys.exit(1)

    return api_key, base_url, model


def main() -> None:
    parse_args()  # aceita --demo; não altera o fluxo por enquanto
    api_key, base_url, model = load_config()

    print("=" * 64)
    print(" PK Tracker Regulatório — protótipo (modo demo)")
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
