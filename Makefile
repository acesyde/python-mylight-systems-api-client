.SILENT:

# CLI
PYTHON ?= $(shell which python3)
PIP ?= $(shell which pip)
PRECOMMIT ?= $(shell which pre-commit)
POETRY ?= $(shell which poetry)

# ******************************************************************
##@ Helpers

help:  ## Display this help
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[3mcommand\033[0m \n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# ******************************************************************
##@ Python tools

.PHONY: precommit-install
python-update: ## Poetry update
	$(POETRY) update

.PHONY: python-install
python-install: ## Install python dependencies
	$(POETRY) install

# ******************************************************************
##@ Pre-commit tools

.PHONY: precommit-install
precommit-install: ## Install precommit
	echo "########### Start pre-commit install ###########\n"
	$(PIP) install pre-commit

.PHONY: precommit-configure
precommit-configure: ## Configure precommit hooks
	echo "########### Start pre-commit configuration ###########\n"
	$(PRECOMMIT) install --install-hooks
	$(PRECOMMIT) install --hook-type commit-msg
