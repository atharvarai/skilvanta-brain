# This repository is a brain-template domain pack: the pack is the repository root.
PACK ?= .
# Signs and checks demo user tokens. A development-only value: set your own in production.
BRAIN_JWT_SECRET ?= dev-only-secret-not-for-production-0001
export BRAIN_JWT_SECRET
CLI = BRAIN_PACK=$(PACK) uv run python -m core.cli

.PHONY: install ingest run eval eval-retrieval traces audit token tools test check

install:
	uv sync

ingest:
	$(CLI) ingest

run:
	BRAIN_PACK=$(PACK) uv run uvicorn core.api.app:create_app --factory

eval:
	$(CLI) eval

eval-retrieval:
	$(CLI) eval --retrieval

traces:
	$(CLI) traces

audit:
	$(CLI) audit

# make token as=riya
token:
	@$(CLI) token $(or $(as),riya)

# make tools tool=get_course_progress args='{"course": "DSA"}' as=riya
tools:
	$(CLI) tools $(if $(tool),--call $(tool) --args '$(or $(args),{})') $(if $(as),--as $(as))

test:
	uv run pytest -q

check: test
	uv run ruff check .
