import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.append(str(SRC_ROOT))

from amg.cli import main  # noqa: E402


def test_ingest_and_explain(tmp_path):
    events = Path(__file__).parent / "fixtures" / "meeting.json"
    out_dir = tmp_path / "out"

    ingest_code = main(["ingest", "--events", str(events), "--out", str(out_dir)])
    assert ingest_code == 0

    graph_path = out_dir / "graph.json"
    assert graph_path.exists()

    data = json.loads(graph_path.read_text())
    target_node = data["nodes"][-1]["id"]

    explain_code = main(["explain", "--graph", str(graph_path), "--node", target_node])
    assert explain_code == 0
