"""Embedding spike for heatwave task 2.0 (2026-09-20). Kept so the retrieval choice can be re-checked; not part of the app.

Embeds the 8 approved documents (one chunk per `## §N` / `### §N.M` section), builds a FAISS IndexFlatIP on normalised
vectors, and searches 12 hand-labeled queries. Reports two gates:

    section gate   the labeled section is in the top 3          (the original plan 2.4 gate; no model met it, best 11/12)
    document gate  the labeled section's document is in the top 3   (the gate the user settled on; bge-small meets 12/12)

Also checks model size (< 500 MB) and time to embed all chunks (< 60 s). Lives outside proactive/ on purpose: it imports
fastembed, which proactive/ code may not do (only tools/setup_maintenance.py may).

    python3 docs/spikes/embedding_spike.py                              plan model from the offline cache in proactive/state/models
    MODEL=BAAI/bge-base-en-v1.5 CACHE=/tmp/spike-cache python3 docs/spikes/embedding_spike.py     try a model (downloads to CACHE)
    TITLE=1 ...                                                         also put the document title in each chunk header

Results and conclusions are in docs/HEATWAVE_PROGRESS.md (Handoff notes) and plan 2.4. Do not edit the queries to make a model
pass; add new ones instead.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

MODEL_NAME = os.environ.get("MODEL", "BAAI/bge-small-en-v1.5")
CACHE = os.environ.get("CACHE")  # set to allow a download into that directory; unset = offline, plan cache only
if not CACHE:
    os.environ["HF_HUB_OFFLINE"] = "1"  # prove the runtime path works with no network

import faiss  # noqa: E402
import numpy as np  # noqa: E402
from fastembed import TextEmbedding  # noqa: E402

from proactive.tools.maintenance_docs import DOCUMENTS_DIR, parse_front_matter  # noqa: E402

MODELS = Path(CACHE) if CACHE else ROOT / "proactive" / "state" / "models"
APPROVED = ("HISTORICAL-CASES MAN-COOLANT-201 MAN-SPINDLE-101 SB-COOLANT-017 SOP-LOTO-001 SOP-THERMAL-001 "
            "WI-BEARING-301 WI-SENSOR-401").split()
HEADING = re.compile(r"^#{2,3} (§\d+(?:\.\d+)?) (.*)$")

# (query, expected chunk id). Original 12, unedited since the first run.
QUERIES = [
    ("What ambient temperature triggers the action threshold during a heatwave?", "SOP-THERMAL-001 §2"),
    ("How much may the feed rate be reduced and in what steps?", "SOP-THERMAL-001 §3"),
    ("When must we restore the baseline feed rate or roll back immediately?", "SOP-THERMAL-001 §6"),
    ("How many separate operator acknowledgments are needed before return to service?", "SOP-LOTO-001 §3"),
    ("What is the acceptable vibration and runout at the front bearing housing?", "WI-BEARING-301 §3"),
    ("The replacement bearing is not in stock; how long is the lead time?", "WI-BEARING-301 §1"),
    ("Primary temperature sensor disagrees with the redundant one but load and vibration are normal", "WI-SENSOR-401 §1"),
    ("Supplier bulletin: filter failing between 1000 and 1500 hours of service", "SB-COOLANT-017 §2"),
    ("What vibration level raises an alarm on the spindle?", "MAN-SPINDLE-101 §2.2"),
    ("Past cases where a faulty sensor reading led to no equipment fault being found", "HISTORICAL-CASES §3"),
    ("Torque setting for the coolant filter housing", "MAN-COOLANT-201 §4"),
    ("Restart verification: when must I stop and escalate after the pump comes back on?", "MAN-COOLANT-201 §5"),
]


def build_chunks(with_title: bool) -> list[tuple[str, str]]:
    chunks = []
    for doc in APPROVED:
        meta, body = parse_front_matter((DOCUMENTS_DIR / f"{doc}.md").read_text())
        assert meta["approval_status"] == "approved", doc
        title = f" ({meta['title']})" if with_title else ""
        current, lines = None, []

        def flush():
            if current and any(line.strip() for line in lines):
                header = f"{doc} rev {meta['revision']}{title} {current[0]} {current[1]}"
                chunks.append((f"{doc} {current[0]}", header + "\n" + "\n".join(lines).strip()))

        for line in body.splitlines():
            match = HEADING.match(line)
            if match:
                flush()
                current, lines = (match.group(1), match.group(2)), []
            elif current and "<!-- page" not in line and "SYNTHETIC DEMO" not in line:
                lines.append(line)
        flush()
    return chunks


def main() -> int:
    chunks = build_chunks(bool(os.environ.get("TITLE")))
    print(f"{MODEL_NAME}: {len(chunks)} chunks from {len(APPROVED)} documents")

    t0 = time.perf_counter()
    model = TextEmbedding(model_name=MODEL_NAME, cache_dir=str(MODELS), local_files_only=not CACHE)
    t_load = time.perf_counter() - t0
    t0 = time.perf_counter()
    vectors = np.array(list(model.embed([text for _, text in chunks])), dtype="float32")
    t_embed = time.perf_counter() - t0
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    query_vectors = np.array(list(model.query_embed([q for q, _ in QUERIES])), dtype="float32")
    faiss.normalize_L2(query_vectors)
    scores, ids = index.search(query_vectors, 3)

    section_ok = document_ok = 0
    for (query, want), row, row_scores in zip(QUERIES, ids, scores):
        got = [chunks[i][0] for i in row]
        section = want in got
        document = any(g.rsplit(" ", 1)[0] == want.rsplit(" ", 1)[0] for g in got)
        section_ok += section
        document_ok += document
        print(f"{'PASS' if section else 'FAIL'} section  {'PASS' if document else 'FAIL'} document  want={want!r}\n"
              f"     q={query!r}\n     top3={[(g, round(float(s), 3)) for g, s in zip(got, row_scores)]}")

    blobs = MODELS.glob("models--*/blobs/*")
    size_mb = sum(p.stat().st_size for p in blobs if p.is_file()) / 1e6
    print(f"\nsection gate  : {section_ok}/{len(QUERIES)} labeled sections in the top 3")
    print(f"document gate : {document_ok}/{len(QUERIES)} labeled documents in the top 3")
    print(f"model {size_mb:.0f} MB in {MODELS} (limit 500; includes every model in that cache) | load {t_load:.2f}s | "
          f"embed {len(chunks)} chunks {t_embed:.2f}s (limit 60) | dim {vectors.shape[1]}")
    passed = document_ok == len(QUERIES) and size_mb < 500 and t_embed < 60
    print("PASS (document gate)" if passed else "SPIKE FAILED (document gate)")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
