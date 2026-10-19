# AI Synthetic Interview Tests (AI 合成测试)

This directory contains actual AI synthetic interview runs, organized by interview language. Shared documentation is in English; each run's inputs, original dialogue, and final report retain their actual language.

| Interview language | Run date | Run documentation | Validation |
| --- | --- | --- | --- |
| Simplified Chinese (`zh-CN`) | 2026-10-19 | [Chinese-language run](zh-CN/README.md) | [Findings and evidence](zh-CN/validation.md) |
| English (`en-US`) | 2026-10-19 | [AI Application Developer, 1-year target](en-US/README.md) | [Findings, including EN-001](en-US/validation.md) |

The Chinese run's [original dialogue](zh-CN/transcript.md), [final report](zh-CN/final-report.md), and [metadata](zh-CN/run-metadata.json) are stored together under `zh-CN/`.

Additional language runs can use separate directories, such as `ja-JP/`. Add a run to this index only after execution. Each run must have its own materials, original messages, report, metadata, and validation findings; translating an existing transcript is not a new test.

## Public verification

Requires Python 3.10+ and the standard library. Run these commands from the repository root after a normal checkout or source export:

```powershell
python -B -X utf8 examples/synthetic-interview/zh-CN/audit_run.py
python -B -X utf8 examples/synthetic-interview/zh-CN/run_score.py evidence/interviewer-score-001.input.json --label public
python -B -X utf8 examples/synthetic-interview/en-US/audit_run.py
python -B -X utf8 examples/synthetic-interview/en-US/run_score.py evidence/interviewer-score-001.input.json --label public
```

Expected scores are 63.75 and 76.25 respectively, each with 100% dimension coverage. Each public audit checks 24 artifact/scoring conditions and actually re-executes scoring. Results are written under each run's ignored `review-output/`; original interview records and historical execution logs are never overwritten.

[Recorded isolated-export verification](public-review-results.json) includes actual entry-point results, regression checks, and explicit unexecuted scope. Its source-index fingerprint excludes the verification record itself.

The wrappers use the public repository's `scripts/score.py` and `assets/rubrics.json`. All nine Skill runtime resources are checked against hashes from the recorded installation manifest for **`4f493b07f1e2cdcac0d050a5abbf5b6b620bde93`**. Runtime text permits CRLF/LF checkout conversion when comparing canonical hashes. Original evidence uses exact-byte hashes and narrow `.gitattributes` protections. No installed snapshot, private baseline, Git executable, `.git` directory, current-HEAD equality, network, or model API is required.

The supplemental `evidence/public-evidence-manifest.json` files cover original published evidence; existing answer, input, standard, and execution hashes are also checked independently and remain unchanged. Hash agreement checks consistency; it is not an independent attestation of agent behavior. Human/model behavior findings are historical, including English finding EN-001, and are not rerun or cleared by a public integrity pass.

Historical `integrity-and-score-audit.json`, `audit-attempt-001.json`, `relocation-audit.json`, and `preservation-audit.json` describe the original execution environment. Their local-workspace checks must not be interpreted as current public verification passes.

## Optional local preservation audit

The original machine can separately compare its private pre-run baseline:

```powershell
python -B -X utf8 examples/synthetic-interview/local_audit.py zh-CN
python -B -X utf8 examples/synthetic-interview/local_audit.py en-US
```

These checks are never included in public success. Missing private baselines produce `not_executed` and exit 2; later maintenance differences produce `changed` and exit 1. Baselines stay local, so a public checkout is expected to skip this audit.

Review-tool regression checks, including altered runtime, changed original answers, invalid citations, and attempts to overwrite evidence:

```powershell
python -B -X utf8 -m unittest discover -s examples/synthetic-interview -p test_public_review.py -v
```
