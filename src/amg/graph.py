from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class Graph:
    nodes: List[dict]
    edges: List[dict]

    def to_json(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2))

    def to_dot(self) -> str:
        lines = ["digraph MemoryGraph {"]
        for node in self.nodes:
            label = node.get("label", "")
            lines.append(f'  "{node["id"]}" [label="{label}"];')
        for edge in self.edges:
            label = edge.get("label", "")
            lines.append(f'  "{edge["from"]}" -> "{edge["to"]}" [label="{label}"];')
        lines.append("}")
        return "\n".join(lines)

    def to_dot_file(self, path: Path) -> None:
        path.write_text(self.to_dot())


def load_graph(path: Path) -> Graph:
    data = json.loads(path.read_text())
    return Graph(nodes=data.get("nodes", []), edges=data.get("edges", []))
