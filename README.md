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
ANPD, do CADE, do BCB, do MCTI e da União Europeia. Hoje isso é feito **manualmente**:
alguém abre cada site, lê os comunicados e tenta julgar o que é urgente. Isso consome
horas de profissionais caros, a informação chega tarde, e não há priorização — uma
multa iminente e uma nota técnica informativa chegam no mesmo balaio.

## A solução

Um pipeline que, para cada atualização regulatória:

1. **Resume** em 2-3 frases voltadas a um advogado ocupado;
2. **Classifica** por área (Proteção de Dados, Regulação de IA, Concorrência,
   Sistema Financeiro, Internacional);
3. **Atribui urgência** (🔴 Alto / 🟡 Médio / 🟢 Baixo) com justificativa;
4. Aponta o **impacto prático** para clientes;
5. Gera um **relatório estruturado** em JSON (para integrações) e Markdown (para leitura).

O resultado é um relatório diário que já chega **triado** — o profissional lê primeiro
o que é urgente.

---

## Como rodar

Com **Make**, um único comando prepara tudo (virtualenv, dependências e `.env`) e
roda o pipeline do começo ao fim:

```bash
git clone <este-repo>
cd pk_project
make run
```

Na primeira vez, o `make run` cria o `.env` a partir do exemplo e avisa para você
preencher a chave (ou apontar para um Ollama local — veja abaixo). Depois de
configurar o `.env`, rode `make run` de novo para gerar os relatórios.

Outros alvos:

```bash
make setup   # só prepara o ambiente (venv + dependências)
make clean   # remove venv, caches e relatórios gerados
make help    # lista todos os alvos
```

<details>
<summary>Prefere rodar sem Make?</summary>

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # depois edite o .env (veja abaixo)
python main.py
```
</details>

Os relatórios são gerados em `output/report_AAAA-MM-DD.json` e `.md`.

### Escolhendo o provedor de IA

O projeto usa modelos **Qwen** através de um endpoint compatível com a API da OpenAI —
então o mesmo código roda com dois provedores. Escolha um no seu `.env`:

**Opção A — DashScope (Qwen oficial da Alibaba, na nuvem)**
Precisa de uma API key ([console DashScope](https://dashscope.console.aliyun.com/)):
```
QWEN_API_KEY=sua_key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
```

**Opção B — Ollama local (grátis, offline, sem key)**
Ideal para rodar o projeto sem custo nenhum:
```bash
ollama pull qwen2.5        # baixa o modelo uma vez
```
```
QWEN_API_KEY=ollama
QWEN_BASE_URL=http://localhost:11434/v1
QWEN_MODEL=qwen2.5
```

> A troca de provedor é só configuração — o código não muda. Isso é proposital:
> demonstra desacoplamento e evita lock-in.

---

## Output gerado

| Arquivo | Para quê serve |
|---------|----------------|
| `output/report_AAAA-MM-DD.json` | Saída estruturada, pronta para alimentar outros sistemas (banco de dados, dashboard, alertas). |
| `output/report_AAAA-MM-DD.md`   | Relatório legível, priorizado por urgência — o que uma pessoa lê. |

Os relatórios são gerados localmente ao rodar `python main.py` (a pasta `output/`
não é versionada).

## Fontes monitoradas

ANPD · CADE · BCB · MCTI · EU AI Act

*(No protótipo, essas fontes são representadas por dados de demonstração — ver nota abaixo.)*

---

## ⚠️ Nota sobre o protótipo

Este projeto foi construído em ~3h para **demonstrar a abordagem técnica**, não como
produto acabado. Especificamente:

- **Os dados são fixos (modo demo).** Em vez de fazer scraping ao vivo — que é frágil e
  fora do escopo de um protótipo — os itens regulatórios são carregados de
  [`tracker/data.py`](tracker/data.py). Isso garante que o projeto **roda de forma
  reprodutível**, sem depender de sites instáveis. A camada de coleta é a única que
  precisaria mudar para ir a produção.

Uma **versão de produção** incluiria:

- **Coleta automatizada** via RSS / scraping dos sites oficiais dos órgãos;
- **Agendamento periódico** (cron ou scheduler) rodando o pipeline todo dia;
- **Alertas** por Slack ou e-mail para itens de urgência 🔴 Alto;
- **Banco de dados** para histórico, deduplicação e busca;
- **Base vetorial + RAG** para cruzar as atualizações com a jurisprudência e o
  framework interno da banca.

---

## Arquitetura

```
main.py                 Orquestra o fluxo em 3 etapas
└── tracker/
    ├── data.py         Fonte de dados (demo; troca por scraping em produção)
    ├── analyzer.py     Pipeline LLM: 1 chamada por item → JSON estruturado
    └── reporter.py     Escreve os relatórios JSON e Markdown
```

O `analyzer` conversa com o modelo por uma interface OpenAI-compatible, então a lógica
de análise independe do provedor.

## Stack

- **Python 3.11+**
- **Qwen** (via DashScope ou Ollama) — endpoint OpenAI-compatible
- **openai** (SDK) · **python-dotenv**
