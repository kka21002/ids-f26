SHELL := /bin/sh

.DEFAULT_GOAL := help
.DELETE_ON_ERROR:

QUARTO ?= quarto
PYTHON ?= python3
QUARTO_ARGS ?=

.PHONY: help check-tools check render book presentations preview render-one \
	publish clean clean-output clean-cache

help: ## Show the available targets.
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\nTargets:\n"} \
		/^[a-zA-Z0-9_-]+:.*## / {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-tools: ## Verify that required command-line tools are available.
	@command -v "$(QUARTO)" >/dev/null 2>&1 || { \
		echo "Error: Quarto executable not found: $(QUARTO)" >&2; exit 1; }
	@command -v "$(PYTHON)" >/dev/null 2>&1 || { \
		echo "Error: Python executable not found: $(PYTHON)" >&2; exit 1; }

check: check-tools ## Run Quarto's installation and environment checks.
	$(QUARTO) check

render: book presentations ## Render the notes and all presentations.

book: check-tools ## Render the book pages.
	$(QUARTO) render $(QUARTO_ARGS)

presentations: check-tools ## Render all topic and final presentations.
	$(QUARTO) render topic --profile presentations $(QUARTO_ARGS)
	$(QUARTO) render final --profile presentations $(QUARTO_ARGS)

preview: check-tools ## Preview the book with live reload.
	$(QUARTO) preview $(QUARTO_ARGS)

render-one: check-tools ## Render one presentation specified by FILE.
	@test -n "$(FILE)" || { \
		echo "Error: set FILE to a presentation source file." >&2; \
		exit 2; }
	@test -f "$(FILE)" || { \
		echo "Error: file not found: $(FILE)" >&2; exit 2; }
	$(QUARTO) render "$(FILE)" --profile presentations $(QUARTO_ARGS)

publish: render ## Render and publish the complete site to GitHub Pages.
	$(QUARTO) publish gh-pages --no-render --no-prompt $(QUARTO_ARGS)

clean-output: ## Remove the rendered book.
	rm -rf -- _book

clean-cache: ## Remove Quarto caches and frozen computations.
	rm -rf -- .quarto _freeze topic/.quarto topic/_freeze final/.quarto final/_freeze

clean: clean-output clean-cache ## Remove all generated Quarto files.
