"""
Pipeline de análise com LLM.

Cada atualização regulatória é enviada a um modelo local servido pelo Ollama (via
endpoint OpenAI-compatible) que devolve um resumo jurídico objetivo, uma categoria,
um nível de urgência e o impacto prático para clientes. A saída é sempre um JSON
estruturado.
"""

import json
import re

from openai import OpenAI

SYSTEM_PROMPT = (
    "Você é um analista jurídico especializado em direito digital, proteção de dados "
    "e regulação de inteligência artificial no Brasil. Você apoia advogados de uma "
    "banca full service, resumindo atualizações regulatórias de forma objetiva e "
    "priorizando o que exige ação. Responda sempre e exclusivamente em JSON válido, "
    "sem texto fora do objeto JSON."
)

CATEGORIAS = (
    "Proteção de Dados (LGPD)",
    "Regulação de IA",
    "Concorrência",
    "Sistema Financeiro",
    "Internacional",
    "Outros",
)


def _build_user_prompt(item: dict) -> str:
    return (
        "Analise a atualização regulatória abaixo e retorne UM objeto JSON com "
        "exatamente estas chaves (valores em texto simples, nunca listas):\n"
        '- "resumo": 2 a 3 frases resumindo a atualização para um advogado ocupado.\n'
        f'- "categoria": UMA única string, a mais relevante, entre {list(CATEGORIAS)}.\n'
        '- "urgencia": exatamente uma palavra - "Alto", "Médio" ou "Baixo".\n'
        '- "justificativa_urgencia": 1 frase justificando o nível de urgência.\n'
        '- "impacto_pratico": 1 frase sobre o impacto prático para clientes da banca.\n\n'
        "Como decidir a urgência (escolha o nível mais alto que se aplica):\n"
        "- Alto: sanção JÁ aplicada; norma em vigor imediata; ou votação/decisão "
        "marcada para os próximos dias.\n"
        "- Médio: consulta pública aberta com prazo para contribuição; inquérito ou "
        "processo em curso sem dever imediato para clientes.\n"
        "- Baixo: nota técnica ou orientação informativa; decisão já encerrada que "
        "não cria novo dever imediato.\n\n"
        "Exemplos:\n"
        '- "multa aplicada pela ANPD" -> Alto.\n'
        '- "consulta pública aberta por 30 dias" -> Médio.\n'
        '- "nota técnica esclarecendo critérios, sem prazo" -> Baixo.\n\n'
        f"Órgão: {item['source']}\n"
        f"Título: {item['title']}\n"
        f"Descrição: {item['summary']}\n"
    )


def _normalize_analysis(analysis: dict) -> dict:
    """Torna a resposta do modelo robusta: coage listas em texto e limpa a urgência.

    Modelos menores às vezes devolvem `categoria` como lista ou `urgencia` com texto
    extra. Aqui garantimos strings simples para o relatório não vazar estruturas.
    """
    def _to_text(value) -> str:
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        return str(value).strip()

    categoria = _to_text(analysis.get("categoria", "Outros"))

    urgencia_raw = _to_text(analysis.get("urgencia", "Médio"))
    urgencia = "Médio"
    for nivel in ("Alto", "Médio", "Baixo"):
        if nivel.lower() in urgencia_raw.lower():
            urgencia = nivel
            break

    return {
        **analysis,
        "categoria": categoria,
        "urgencia": urgencia,
    }


def _extract_json(text: str) -> dict:
    """Extrai o objeto JSON da resposta do modelo, tolerando texto ao redor."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def analyze_item(client: OpenAI, model: str, item: dict) -> dict:
    """Analisa um único item e retorna o item enriquecido com a chave 'analysis'."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(item)},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    analysis = _normalize_analysis(_extract_json(response.choices[0].message.content))
    return {**item, "analysis": analysis}


def analyze_all(items: list[dict], api_key: str, base_url: str, model: str) -> list[dict]:
    """Roda o pipeline sobre todos os itens, sem deixar um erro derrubar o lote."""
    client = OpenAI(api_key=api_key, base_url=base_url)
    results: list[dict] = []
    total = len(items)

    for i, item in enumerate(items, start=1):
        print(f"      - ({i}/{total}) {item['source']}: {item['title'][:60]}...")
        try:
            results.append(analyze_item(client, model, item))
        except Exception as exc:  # noqa: BLE001 - queremos continuar o lote
            print(f"        ! falha ao analisar este item: {exc}")
            results.append(
                {
                    **item,
                    "analysis": {
                        "resumo": item["summary"],
                        "categoria": "Outros",
                        "urgencia": "Médio",
                        "justificativa_urgencia": "Análise automática indisponível (erro de API).",
                        "impacto_pratico": "Revisar manualmente.",
                        "erro": str(exc),
                    },
                }
            )
    return results
