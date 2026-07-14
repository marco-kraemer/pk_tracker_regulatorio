"""
Fonte de dados do protótipo (modo demo).

Em produção, esta camada seria substituída por scraping / feeds RSS dos sites
oficiais dos órgãos reguladores. Aqui os itens são fixos para garantir que o
projeto rode de forma reprodutível, sem depender de rede nem de sites instáveis.

Os textos são fictícios/ilustrativos, mas escritos no estilo de comunicados reais
para exercitar de forma honesta o pipeline de análise.
"""

from datetime import datetime, timedelta


def _days_ago(days: int) -> str:
    """Retorna uma data ISO 8601 relativa a agora (para os itens não ficarem velhos)."""
    return (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")


def get_sample_items() -> list[dict]:
    """Retorna a lista de atualizações regulatórias que alimenta o tracker."""
    return [
        {
            "source": "ANPD",
            "title": "ANPD aplica multa a empresa de marketing por uso irregular de dados",
            "summary": (
                "A Autoridade Nacional de Proteção de Dados aplicou sanção pecuniária a "
                "empresa do setor de marketing digital pelo tratamento de dados pessoais "
                "sem base legal adequada e por falha no atendimento a titulares. É uma das "
                "primeiras multas de valor expressivo aplicadas pela autoridade."
            ),
            "url": "https://www.gov.br/anpd/pt-br/exemplo/multa-marketing",
            "published_at": _days_ago(1),
        },
        {
            "source": "ANPD",
            "title": "Aberta consulta pública sobre decisões automatizadas e revisão",
            "summary": (
                "A ANPD abriu consulta pública sobre a regulamentação do direito à revisão "
                "de decisões tomadas exclusivamente com base em tratamento automatizado de "
                "dados, incluindo perfilamento. Contribuições podem ser enviadas no prazo "
                "de 30 dias a partir da publicação."
            ),
            "url": "https://www.gov.br/anpd/pt-br/exemplo/consulta-decisoes-automatizadas",
            "published_at": _days_ago(3),
        },
        {
            "source": "CADE",
            "title": "CADE instaura inquérito sobre práticas em IA generativa",
            "summary": (
                "A Superintendência-Geral do CADE instaurou inquérito administrativo para "
                "apurar possíveis práticas anticompetitivas no mercado de modelos de "
                "inteligência artificial generativa, com foco em acordos de exclusividade "
                "de acesso a dados e infraestrutura de computação."
            ),
            "url": "https://www.gov.br/cade/pt-br/exemplo/inquerito-ia-generativa",
            "published_at": _days_ago(2),
        },
        {
            "source": "BCB",
            "title": "Banco Central publica consulta sobre uso de IA em concessão de crédito",
            "summary": (
                "O Banco Central do Brasil colocou em consulta pública proposta de norma "
                "que estabelece requisitos de governança, explicabilidade e mitigação de "
                "viés para instituições financeiras que utilizam modelos de inteligência "
                "artificial na análise e concessão de crédito."
            ),
            "url": "https://www.bcb.gov.br/exemplo/consulta-ia-credito",
            "published_at": _days_ago(6),
        },
        {
            "source": "MCTI",
            "title": "Texto-base do Marco Legal da IA avança e deve ser votado na próxima semana",
            "summary": (
                "O relatório do projeto de lei que institui o marco legal da inteligência "
                "artificial no Brasil foi apresentado e a votação está prevista para a "
                "próxima semana. O texto define categorias de risco, obrigações para "
                "sistemas de alto risco e responsabilidades de fornecedores e operadores."
            ),
            "url": "https://www.gov.br/mcti/pt-br/exemplo/marco-legal-ia",
            "published_at": _days_ago(1),
        },
        {
            "source": "EU AI Act",
            "title": "Comissão Europeia publica guia de conformidade para sistemas de alto risco",
            "summary": (
                "A Comissão Europeia divulgou orientações práticas sobre as obrigações "
                "aplicáveis a sistemas de IA classificados como de alto risco sob o AI Act. "
                "O documento afeta empresas brasileiras que oferecem produtos ou serviços "
                "de IA no mercado da União Europeia."
            ),
            "url": "https://digital-strategy.ec.europa.eu/exemplo/ai-act-guidance",
            "published_at": _days_ago(9),
        },
        {
            "source": "ANPD",
            "title": "ANPD publica nota técnica sobre transferência internacional de dados",
            "summary": (
                "A autoridade divulgou nota técnica esclarecendo critérios para a "
                "transferência internacional de dados pessoais, incluindo cláusulas-padrão "
                "contratuais e requisitos de nível adequado de proteção no país de destino. "
                "Não há prazo regulatório imediato associado."
            ),
            "url": "https://www.gov.br/anpd/pt-br/exemplo/nota-transferencia-internacional",
            "published_at": _days_ago(12),
        },
        {
            "source": "CADE",
            "title": "CADE aprova aquisição de startup de IA com compromissos voluntários",
            "summary": (
                "O Tribunal do CADE aprovou, sem restrições estruturais, a aquisição de uma "
                "startup de inteligência artificial por grande grupo de tecnologia, mediante "
                "compromissos voluntários de interoperabilidade. A decisão tem caráter "
                "majoritariamente informativo para o mercado."
            ),
            "url": "https://www.gov.br/cade/pt-br/exemplo/aquisicao-startup-ia",
            "published_at": _days_ago(15),
        },
    ]
