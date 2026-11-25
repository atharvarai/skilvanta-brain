# Skilvanta Brain

The AI assistant for **Skilvanta**, a fictional ed-tech company that sells courses, pairs
learners with mentors and helps them get placed. **Skilvanta, its people and all its data
are fictional and synthetic.**

This repository is the company's whole brain, and it holds no AI code at all. It is a
domain pack for [brain-template](https://github.com/atharvarai/brain-template), which is
installed as a dependency:

```toml
dependencies = ["brain-template @ git+https://github.com/atharvarai/brain-template@v0.1.0"]
```

| What | Where |
|---|---|
| Which models, budgets, guardrails, cache, router and access settings | `brain.yaml` |
| Who the assistant is | `prompts/persona.v1.md` (the core adds the rules around it) |
| What it knows | `docs/`: 19 Markdown documents, two of them internal and one admin-only |
| Who may read and do what | `policy.yaml`: learner, mentor, support agent, admin |
| What it can do | `mcp_server/`: a demo stand-in for Skilvanta's backend (enrollments, progress, mentor slots, bookings, refunds) |
| How good it is | `evals/cases.jsonl`: 51 cases, run as demo users with real tokens |

The same pack lives in brain-template as `examples/edtech`, next to a second company built
without touching the core.

## Run it

Requires [uv](https://docs.astral.sh/uv/) and the Claude Code CLI (or Ollama: set
`BRAIN_MODEL_PROFILE=ollama`).

```bash
make install
make ingest                 # index the documents
make run                    # http://127.0.0.1:8000, demo chat page at /demo/
make -s token as=riya       # a token for the demo learner Riya; also arjun, sana, admin
make eval                   # every case, with the model
make eval-retrieval         # retrieval only, no model: what CI runs
```

## Results

From brain-template v0.1.0, through the Claude Code CLI:

- 50 of 51 eval cases pass. The failure is a Hinglish question that the English-only
  reranker cannot rank.
- 28 of 29 retrieval cases pass.
- An answer costs about $0.0034 at API list prices, with 94% of input tokens served from
  the prompt cache.

[Every measurement](https://github.com/atharvarai/brain-template/blob/main/docs/results.md)
and what it changed is in brain-template.

## Licence

MIT
