from __future__ import annotations

from pathlib import Path

from .graph import Graph, load_graph


def explain(graph_path: Path, node_id: str) -> str:
    graph = load_graph(graph_path)
    node = next((n for n in graph.nodes if n.get("id") == node_id), None)
    if not node:
        return f"Node {node_id} not found"

    inbound = [e for e in graph.edges if e.get("to") == node_id]
    outbound = [e for e in graph.edges if e.get("from") == node_id]

    parts = [f"Node {node_id}: {node.get('label', '')}"]
    parts.append(f"Inbound edges: {len(inbound)}")
    parts.append(f"Outbound edges: {len(outbound)}")
    return "; ".join(parts)
