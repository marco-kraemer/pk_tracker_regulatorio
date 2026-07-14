# PK Tracker Regulatório - automação de setup e execução.
#
# Uso mais comum (clonou -> rodou -> pronto):
#   make run     -> prepara tudo (venv + deps + modelo local) e roda o pipeline
#
# Outros alvos úteis:
#   make setup   -> só prepara o ambiente Python (venv + deps)
#   make model   -> garante que o modelo do Ollama está baixado
#   make clean   -> remove venv, __pycache__ e relatórios gerados
#   make help    -> lista os alvos

VENV    := .venv
PYTHON  := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
MODEL   := llama3.2:1b

.DEFAULT_GOAL := help
.PHONY: run setup model clean help

## run: prepara o ambiente + modelo e roda o pipeline do começo ao fim
run: setup model
	@echo ">> Rodando o pipeline..."
	@$(PYTHON) main.py

## setup: cria a virtualenv e instala as dependências Python
setup: $(VENV)/.installed

$(VENV)/.installed: requirements.txt
	@echo ">> Criando virtualenv em $(VENV)/ e instalando dependências..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --quiet --upgrade pip
	@$(PIP) install --quiet -r requirements.txt
	@touch $(VENV)/.installed
	@echo ">> Ambiente pronto."

## model: garante que o Ollama está instalado e o modelo baixado
model:
	@command -v ollama >/dev/null 2>&1 || { \
		echo "ERRO: Ollama não encontrado."; \
		echo "Instale com:  curl -fsSL https://ollama.com/install.sh | sh"; \
		echo "(macOS/Windows: baixe em https://ollama.com/download)"; \
		exit 1; \
	}
	@echo ">> Garantindo o modelo '$(MODEL)' (baixa só na primeira vez)..."
	@ollama pull $(MODEL)

## clean: remove venv, caches e relatórios gerados
clean:
	@echo ">> Limpando..."
	@rm -rf $(VENV) output __pycache__ tracker/__pycache__
	@echo ">> Limpo."

## help: lista os alvos disponíveis
help:
	@echo "Alvos disponíveis:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## /  /'
