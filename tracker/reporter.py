"""
Geração dos relatórios de saída.

Produz dois artefatos a partir dos itens já analisados:
- um JSON estruturado (para consumo por outros sistemas / integrações futuras);
- um Markdown legível, priorizado por urgência (o relatório que uma pessoa lê).
"""

import json
import os
from datetime import datetime

# Ordem de prioridade para ordenar e para a tabela-resumo.
_URGENCIA_ORDEM = {"Alto": 0, "Médio": 1, "Baixo": 2}
_URGENCIA_EMOJI = {"Alto": "🔴", "Médio": "🟡", "Baixo": "🟢"}


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def save_json(items: list[dict], output_dir: str) -> str:
    """Salva o relatório completo em JSON e retorna o caminho do arquivo."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"report_{_today()}.json")
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total": len(items),
        "items": items,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def _urgencia_de(item: dict) -> str:
    return item.get("analysis", {}).get("urgencia", "Médio")


def save_markdown(items: list[dict], output_dir: str) -> str:
    """Gera o relatório em Markdown, ordenado por urgência, e retorna o caminho."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"report_{_today()}.md")

    ordenados = sorted(items, key=lambda it: _URGENCIA_ORDEM.get(_urgencia_de(it), 1))

    # Contagem por nível de urgência para a tabela-resumo.
    contagem = {"Alto": 0, "Médio": 0, "Baixo": 0}
    for it in items:
        contagem[_urgencia_de(it)] = contagem.get(_urgencia_de(it), 0) + 1

    linhas: list[str] = []
    linhas.append("# 📋 Tracker Regulatório - Relatório Diário")
    linhas.append("")
    linhas.append(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  ")
    linhas.append(f"**Total de atualizações:** {len(items)}")
    linhas.append("")
    linhas.append("## Resumo por urgência")
    linhas.append("")
    linhas.append("| Urgência | Quantidade |")
    linhas.append("|----------|:----------:|")
    for nivel in ("Alto", "Médio", "Baixo"):
        emoji = _URGENCIA_EMOJI[nivel]
        linhas.append(f"| {emoji} {nivel} | {contagem.get(nivel, 0)} |")
    linhas.append("")
    linhas.append("---")
    linhas.append("")

    for it in ordenados:
        analysis = it.get("analysis", {})
        urgencia = analysis.get("urgencia", "Médio")
        emoji = _URGENCIA_EMOJI.get(urgencia, "🟡")

        linhas.append(f"## {emoji} {it['title']}")
        linhas.append("")
        linhas.append(
            f"**Fonte:** {it['source']}  |  "
            f"**Categoria:** {analysis.get('categoria', '-')}  |  "
            f"**Urgência:** {emoji} {urgencia}"
        )
        linhas.append("")
        linhas.append(f"{analysis.get('resumo', it['summary'])}")
        linhas.append("")
        linhas.append(f"- **Impacto prático:** {analysis.get('impacto_pratico', '-')}")
        linhas.append(
            f"- **Por que esta urgência:** {analysis.get('justificativa_urgencia', '-')}"
        )
        linhas.append(f"- **Fonte original:** [{it['url']}]({it['url']})")
        linhas.append("")
        linhas.append("---")
        linhas.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return path
