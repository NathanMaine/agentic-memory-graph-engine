from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .explain import explain
from .graph import load_graph
from .ingest import ingest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="amg", description="Agentic Memory Graph Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest events into a memory graph")
    ingest_parser.add_argument("--events", required=True, type=Path, help="Path to events JSON")
    ingest_parser.add_argument("--out", default=Path("out"), type=Path, help="Output directory (default: out)")

    explain_parser = subparsers.add_parser("explain", help="Explain a node in an existing graph")
    explain_parser.add_argument("--graph", required=True, type=Path, help="Path to graph.json")
    explain_parser.add_argument("--node", required=True, help="Node id to explain")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ingest":
        graph = ingest(args.events)
        args.out.mkdir(parents=True, exist_ok=True)
        graph_path = args.out / "graph.json"
        dot_path = args.out / "graph.dot"
        graph.to_json(graph_path)
        graph.to_dot_file(dot_path)
        print(f"Graph written to {graph_path}")
        print(f"DOT written to {dot_path}")
        return 0

    if args.command == "explain":
        message = explain(args.graph, args.node)
        print(message)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
