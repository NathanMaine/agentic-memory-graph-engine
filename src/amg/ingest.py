from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from .graph import Graph


def ingest(events_path: Path) -> Graph:
    payload = json.loads(events_path.read_text())
    events = payload.get("events", [])
    nodes = []
    edges = []

    previous_id: str | None = None
    for idx, event in enumerate(events, start=1):
        node_id = str(event.get("id", f"event-{idx}"))
        label = f"{event.get('speaker', 'unknown')}: {event.get('text', '')}".strip()
        node_type = event.get("type", "event")
        nodes.append({
            "id": node_id,
            "label": label,
            "type": node_type,
        })
        if previous_id:
            edges.append({"from": previous_id, "to": node_id, "label": "follows"})
        previous_id = node_id

    # Connect decisions to their referenced topics if provided
    for ref in payload.get("references", []):
        source = ref.get("from")
        target = ref.get("to")
        if source and target:
            edges.append({"from": source, "to": target, "label": ref.get("label", "refers_to")})

    return Graph(nodes=nodes, edges=edges)
