# -------------------------------------------------
# Makefile — @astroai/backend
# -------------------------------------------------

.PHONY: help venv install install_dev lint format test test_unit test_integration install_hooks run run_dev run_front run_seeds clean
.DEFAULT_GOAL := help

# -------------------------------------------------
# Settings
# -------------------------------------------------
VENV_DIR  := .venv
UV        := uv

# Tools
PY        := $(UV) run python
PIP       := $(UV) pip
STREAMLIT := $(UV) run streamlit

HOST      ?= 0.0.0.0
PORT      ?= 8000

###################################################
help: ## Show this help
	@echo "Available commands:"; \
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

###################################################
# Environment
###################################################
venv: $(VENV_DIR)/pyvenv.cfg ## Create the virtualenv using uv

$(VENV_DIR)/pyvenv.cfg:
	$(UV) venv $(VENV_DIR)

###################################################
# Dependencies
###################################################
install: venv ## Installs the project dependencies.
	$(PIP) install -r pyproject.toml --extra dev

###################################################
# Quality
###################################################
lint: venv ## Lint with Ruff
	$(PY) -m ruff .

format: venv ## Format with Black
	$(PY) -m black .

test: venv ## Run all tests with coverage report
	$(UV) run pytest tests/ --cov=app --cov-report=term-missing

test_unit: venv ## Run only unit tests
	$(UV) run pytest tests/unit/ -v

test_integration: venv ## Run only integration tests
	$(UV) run pytest tests/integration/ -v

install_hooks: ## Install git hooks (pre-push test guard)
	@bash scripts/install_hooks.sh

###################################################
# Execution
###################################################
run: venv ## Start server
	$(PY) -m uvicorn app.api.server:app --host $(HOST) --port $(PORT)

run_dev: venv ## Start server in development mode (hot reload)
	$(PY) -m uvicorn app.api.server:app --host $(HOST) --port $(PORT) --reload

run_front: venv ## Start server in Streamlit
	$(STREAMLIT) run small_front.py

run_seeds: venv ## Start the seeds
	$(PY) -m app.seeds.run_seeds

###################################################
# Cleaning
###################################################
clean: ## Remove Python cache files
	find . -type f -name '*.py[co]' -delete -o -type d -name '__pycache__' -exec rm -r {} +