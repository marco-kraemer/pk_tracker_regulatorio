# PK Tracker Regulatório — automação de setup e execução.
#
# Uso mais comum:
#   make run     -> prepara tudo (venv + deps + .env) e roda o pipeline
#
# Outros alvos úteis:
#   make setup   -> só prepara o ambiente (venv + deps)
#   make env     -> cria o .env a partir do .env.example (se não existir)
#   make clean   -> remove venv, __pycache__ e relatórios gerados
#   make help    -> lista os alvos

VENV    := .venv
PYTHON  := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip

.DEFAULT_GOAL := help
.PHONY: run setup env clean help

## run: prepara o ambiente e roda o pipeline do começo ao fim
run: setup env
	@echo ">> Rodando o pipeline..."
	@$(PYTHON) main.py

## setup: cria a virtualenv e instala as dependências
setup: $(VENV)/.installed

$(VENV)/.installed: requirements.txt
	@echo ">> Criando virtualenv em $(VENV)/ e instalando dependências..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --quiet --upgrade pip
	@$(PIP) install --quiet -r requirements.txt
	@touch $(VENV)/.installed
	@echo ">> Ambiente pronto."

## env: cria o .env a partir do exemplo (se ainda não existir)
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ">> .env criado a partir de .env.example."; \
		echo ">> ATENÇÃO: edite o .env e preencha QWEN_API_KEY antes de rodar."; \
		echo "   (ou configure o Ollama local — veja o README)"; \
	else \
		echo ">> .env já existe, mantido."; \
	fi

## clean: remove venv, caches e relatórios gerados
clean:
	@echo ">> Limpando..."
	@rm -rf $(VENV) output __pycache__ tracker/__pycache__
	@echo ">> Limpo."

## help: lista os alvos disponíveis
help:
	@echo "Alvos disponíveis:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## /  /'
