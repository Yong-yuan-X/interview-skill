"""Offline helpers for reviewing archived synthetic interviews with public resources."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys


TESTED_SHA = "4f493b07f1e2cdcac0d050a5abbf5b6b620bde93"
REPO = Path(__file__).resolve().parents[2]
RUNTIME_FILES = (
    "SKILL.md",
    "references/workflows.md",
    "references/questions.md",
    "references/evaluation.md",
    "references/scoring-input.md",
    "references/design-notes.md",
    "assets/report-template.md",
    "assets/rubrics.json",
    "scripts/score.py",
)


def read_json(path):
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def within(root, name):
    path = (root / name).resolve()
    path.relative_to(root.resolve())
    return path


def verify_runtime(run):
    """Compare public runtime text with the original pinned installation manifest.

    Only runtime source text permits Git CRLF/LF conversion. Raw interview
    evidence is always checked byte-for-byte elsewhere.
    """
    metadata = read_json(run / "run-metadata.json")
    snapshot = read_json(run / "evidence/installed-snapshot.json")
    if metadata["skill_commit_sha"] != TESTED_SHA or snapshot["skill_commit_sha"] != TESTED_SHA:
        raise ValueError("Tested version does not match the recorded pinned SHA")
    recorded = {entry["path"]: entry["sha256"] for entry in snapshot["files"]}
    files = []
    for name in RUNTIME_FILES:
        path = REPO / name
        data = path.read_bytes()
        canonical = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
        if canonical != recorded.get(name):
            raise ValueError("Public runtime differs from tested version: " + name)
        files.append({"path": name, "recorded_sha256": recorded[name],
                      "file_sha256": hashlib.sha256(data).hexdigest(),
                      "canonical_lf_sha256": canonical})
    return {"tested_commit_sha": TESTED_SHA, "files": files,
            "comparison": "Runtime text only: canonical LF; raw evidence: exact bytes"}


def execute_score(run, source):
    runtime = verify_runtime(run)
    command = [sys.executable, "-B", "-X", "utf8", str(REPO / "scripts/score.py"), str(source)]
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=REPO, capture_output=True)
    return runtime, result, {"command": command, "working_directory": str(REPO),
                             "started_at_utc": started,
                             "completed_at_utc": datetime.now(timezone.utc).isoformat(),
                             "exit_code": result.returncode}


def score_main(run):
    parser = argparse.ArgumentParser(description="Replay scoring using verified public runtime resources")
    parser.add_argument("input", help="Input path relative to this archived run")
    parser.add_argument("--label", choices=("interviewer", "parent", "public"), default="public")
    args = parser.parse_args()
    try:
        source = within(run, args.input)
        # Refuse changed runtime before executing it or recording a new result.
        verify_runtime(run)
        destination = run / "review-output"
        destination.mkdir(exist_ok=True)
        number = 1
        while any(destination.glob(f"{args.label}-score-{number:03d}.*")):
            number += 1
        stem = f"{args.label}-score-{number:03d}"
        snapshot = destination / (stem + ".input.json")
        snapshot.write_bytes(source.read_bytes())
        runtime, result, execution = execute_score(run, snapshot)
        stdout = destination / (stem + ".stdout.json")
        stderr = destination / (stem + ".stderr.txt")
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        execution.update({"scope": "public_scoring_replay", "runtime": runtime,
                          "source_input": source.relative_to(run).as_posix(),
                          "input_snapshot": snapshot.relative_to(run).as_posix(),
                          "input_sha256": digest(snapshot),
                          "stdout": stdout.relative_to(run).as_posix(),
                          "stderr": stderr.relative_to(run).as_posix()})
        record = destination / (stem + ".execution.json")
        record.write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary = {"execution": record.relative_to(run).as_posix(), "exit_code": result.returncode}
        if result.returncode == 0:
            output = json.loads(result.stdout.decode("utf-8"))
            summary.update({key: output[key] for key in ("score", "coverage_percent", "judgment_status")})
        print(json.dumps(summary, ensure_ascii=False))
        return result.returncode
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({"scope": "public_scoring_replay", "error": str(error)}), file=sys.stderr)
        return 2
