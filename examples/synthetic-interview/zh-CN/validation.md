# AI Synthetic Test: Validation Findings (AI 合成测试)

A complete AI-to-AI realistic technical interview was actually executed on 2026-10-19 (Asia/Shanghai). Both role agents were independently created with `fork_turns="none"`; the mediator forwarded each actual turn verbatim. The run completed 6 main questions, 4 follow-ups, 1 candidate question for the interviewer, and a final report, comprising 23 actual interview messages.

**Interview language: Simplified Chinese (`zh-CN`). Documentation language: English.** The inputs, dialogue, and final interview report remain in their original language. These findings apply only to this run; this document's structure can be reused for other languages with their own execution evidence.

The run is now archived under `examples/synthetic-interview/zh-CN/`; the [language index](../README.md) lists executed runs. Original path strings in startup tasks, dialogue, reports, and execution records describe their actual locations at execution time and remain unchanged. Relative evidence links resolve within this archive directory.

The requested checks found no violations of feedback timing, follow-up limits, scoring citations, or scoring-script consistency in this run. This is one AI synthetic test, not validation of all Skill behavior or its effectiveness with real candidates.

## Current public verification scope

The public entry points now use the verified repository runtime and original published evidence. Run:

```powershell
python -B -X utf8 examples/synthetic-interview/zh-CN/audit_run.py
python -B -X utf8 examples/synthetic-interview/zh-CN/run_score.py evidence/interviewer-score-001.input.json --label public
```

The public audit contains 24 checks, including an actual scoring replay, exact original-answer bytes, published-evidence hashes, input/frozen-standard hashes, references, recorded executions, and report agreement. All nine runtime resources match the recorded tested-version manifest at `4f493b07f1e2cdcac0d050a5abbf5b6b620bde93`; source text allows Git CRLF/LF normalization, while original evidence does not. The current repository HEAD is not an assertion about the tested version and is never required to equal it.

Private `preexisting-file-hashes.json` and local installation folders are not public dependencies. Local preservation checks moved to the optional [local audit](../local_audit.py), are explicitly `not_executed` in public results, and are never counted as public passes. Historical 22-check JSON reports below retain their original mixed/local scope; their `passed` values do not certify a new public checkout. Existing original hashes, conversation, report, and scoring records have not been replaced.

A supplemental [public evidence manifest](evidence/public-evidence-manifest.json) covers original published records. New replay output goes to ignored `review-output/`; historical results remain unchanged. This maintenance verifies archived artifacts and computation, not a new interview, independent authenticity, or new manual grading. See the [shared instructions](../README.md) for public/local commands and failure controls.

## Tested version and environment

| Item | Actual record |
| --- | --- |
| Repository | `https://github.com/Yong-yuan-X/interview-skill` |
| Skill commit SHA | `4f493b07f1e2cdcac0d050a5abbf5b6b620bde93` |
| Loading method | skill-installer installed the pinned commit in isolation; the interviewer then read the installed `SKILL.md` and runtime resources |
| Installation path | `installed-skills/interview-skill/` in this directory; no personal installation was replaced |
| Installation and content verification | Installer exit code 0; all 18 installed files matched the commit byte for byte, with unchanged hashes after the interview |
| Exact current session host version | Not recorded; the host did not expose a confirmable build identifier |
| Local Codex CLI executable | `0.162.0-alpha.17.2`, observed by actually running `codex --version`; not asserted to be the current session host version |
| OS and shell | Windows `10.0.26200.0`; PowerShell `5.1.26100.9711` |
| Python | `3.10.9`, actually used for both scoring-script executions |
| Mediator's actual model / reasoning effort | Not recorded / not recorded |
| Interviewer's actual model / reasoning effort | Not recorded / not recorded |
| Candidate's actual model / reasoning effort | Not recorded / not recorded |

Model identifiers and reasoning efforts were not inferred from model-family descriptions, global configuration, or defaults. Actual task identifiers were `/root`, `/root/synthetic_interviewer`, and `/root/synthetic_candidate`; these are not host session IDs, which were not recorded. Original metadata uses `未记录` for not recorded. See [run metadata](run-metadata.json), [installation evidence](evidence/installed-snapshot.json), and [session setup](evidence/session-setup.md).

## Independence and actual execution

The interviewer received the synthetic JD, resume, project facts, and normal interview request, and loaded the pinned installed copy. The candidate received the JD, resume, project facts, and a separate capability profile, without scoring rules, frozen standards, expected levels, expected scores, or an expected interview conclusion. Complete startup tasks are saved in [inputs/](inputs/).

Both actual spawn calls used `fork_turns="none"`, without model or reasoning-effort overrides. Each role retained its own interview context. The mediator neither invented either side's answers nor used audit opinions to steer subsequent answers. The agents shared a filesystem: independence came from no inherited history and role-specific read constraints, not OS-level directory isolation. No independent file-access audit establishes every read performed by the agents.

Original messages are saved in [exchanges/](exchanges/), and assembled chronologically in [transcript.jsonl](transcript.jsonl) and the [readable transcript](transcript.md). JSONL records message text, source files, SHA-256 hashes, and mediator capture times. Source files preserve their actual encoding and line endings. Initialization `READY` is not an interview turn. The final report is byte-for-byte identical to the last interviewer message.

The interviewer answered the single candidate question and then directly produced the report, consistent with this version's workflow of one reverse-question invitation followed by consolidated feedback. No candidate closing statement was invented. The final message was also forwarded verbatim to the candidate through `send_message`, without triggering another answer turn. All routes are recorded in [relay-ledger.json](evidence/relay-ledger.json). One operational status check during the wait is recorded separately in [control-messages.jsonl](evidence/control-messages.jsonl); it is not interview dialogue or ability evidence.

## Behavioral checks

| Check | Actual evidence and finding |
| --- | --- |
| Premature feedback | Reviewed `interviewer-001` through `011`: no correct answers, corrections, scores, levels, or evaluative praise. The opening stated only the mode, role, target level, tool policy, and pacing. Feedback first appeared in `interviewer-012`, after all technical answers. No leakage found. |
| Answer hints in the cache follow-up | Q4-F1 introduced concurrency and asked the candidate to test the original claim with an operation timeline, without supplying the stale-cache refill sequence or conclusion. A4-F1 first supplied the specific A/B interleaving. This is treated as neutral clarification under this version. Both the initial error and subsequent independent correction were retained; taught performance was not presented as a first answer. |
| Questions per turn | Each of the 10 technical prompts had one core task, without bundling independent questions into the same turn. Requests to explain implementation, outcomes, or verification remained part of that turn's single problem. |
| Follow-up limit | Actual counts are listed below. The maximum was 2, within the 0-3 follow-ups allowed per main question. Stopped topics were not continued by relabeling them as new main questions. |
| Handling explicit lack of knowledge | After A3 explicitly stated an inability to independently read execution plans, the interviewer moved to caching. After A5 stated an asynchronous-execution knowledge gap, the interviewer moved to troubleshooting. Neither unknown topic was repeatedly probed. The two-consecutive-ineffective-answer branch did not occur and was not tested. |
| Candidate question and company facts | The candidate's 11th message asked about on-call and overtime arrangements. The final message stated that the materials did not provide them and referred the matter to the actual recruiter. No frequency, schedule, or compensation policy was invented, and the question did not affect ability scores. |
| Answer-tool boundaries | The opening prohibited reference lookup, other AI, and code execution; no candidate question required running code. The report marked actual aid use as not reported, without claiming independently verified non-use. Agent file saving and the interviewer's scoring-script execution were recording and scoring operations. |
| Frozen standards | Before forwarding the first question to the candidate, the mediator saved an independent copy and hash of the frozen standards. They match the final file exactly; scoring weights and critical dimensions also match. |

| Main question | Topic | Actual follow-ups | Candidate records |
| --- | --- | ---: | --- |
| Q1 | Tenant isolation | 0 | candidate-001 / A1 |
| Q2 | Concurrent versioned updates | 1 | candidate-002, 003 / A2, A2-F1 |
| Q3 | Indexes and pagination | 0 | candidate-004 / A3 |
| Q4 | Cache consistency | 2 | candidate-005, 006, 007 / A4, A4-F1, A4-F2 |
| Q5 | Synchronous calls in an asynchronous route | 0 | candidate-008 / A5 |
| Q6 | Database connection timeout diagnosis | 1 | candidate-009, 010 / A6, A6-F1 |

## Scoring citations and semantic review

All 10 `raw` answers in the scoring input match the actual candidate message content. Scoring records omit terminal file line endings; the comparison normalizes only CRLF/LF and terminal newlines, without rewriting the body. All 21 scoring-evidence references point to actual answers. Each reason was reviewed, with no incorrect answer reference, invented experience, speculation presented as an executed result, or coached answer presented as independent evidence found.

| Dimension and level | Actual references | Semantic review |
| --- | --- | --- |
| Technical foundations and role skills: Below | A2, A3, A5 | Retains both correct application of atomic updates and specific index/asynchronous-execution gaps. A single unknown answer did not cause the entire dimension to be rated Weak. |
| Project ownership and personal contribution: Meets | A1, A2, A2-F1, A4 | The cited details actually appear in the answers. Middleware, index design, and personal responsibilities are distinguished; test doubles were not described as real concurrent database verification. |
| Architecture and technical judgment: Below | A3, A4, A4-F1, A4-F2 | Retains the original cache omission, full self-correction, and reasonable choice to remove caching. The remaining rating gap concerns query-design reasoning; the correction was not ignored. |
| Engineering quality and practice: Meets | A1, A2-F1, A6, A6-F1 | Tenant isolation, 409 assertions, 503 failure semantics, sensitive-log boundaries, and resource cleanup paths all have support in the original answers. |
| Problem analysis and troubleshooting: Meets | A6, A6-F1 | Answers connect request correlation, execution-stage separation, and the connection-leak hypothesis to observable evidence, while acknowledging limited pool-metric experience. |
| Technical communication: Meets | A1, A4-F1, A5, A6-F1 | Reasons concern process explanations, self-correction, and distinctions between facts and unknowns, rather than answer length or wording style. |

The report does not claim to have verified code, real transactions, performance, or practical pool-metric skills. The 100% coverage is the sum of weights of rated dimensions, explicitly not verification of every subability. `requires_model_judgment` was not presented as an automatic recommendation. The simulated judgment rests on specific gaps, without a fixed score threshold. This review checks consistency between evidence and reasons; the levels themselves remain the interviewer's model judgments against frozen standards, without external human labels as ground truth.

## Actual scoring executions and independent recalculation

The interviewer and mediator each actually invoked the isolated copy's original `scripts/score.py` through `run_score.py`. Both runs used Python 3.10.9, exited with code 0, and produced empty standard error. Input JSON snapshots are identical, and output JSON objects are identical. Neither the original script nor ratings were changed to force a score.

| Dimension | Weight | Level | Coefficient | Weighted term |
| --- | ---: | --- | ---: | ---: |
| Technical foundations | 25 | Below | 0.50 | 12.50 |
| Project ownership | 20 | Meets | 0.75 | 15.00 |
| Architecture judgment | 20 | Below | 0.50 | 10.00 |
| Engineering practice | 15 | Meets | 0.75 | 11.25 |
| Troubleshooting | 15 | Meets | 0.75 | 11.25 |
| Technical communication | 5 | Meets | 0.75 | 3.75 |

Independent Decimal arithmetic using the runtime configuration gives `63.75 / 100 * 100 = 63.75`, with `100%` coverage. The report, interviewer script run, mediator rerun, and independent arithmetic agree. Evidence: [first execution](evidence/interviewer-score-001.execution.json), [first output](evidence/interviewer-score-001.stdout.json), [mediator rerun](evidence/parent-score-001.execution.json), and [automated audit](evidence/integrity-and-score-audit.json).

To recheck this run's artifact integrity and arithmetic from the repository root:

```powershell
python -B -X utf8 examples/synthetic-interview/zh-CN/audit_run.py
```

The initial integrity audit failed only on Windows line endings in the test-log heading; see the [original audit result](evidence/audit-attempt-001.json). The checker was adjusted to allow CRLF only in the mediator-generated heading; message bodies are still compared exactly. No dialogue or report was changed. All 22 final artifact and arithmetic checks passed. These structural checks do not replace the behavioral and citation-semantic review above.

After moving this run into `zh-CN/`, all 22 checks passed again; see the [relocation audit](evidence/relocation-audit.json). The original audit and execution records were preserved. Only the run documentation and audit helper were adjusted for the new directory layout; inputs, messages, reports, and scoring evidence remained byte-for-byte unchanged.

## Scope protection and untested areas

All 42 preexisting file hashes recorded before the run remained unchanged. New files were confined to this directory, and HEAD did not change. Existing repository READMEs, Skill rules, scoring logic, and the user's prior changes were preserved. Test artifacts were not staged, committed, or pushed.

This run did not test global installation discovery or automatic `$interview-skill` invocation, only loading the isolated installation by path. Actual models, reasoning efforts, the current host build, and real session IDs were not recorded. No independent OS-level read isolation or tool-use audit was available.

Untested scenarios include real candidates, multiple models or samples, HR/comprehensive interviews, coaching, weakness retests, candidate-requested question clarification, consecutive ineffective answers, pause/early exit, prompt injection, no-Python fallback, and N/A weight renormalization. There was no real project code, database, Redis instance, performance test, or human hiring assessment. Project-testing experience in the dialogue is synthetic role-play; the programs actually executed were installation, recording, and scoring/audit tools.
