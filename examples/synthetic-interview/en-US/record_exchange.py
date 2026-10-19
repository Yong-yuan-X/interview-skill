"""Append actual agent output files without rewriting their contents (AI synthetic test)."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("interviewer", "candidate"))
    parser.add_argument("source")
    parser.add_argument("--agent-id", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    source = (root / args.source).resolve()
    source.relative_to(root)
    data = source.read_bytes()
    text = data.decode("utf-8-sig")
    log = root / "transcript.jsonl"
    existing = []
    if log.exists():
        existing = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    relative = source.relative_to(root).as_posix()
    if any(row["source"] == relative for row in existing):
        raise ValueError("Exchange already recorded: " + relative)
    entry = {
        "sequence": len(existing) + 1,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "speaker": args.role,
        "agent_id": args.agent_id,
        "source": relative,
        "sha256": hashlib.sha256(data).hexdigest(),
        "source_has_utf8_bom": data.startswith(b"\xef\xbb\xbf"),
        "text": text,
    }
    with log.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    markdown = root / "transcript.md"
    if not markdown.exists():
        markdown.write_text('# AI Synthetic Test: Unedited Actual Interview\n\nMessages are copied verbatim from actual agent output files. Original wording, formatting, and errors are preserved; timestamps record mediator capture, not generation time.\n\n', encoding="utf-8", newline="\n")
    with markdown.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"## {entry['sequence']:02d} · {args.role} · {relative}\n\n")
        handle.write(text)
        handle.write("\n\n")
    print(json.dumps({"sequence": entry["sequence"], "speaker": args.role, "source": relative}))


if __name__ == "__main__":
    main()
