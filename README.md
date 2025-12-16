# Agentic Memory Graph Engine

A graph-based memory layer for agent systems, capturing events,
decisions, entities, and relationships with explainable queries.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m amg.cli ingest --events examples/meeting.json --out out
python -m amg.cli explain --graph out/graph.json --node decision-1
```

Outputs: `out/graph.json` and `out/graph.dot`; `explain` prints a simple summary for the chosen node.
