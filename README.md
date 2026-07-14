# 📋 PK Tracker Regulatório

Protótipo de um **tracker regulatório com IA**: coleta atualizações de órgãos
reguladores, resume cada uma em linguagem jurídica objetiva, classifica por área e
**prioriza por urgência** — entregando um relatório pronto para leitura.

> Construído como projeto de demonstração para a vaga de *Desenvolvedor Júnior — IA
> Aplicada* do **PK Advogados**, atacando diretamente o primeiro item da lista de
> projetos: *"Tracker regulatório automatizado com agentes que monitoram ANPD, CADE,
> BCB, MCTI, União Europeia e jurisprudência relevante."*

---

## O problema

Uma banca que atua em direito digital precisa acompanhar, todos os dias, o que sai da
ANPD, do CADE, do BCB, do MCTI e da União Europeia. Hoje isso costuma ser feito
**manualmente**: alguém abre cada site, lê os comunicados e tenta julgar o que é
urgente. Isso consome horas de profissionais caros, a informação chega tarde, e não há
priorização — uma multa recém-aplicada e uma nota técnica informativa chegam no mesmo
balaio.

## A solução

Um pipeline que, para cada atualização regulatória:

1. **Resume** em 2-3 frases voltadas a um advogado ocupado;
2. **Classifica** por área (Proteção de Dados, Regulação de IA, Concorrência,
   Sistema Financeiro, Internacional);
3. **Atribui urgência** (🔴 Alto / 🟡 Médio / 🟢 Baixo) com justificativa;
4. Aponta o **impacto prático** para clientes;
5. Gera um **relatório estruturado** em JSON (para integrações) e Markdown (para leitura).

O resultado é um relatório que já chega **triado** — o profissional lê primeiro o que
é urgente, em vez de garimpar site por site.

---

## Como rodar

O projeto roda **100% local e de graça**, sem chave de API e sem conta em nuvem. O
único requisito é o [Ollama](https://ollama.com) instalado. Com ele, um único comando
prepara tudo e executa o pipeline do começo ao fim:

```bash
git clone <este-repo>
cd pk_project
make run
```

É isso. O `make run` cria a virtualenv, instala as dependências, baixa o modelo (só na
primeira vez) e gera os relatórios em `output/`.

Outros alvos:

```bash
make setup   # só prepara o ambiente Python (venv + dependências)
make model   # só garante que o modelo do Ollama está baixado
make clean   # remove venv, caches e relatórios gerados
make help    # lista todos os alvos
```

<details>
<summary>Prefere rodar sem Make?</summary>

```bash
ollama pull llama3.2:1b          # baixa o modelo uma vez
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
</details>

---

## Exemplo de uso

Rodando o pipeline:

```console
$ make run
================================================================
 PK Tracker Regulatório — protótipo (modo demo)
================================================================

[1/3] Carregando atualizações regulatórias...
      8 atualizações carregadas.

[2/3] Analisando com IA (modelo: llama3.2:1b)...
      - (1/8) ANPD: ANPD aplica multa a empresa de marketing por uso irregular d...
      - (2/8) ANPD: Aberta consulta pública sobre decisões automatizadas e revis...
      - (3/8) CADE: CADE instaura inquérito sobre práticas em IA generativa...
      ...
      - (8/8) CADE: CADE aprova aquisição de startup de IA com compromissos volu...

[3/3] Gerando relatórios...

================================================================
 Relatórios gerados:
   - JSON:     output/report_2026-07-14.json
   - Markdown: output/report_2026-07-14.md
================================================================
```

Um item do relatório Markdown gerado (`output/report_AAAA-MM-DD.md`):

> ## 🔴 ANPD aplica multa a empresa de marketing por uso irregular de dados
>
> **Fonte:** ANPD  |  **Categoria:** Proteção de Dados (LGPD)  |  **Urgência:** 🔴 Alto
>
> A Autoridade Nacional de Proteção de Dados (ANPD) aplica sanção pecuniária à empresa
> de marketing digital por uso irregular de dados pessoais, sem base legal adequada e
> falha no atendimento a titulares.
>
> - **Impacto prático:** Os clientes da banca devem ser alertados sobre o tema e revisar
>   suas próprias bases legais de tratamento de dados.
> - **Por que esta urgência:** Sanção já aplicada — sinaliza fiscalização ativa da ANPD
>   sobre esse tipo de prática.
> - **Fonte original:** https://www.gov.br/anpd/pt-br/exemplo/multa-marketing

E o mesmo item na saída JSON (`output/report_AAAA-MM-DD.json`), pronta para integração:

```json
{
  "source": "ANPD",
  "title": "ANPD aplica multa a empresa de marketing por uso irregular de dados",
  "url": "https://www.gov.br/anpd/pt-br/exemplo/multa-marketing",
  "analysis": {
    "resumo": "A ANPD aplica sanção pecuniária à empresa de marketing digital por uso irregular de dados pessoais...",
    "categoria": "Proteção de Dados (LGPD)",
    "urgencia": "Alto",
    "justificativa_urgencia": "Sanção já aplicada — sinaliza fiscalização ativa.",
    "impacto_pratico": "Clientes devem revisar suas bases legais de tratamento."
  }
}
```

> **Sobre a qualidade da classificação:** o modelo padrão (`llama3.2:1b`) foi escolhido
> para **rodar em qualquer máquina** com um comando — é leve e rápido, mas conservador
> na urgência (tende a marcar itens como Alto). A triagem fica bem mais precisa com um
> modelo maior; veja *[Trocar de modelo](#trocar-de-modelo)*. Os resumos e categorias
> já saem consistentes mesmo no modelo leve.

---

## Como funciona

```
main.py                 Orquestra o fluxo em 3 etapas (carregar → analisar → relatar)
└── tracker/
    ├── data.py         Fonte de dados (demo; troca por scraping/RSS em produção)
    ├── analyzer.py     Pipeline LLM: 1 chamada por item → JSON estruturado + normalização
    └── reporter.py     Escreve os relatórios JSON e Markdown (ordenados por urgência)
```

- **`data.py`** entrega as atualizações a processar. Trocar a fonte (por scraping/RSS
  real) não afeta o resto do pipeline.
- **`analyzer.py`** monta um prompt com rubrica de urgência, chama o modelo via uma
  interface **OpenAI-compatible** e normaliza a resposta (garante que `categoria` e
  `urgencia` sejam sempre strings válidas, mesmo se o modelo desviar do formato). Uma
  falha em um item não derruba o lote — ele degrada com um marcador de erro.
- **`reporter.py`** gera dois artefatos: um JSON para consumo por máquina e um Markdown
  priorizado por urgência para consumo por pessoa.

Como o acesso ao modelo é por interface OpenAI-compatible, a lógica **independe do
provedor**: hoje aponta para o Ollama local; trocar para um modelo em nuvem é só mudar
as variáveis de ambiente, sem tocar no código.

### Trocar de modelo

Os padrões (Ollama local, modelo `llama3.2:1b`) estão no código e funcionam sem
configuração. Para usar outro modelo ou endpoint, basta exportar as variáveis:

```bash
# Um modelo local maior (triagem mais precisa; exige mais RAM):
export LLM_MODEL=llama3.2:3b

# Ou qualquer endpoint compatível com a API da OpenAI:
export LLM_BASE_URL=https://...
export LLM_API_KEY=sua_key
export LLM_MODEL=nome-do-modelo
```

---

## Por que um projeto desses é útil

- **Devolve horas de trabalho qualificado.** Monitorar cinco ou mais órgãos todos os
  dias é tarefa repetitiva que hoje ocupa advogados. O tracker faz a primeira passada e
  entrega o material já resumido e priorizado.
- **Reduz o risco de perder algo relevante.** Um prazo de consulta pública ou uma nova
  sanção que passa despercebida vira problema para o cliente. A triagem automática
  diminui esse ponto cego.
- **Padroniza a leitura.** Todo item chega no mesmo formato (resumo, categoria,
  urgência, impacto), o que facilita distribuir para as pessoas certas e comparar ao
  longo do tempo.
- **É a base de coisas maiores.** A saída estruturada em JSON é o insumo natural para
  alertas (Slack/e-mail), um dashboard, um histórico pesquisável ou um RAG que cruza as
  atualizações com a jurisprudência e o framework interno da banca.
- **Vira vantagem de produto.** Uma banca que responde a mudanças regulatórias mais
  rápido do que a concorrência transforma monitoramento em diferencial comercial.

---

## ⚠️ Nota sobre o protótipo

Este projeto foi construído em poucas horas para **demonstrar a abordagem técnica**, não
como produto acabado. Em particular:

- **Os dados são fixos (modo demo).** Em vez de fazer scraping ao vivo — frágil e fora
  do escopo de um protótipo — os itens vêm de [`tracker/data.py`](tracker/data.py). Isso
  garante que o projeto **roda de forma reprodutível**, sem depender de sites instáveis.
  A camada de coleta é a única que precisaria mudar para ir a produção.

Uma **versão de produção** incluiria:

- **Coleta automatizada** via RSS / scraping dos sites oficiais dos órgãos;
- **Agendamento periódico** (cron ou scheduler) rodando o pipeline todo dia;
- **Alertas** por Slack ou e-mail para itens de urgência 🔴 Alto;
- **Banco de dados** para histórico, deduplicação e busca;
- **Base vetorial + RAG** para cruzar as atualizações com a jurisprudência e o
  framework interno da banca.

---

## Fontes monitoradas (no modo demo)

ANPD · CADE · BCB · MCTI · EU AI Act

## Stack

- **Python 3.11+**
- **Ollama** servindo **`llama3.2`** localmente (endpoint OpenAI-compatible)
- **openai** (SDK) para falar com o modelo
- **Make** para orquestrar setup e execução
