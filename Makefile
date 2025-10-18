.PHONY: help venv install run test cov validate data-check workflow fmt fmt-check lint lab streamlit fastapi clean

# Cross-platform venv bin path
VENV := .venv
ifeq ($(OS),Windows_NT)
  VENV_BIN := $(VENV)/Scripts
else
  VENV_BIN := $(VENV)/bin
endif

PY := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

# Defaults for app runners
APP ?= app.py
MODULE ?= app
APP_OBJECT ?= app
PORT ?= 8000

help:
	@echo "Targets:"
	@echo "  venv       - create .venv"
	@echo "  install    - install deps into .venv"
	@echo "  run        - run CLI exam (python -m src.main)"
	@echo "  test       - run pytest"
	@echo "  cov        - run pytest with coverage"
	@echo "  validate   - validate question bank"
	@echo "  data-check - validate and fail on coverage gaps (CI)"
	@echo "  workflow   - local workflow: install + strict validate + tests + coverage"
	@echo "  fmt        - format code (isort + black)"
	@echo "  fmt-check  - check format without writing"
	@echo "  lint       - run flake8"
	@echo "  lab        - launch JupyterLab"
	@echo "  streamlit  - run Streamlit app (APP?=$(APP))"
	@echo "  fastapi    - run FastAPI app (MODULE?=$(MODULE) APP_OBJECT?=$(APP_OBJECT))"
	@echo "  clean      - remove caches (keeps .venv)"
	@echo "  bundle     - bundle per-leaf questions into unified src/data/questions.json"
	@echo "  split      - split unified questions.json into per-leaf files"

venv:
	@[ -d $(VENV) ] || ( (command -v python3 >/dev/null 2>&1 && python3 -m venv $(VENV)) || python -m venv $(VENV) )

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: venv
	$(PY) -m src.main $(ARGS)

test: venv
	$(PY) -m pytest -q

cov: venv
	$(PY) -m pytest --cov=src --cov-report=term-missing

validate: venv
	$(PY) scripts/validate_questions.py

data-check: venv
	$(PY) scripts/validate_questions.py --strict-coverage

workflow: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PY) scripts/validate_questions.py --strict-coverage
	$(PY) -m pytest --cov=src --cov-report=term-missing --cov-report=html

fmt: venv
	$(VENV_BIN)/isort .
	$(VENV_BIN)/black .

fmt-check: venv
	$(VENV_BIN)/isort --check --diff .
	$(VENV_BIN)/black --check --diff .

lint: venv
	$(VENV_BIN)/flake8

lab: venv
	$(VENV_BIN)/jupyter lab

streamlit: venv
	@[ -f $(APP) ] && $(VENV_BIN)/streamlit run $(APP) || $(VENV_BIN)/streamlit hello

fastapi: venv
	$(VENV_BIN)/uvicorn $(MODULE):$(APP_OBJECT) --reload --port $(PORT)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

bundle: venv
	$(PY) scripts/bundle_questions.py

split: venv
	$(PY) scripts/split_questions.py
