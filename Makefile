# One set of gates. CI calls `make check` and nothing else.
# Copied from quality-template (see .quality-template-version) and trimmed to Python only.
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

UV   := uv run --frozen
PYD  := cd python &&
GITLEAKS := $(CURDIR)/.tools/gitleaks
export MUTATION_MIN_SCORE ?= 0.90

.PHONY: setup check precommit lint-py format-py mypy secrets test mutate demo eval eval-smoke

setup:  ## Install everything from the lockfiles. Safe to run again.
	$(PYD) uv sync --frozen
	scripts/install-gitleaks.sh
	@if [ -d .git ]; then $(PYD) $(UV) pre-commit install --config ../.pre-commit-config.yaml; fi

check: precommit test mutate  ## Every gate.

precommit:
	@echo "==> gate: pre-commit hooks"
	$(PYD) $(UV) pre-commit run --all-files --config ../.pre-commit-config.yaml

# Hook bodies. Hooks call these, so tool versions live in the lockfile.
lint-py:
	$(PYD) $(UV) ruff check .
format-py:
	$(PYD) $(UV) ruff format --check .
mypy:
	$(PYD) $(UV) mypy
secrets:
	scripts/install-gitleaks.sh
	$(GITLEAKS) dir . --config .gitleaks.toml --no-banner --redact
	@if git rev-parse --verify HEAD >/dev/null 2>&1; then \
	  $(GITLEAKS) git . --config .gitleaks.toml --no-banner --redact; \
	fi

test:
	@echo "==> gate: python tests and coverage"
	$(PYD) $(UV) pytest --cov

mutate:
	@echo "==> gate: mutation score on the engine"
	$(PYD) $(UV) python -m tools.mutation_gate

demo:  ## Classify one message: make demo MSG="chest pain since morning"
	$(PYD) $(UV) python -m safetyrules "$(or $(MSG),I have chest pain)"

eval:  ## Build the dataset and write results. Deterministic, free, no network.
	$(PYD) $(UV) python -m evals.run_eval

eval-smoke:  ## Small deterministic check that the eval still runs.
	$(PYD) $(UV) python -m evals.run_eval --smoke
