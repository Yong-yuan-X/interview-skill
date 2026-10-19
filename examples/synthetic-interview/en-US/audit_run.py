"""Audit saved AI synthetic-test artifacts; does not assign ability ratings."""

from collections import Counter
import argparse
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
COLLECTION = ROOT.parent
REPO = COLLECTION.parents[1]
sys.path.insert(0, str(COLLECTION))
from review_support import verify_runtime, execute_score


def read_json(path):
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def body(text):
    # Transport files may carry BOM/terminal CRLF; preserve all message content.
    return text.replace("\r\n", "\n").rstrip("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="review-output/public-audit.json",
                        help="Audit output path relative to this run directory")
    args = parser.parse_args()
    output_path = (ROOT / args.output).resolve()
    output_path.relative_to(ROOT)
    transcript = [json.loads(line) for line in
                  (ROOT / "transcript.jsonl").read_text(encoding="utf-8").splitlines()]
    metadata = read_json(ROOT / "run-metadata.json")
    snapshot = read_json(ROOT / "evidence/installed-snapshot.json")
    records = read_json(ROOT / "evidence/interviewer-answer-records.json")
    original = read_json(ROOT / "evidence/interviewer-score-001.input.json")
    parent_input = read_json(ROOT / "evidence/parent-score-001.input.json")
    first = read_json(ROOT / "evidence/interviewer-score-001.stdout.json")
    repeat = read_json(ROOT / "evidence/parent-score-001.stdout.json")
    frozen = read_json(ROOT / "evidence/frozen-standards-before-first-question.json")
    checks = []
    not_executed = [
        {"check": "local_workspace_preservation", "status": "not_executed", "reason": "Separate local_audit.py; private baseline is not a public dependency"},
        {"check": "interview_behavior_semantics", "status": "not_reexecuted", "reason": "Historical manual/model review in validation.md; this audit does not replay agents"},
    ]

    def check(name, passed, details):
        checks.append({"check": name, "passed": passed, "details": details})

    bad_sources = [row["source"] for row in transcript
                   if sha(ROOT / row["source"]) != row["sha256"] or
                   (ROOT / row["source"]).read_bytes().decode("utf-8-sig") != row["text"]]
    check("transcript_matches_original_messages", not bad_sources, bad_sources)
    check("chronological_sequence_and_alternation",
          [r["sequence"] for r in transcript] == list(range(1, len(transcript) + 1))
          and all(r["speaker"] == ("interviewer" if i % 2 == 0 else "candidate")
                  for i, r in enumerate(transcript)), {"messages": len(transcript)})
    prefix = '# AI Synthetic Test: Unedited Actual Interview\n\nMessages are copied verbatim from actual agent output files. Original wording, formatting, and errors are preserved; timestamps record mediator capture, not generation time.\n\n'
    md = ""
    for row in transcript:
        md += f"## {row['sequence']:02d} · {row['speaker']} · {row['source']}\n\n" + row["text"] + "\n\n"
    actual_md = (ROOT / "transcript.md").read_bytes().decode("utf-8")
    header, actual_body = actual_md.split("## 01 · ", 1)
    check("markdown_transcript_matches_log",
          header.replace("\r\n", "\n") == prefix and "## 01 · " + actual_body == md,
          "Harness header permits Windows CRLF. Message bodies and their line endings are compared exactly.")

    manifest = read_json(ROOT / "evidence/public-evidence-manifest.json")
    if manifest["tested_commit_sha"] != metadata["skill_commit_sha"]:
        raise ValueError("Evidence manifest and run metadata identify different tested versions")
    protected = manifest["files"]
    changed = [name for name, value in protected.items()
               if not (ROOT / name).is_file() or sha(ROOT / name) != value]
    check("published_original_evidence_unchanged", not changed,
          {"files": len(protected), "changed": changed})
    if (output_path.relative_to(ROOT).as_posix() in protected or
            output_path == ROOT / "evidence/public-evidence-manifest.json"):
        raise ValueError("Refusing to overwrite archived original evidence")
    altered_inputs = [name for name, value in metadata["input_sha256"].items()
                      if sha(ROOT / "inputs" / name) != value]
    check("prepared_inputs_unchanged", not altered_inputs, altered_inputs)
    try:
        runtime = verify_runtime(ROOT)
        runtime_valid = True
        check("public_runtime_matches_tested_version", True, runtime)
    except (OSError, ValueError, KeyError) as error:
        runtime_valid = False
        check("public_runtime_matches_tested_version", False, str(error))
    check("frozen_standards_unchanged",
          sha(ROOT / "evidence/frozen-standards.json") ==
          sha(ROOT / "evidence/frozen-standards-before-first-question.json"), {})
    check("frozen_standards_match_original_hash",
          sha(ROOT / "evidence/frozen-standards-before-first-question.json") ==
          (ROOT / "evidence/frozen-standards-initial-sha256.txt").read_text(encoding="utf-8").strip(), {})

    questions = {q["id"]: q for q in records["questions"]}
    bad_questions = [q["id"] for q in questions.values()
                     if body(q["text"]) not in body((ROOT / "exchanges" / q["exchange"]).read_bytes().decode("utf-8-sig"))]
    check("question_records_match_actual_messages", not bad_questions, bad_questions)
    followups = Counter(q["main_question_id"] for q in questions.values() if q["kind"] == "followup")
    mains = [q["id"] for q in questions.values() if q["kind"] == "main"]
    check("followup_limit", all(followups[q] <= 3 for q in mains),
          {q: followups[q] for q in mains})
    raw_candidates = [row for row in transcript if row["speaker"] == "candidate"]
    raw_by_question = {}
    for q in questions.values():
        source = "exchanges/" + q["exchange"]
        matches = [i for i, r in enumerate(transcript) if r["source"] == source]
        if matches and matches[0] + 1 < len(transcript):
            nxt = transcript[matches[0] + 1]
            if nxt["speaker"] == "candidate":
                raw_by_question[q["id"]] = nxt["text"]
    bad_answers = [a["id"] for a in original["answers"]
                   if a["record_kind"] != "raw" or a["question_id"] not in raw_by_question
                   or body(a["text"]) != body(raw_by_question[a["question_id"]])]
    check("score_answers_match_raw_dialogue", not bad_answers,
          {"scoring_answers": len(original["answers"]), "mismatches": bad_answers,
           "comparison": "Only terminal newlines and CRLF/LF are normalized; no words changed."})
    check("answer_ids_unique", len({a["id"] for a in original["answers"]}) == len(original["answers"]), {})
    answer_ids = {a["id"] for a in original["answers"]}
    invalid_refs = [(dim, ev["answer_id"]) for dim, rating in original["ratings"].items()
                    for ev in rating["evidence"] if ev["answer_id"] not in answer_ids]
    check("rating_references_exist", not invalid_refs, invalid_refs)
    technical_questions = {q["id"] for q in questions.values() if q["kind"] in ("main", "followup")}
    technical_answers = {a["id"] for a in original["answers"] if a["question_id"] in technical_questions}
    nontechnical_refs = [(dim, ev["answer_id"]) for dim, rating in original["ratings"].items()
                         for ev in rating["evidence"] if ev["answer_id"] not in technical_answers]
    check("ratings_use_technical_answers_only", not nontechnical_refs, nontechnical_refs)

    rubrics = read_json(REPO / "assets/rubrics.json")
    defaults = {d["id"]: d["weight"] for d in rubrics["interview_types"][original["interview_type"]]["dimensions"]}
    weights = original.get("weights", defaults)
    check("weights_match_frozen_standards", weights == frozen["weights"], weights)
    check("critical_dimensions_match_frozen_standards",
          original["critical_dimensions"] == frozen["critical_dimensions"], original["critical_dimensions"])
    denominator = Decimal(0)
    numerator = Decimal(0)
    terms = []
    for dim, rating in original["ratings"].items():
        if rating["level"] == "N/A" or rating["evidence_status"] != "sufficient":
            continue
        weight = Decimal(str(weights[dim]))
        coefficient = Decimal(str(rubrics["levels"][rating["level"]]["coefficient"]))
        denominator += weight
        numerator += weight * coefficient
        terms.append({"dimension": dim, "weight": str(weight), "level": rating["level"],
                      "coefficient": str(coefficient), "weighted_term": str(weight * coefficient)})
    score = ((numerator / denominator * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
             if denominator else None)
    check("independent_decimal_arithmetic",
          (score is None and first["score"] is None or score is not None and Decimal(str(first["score"])) == score)
          and Decimal(str(first["coverage_percent"])) == denominator,
          {"terms": terms, "numerator": str(numerator), "denominator": str(denominator),
           "score": str(score) if score is not None else None, "coverage_percent": str(denominator)})
    check("calculator_repeat_input_identical", original == parent_input, {})
    check("calculator_repeat_output_identical", first == repeat, {})
    executions = [read_json(ROOT / f"evidence/{label}-score-001.execution.json")
                  for label in ("interviewer", "parent")]
    recorded_runtime = {entry["path"]: entry["sha256"] for entry in snapshot["files"]}
    execution_errors = []
    for execution in executions:
        if (execution["exit_code"] != 0 or
            execution["input_sha256"] != sha(ROOT / execution["input_snapshot"]) or
            execution["script_sha256"] != recorded_runtime["scripts/score.py"] or
            execution["rubrics_sha256"] != recorded_runtime["assets/rubrics.json"] or
            (ROOT / execution["stderr"]).read_bytes() != b""):
            execution_errors.append(execution["label"])
    check("historical_execution_records_consistent", not execution_errors, execution_errors)
    check("score_source_matches_original_snapshot",
          read_json(ROOT / "evidence/scoring-input.json") == original, {})
    if runtime_valid:
        _, replay, replay_record = execute_score(ROOT, ROOT / "evidence/interviewer-score-001.input.json")
        replay_record.update({"stdout": replay.stdout.decode("utf-8"),
                              "stderr": replay.stderr.decode("utf-8")})
        same = replay.returncode == 0 and json.loads(replay.stdout.decode("utf-8")) == first
        check("actual_public_scoring_replay_matches_archive", same, replay_record)
    else:
        not_executed.append({"check": "actual_public_scoring_replay", "status": "not_executed",
                             "reason": "Refused to execute runtime that failed version verification"})
    check("final_report_is_actual_last_turn",
          (ROOT / "final-report.md").read_bytes().decode("utf-8-sig") == transcript[-1]["text"],
          {"last_source": transcript[-1]["source"]})
    report = (ROOT / "final-report.md").read_bytes().decode("utf-8-sig")
    reported_total = re.search(r"\bOverall score:\s*(\d+(?:\.\d+)?)\s*/\s*100\b", report)
    check("reported_total_matches_calculator",
          reported_total is not None and Decimal(reported_total.group(1)) == Decimal(str(first["score"])),
          {"calculator_score": first["score"],
           "reported_score": reported_total.group(1) if reported_total else None})

    output = {"test_label": "AI synthetic test", "audited_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "public_artifacts_and_scoring_only",
              "not_executed": not_executed,
              "passed": all(c["passed"] for c in checks), "checks": checks,
              "candidate_messages": len(raw_candidates)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scope": output["scope"], "passed": output["passed"], "checks": len(checks),
                      "failed": [c["check"] for c in checks if not c["passed"]],
                      "not_executed": not_executed, "output": str(output_path)}, ensure_ascii=False))
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({"scope": "public_artifacts_and_scoring_only", "error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
