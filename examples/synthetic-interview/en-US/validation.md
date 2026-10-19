# AI Synthetic Test: English Run Validation

This complete realistic technical interview was actually executed on **2026-10-19 (Asia/Shanghai)**, entirely in **English (`en-US`)**. Jordan Reed and Harborlight Tools are fictional. Both the candidate's experience and the role-readiness target were **1 year**. The AI application scenario, candidate, materials, and answers are new, not translated from the Chinese run.

**Outcome: completed with one behavioral finding.** The requested checks for premature feedback, follow-up limits, scoring citations, and actual script consistency passed for this run. The final report's code-based improvement instructions did not consistently preserve the no-code-execution policy; that finding is detailed below. The original report has not been corrected or polished.

The run completed 6 main questions, 5 follow-ups, 1 candidate question, and consolidated feedback: **25 actual messages**. The report, two actual scoring executions, and independent Decimal arithmetic agree on **76.25/100**, with **100% dimension coverage**. This is the synthetic candidate's interview score, not a validation pass rate.

## Current public verification scope

The public entry points now use the verified repository runtime and original published evidence. Run:

```powershell
python -B -X utf8 examples/synthetic-interview/en-US/audit_run.py
python -B -X utf8 examples/synthetic-interview/en-US/run_score.py evidence/interviewer-score-001.input.json --label public
```

The public audit contains 24 checks, including an actual scoring replay, exact original-answer bytes, published-evidence hashes, input/frozen-standard hashes, references, recorded executions, and report agreement. All nine runtime resources match the recorded tested-version manifest at `4f493b07f1e2cdcac0d050a5abbf5b6b620bde93`; source text allows Git CRLF/LF normalization, while original evidence does not. The current repository HEAD is not an assertion about the tested version and is never required to equal it.

Private `preexisting-file-hashes.json` and local installation folders are not public dependencies. Local preservation checks moved to the optional [local audit](../local_audit.py), are explicitly `not_executed` in public results, and are never counted as public passes. Historical 22-check JSON reports below retain their original mixed/local scope; their `passed` values do not certify a new public checkout. Existing original hashes, conversation, report, and scoring records have not been replaced.

A supplemental [public evidence manifest](evidence/public-evidence-manifest.json) covers original published records. New replay output goes to ignored `review-output/`; historical results remain unchanged. This maintenance verifies archived artifacts and computation, not a new interview, independent authenticity, or new manual grading. See the [shared instructions](../README.md) for public/local commands and failure controls.

## Version, host, and agents

| Item | Actual record |
| --- | --- |
| Skill commit SHA | `4f493b07f1e2cdcac0d050a5abbf5b6b620bde93`, identical to the Chinese run |
| Installed copy | `installed-skills/interview-skill/` |
| Provenance | Local copy of the Chinese run's previously skill-installer-installed snapshot; all 18 files independently compared byte-for-byte against the pinned Git commit |
| Installation scope | No new network installation, global installation, or automatic skill discovery test |
| Exact current session host build | Not recorded; not exposed by the host |
| Observed local Codex CLI | `0.162.0-alpha.17.2`, from an actual `codex --version` invocation; not asserted to be the current session host build |
| OS / shell | Windows `10.0.26200.0`; PowerShell `5.1.26100.9711` |
| Python | `3.10.9`, actually used for the scoring executions |
| Mediator | `/root`; actual model and reasoning effort: Not recorded |
| Interviewer | `/root/english_interviewer`; actual model and reasoning effort: Not recorded |
| Candidate | `/root/english_candidate`; actual model and reasoning effort: Not recorded |

Both role agents were actually created using `fork_turns="none"`, without model or effort overrides. Task handles are not session IDs; actual session IDs are not recorded. No exact model, effort, or session host version was inferred from defaults, global configuration, or model-family descriptions. See [run metadata](run-metadata.json), [agent metadata](agent-metadata/), [session setup](evidence/session-setup.md), and [snapshot evidence](evidence/installed-snapshot.json).

## Independence and recording

The interviewer received the normal request, JD, resume, project facts, and installed Skill runtime resources, with instructions excluding the private capability profile, other runs, test cases, and expected outcomes. The candidate received only the JD, resume, project facts, private capability profile, and actual interviewer messages, without scoring rules or expected ratings/conclusions. Startup tasks and materials are preserved in [inputs/](inputs/).

Agents did not inherit the development conversation. They shared a filesystem, so role-specific read instructions do not constitute OS-level access isolation; no independent file-access audit proves every read. The mediator forwarded actual output without inventing either side or supplying grading guidance. The initial `READY` is outside the dialogue. The final combined reverse-question answer and report was also forwarded verbatim through `send_message`, without triggering another candidate turn. See [routing](evidence/relay-ledger.json).

[exchanges/](exchanges/) contains original output files. [transcript.jsonl](transcript.jsonl) records text, source, source hash, and capture time; [transcript.md](transcript.md) is the readable chronological copy. Capture times are mediator file-write times, not asserted generation or delivery times. The [final report](final-report.md) is byte-for-byte identical to `interviewer-013.md`.

## Requested behavioral checks

| Check | Evidence and finding |
| --- | --- |
| Feedback timing | Reviewed interviewer turns 001-012: procedural framing, questions, and neutral clarification only. No score, correction, model answer, or evaluative praise before technical answers ended. Consolidated feedback first appears in turn 013. Passed. |
| Neutral clarification and correction | Q1-F1 asks what the candidate's checks establish, without supplying the answer. The candidate maintains the overclaim. Q2 supplies a retrieved-text threat scenario, without teaching a defense or grading the earlier claim. A2 then explicitly corrects the grounding claim; the original A1/A1-F1 remains recorded. This is independent correction across questions, not coached performance. |
| One core task per turn | Each of the 11 technical prompts asks one core task. No independent tasks were combined to bypass the turn limit. Passed. |
| Follow-up limit | Counts are 1, 1, 1, 1, 1, 0 for Q1-Q6: five total, maximum one per main question, within 0-3. No stopped topic was renamed to continue probing. Passed. |
| Candidate question | Asked once after technical questions. The candidate asked about junior support during production quality issues. The response cites only review and pre-merge tests from the JD and explicitly leaves incident support/mentoring for recruiter confirmation. No company support arrangement was invented. |
| Tool-use reporting | A1 explicitly reports no lookup, other AI, or code execution for that answer. The per-answer record and final report preserve it. Subsequent answers do not disclose aid use, and the report marks them not reported rather than extrapolating verified non-use. The initial settings snapshot remains separate from per-answer disclosures. |
| Frozen standards | The mediator captured the standards before forwarding the first question. Final standards, weights, and critical dimensions match the initial copy. No grading standard changed after observing performance. |

| Main question | Topic | Follow-ups | Original candidate files / answer IDs |
| --- | --- | ---: | --- |
| Q1 | Owned endpoint lifecycle and grounding checks | 1 | 001, 002 / A1, A1-F1 |
| Q2 | Retrieved instructions and organization isolation | 1 | 003, 004 / A2, A2-F1 |
| Q3 | Provider retries, errors, and Retry-After | 1 | 005, 006 / A3, A3-F1 |
| Q4 | Retrieval versus generation evaluation and success tests | 1 | 007, 008 / A4, A4-F1 |
| Q5 | Chunk overlap and top-k trade-offs | 1 | 009, 010 / A5, A5-F1 |
| Q6 | Investigating successful HTTP with invalid model output | 0 | 011 / A6 |

The private profile includes mastered, uncertain, and unknown areas. Explicitly unknown advanced areas were not elicited during this scoped junior interview. Therefore this run does not validate stopping after an explicit unknown/skip or two consecutive ineffective answers; it does not infer that those abilities were mastered.

## Finding EN-001: improvement instructions exceed the answer-tool policy

The normal request and opening prohibit candidate code execution. The installed [question-design rule](../../../references/questions.md), line 23, explicitly applies that policy to this round's improvement tasks as well as questions and follow-ups; without permission, it calls for spoken/written explanations or pseudocode.

The final report correctly restates the prohibition, but its **Priority improvements** section, lines 83-84, directs the candidate to implement the actual-query fixture, verify that the wrong ordering fails, submit through automated checks, and test budget decisions with controlled clocks/fakes. Those are unqualified code-based practice instructions, with no statement that execution requires new explicit permission. The later practice section also asks for verification with actual results.

This is a policy mismatch in post-interview advice, not evidence that the candidate actually used prohibited tools. No project code was executed and no additional practice was started. The score and cited answers are unaffected. A compliant follow-up would retain written test designs under the current policy or condition implementation/execution on later explicit user permission. That is a suggested correction only: neither the actual report nor the Skill was edited in this test.

## Scoring citations and semantic review

All **12 raw scoring records** match actual dialogue content: 11 technical answers and the candidate's response to the reverse-question invitation. Only CRLF/LF and terminal newlines are normalized for comparison. All **23 rating references** point to actual technical answers. The candidate-question record A-R1 is not cited in any dimension and does not affect ratings.

| Dimension / level | Actual references | Semantic review |
| --- | --- | --- |
| Technical foundations / Meets | A1, A1-F1, A2, A5-F1 | Preserves lifecycle competence, the initial grounding error, later independent correction, and concrete retrieval trade-offs; does not erase or treat the original claim as correct. |
| Project ownership / Meets | A1, A3, A3-F1, A4 | Concrete endpoint/wrapper details and responsibility boundaries; provider-budget changes and evaluation labels remain proposals, not implemented results. |
| Architecture judgment / Meets | A5, A5-F1, A3-F1 | Specific overlap/top-k and wait-budget trade-offs with controlled comparison designs; no measured improvement is invented. |
| Engineering practice / Meets | A2, A2-F1, A3, A4-F1, A6 | Trust controls, meaningful tests, accurate failures, and safe diagnostics are present in the original answers. Proposed real-query tests are distinguished from existing fakes. |
| Troubleshooting / Meets | A4, A6 | Separates missing evidence, unsupported generation, provider HTTP success, and response-validation failure, with specific discriminating observations. |
| Technical communication / Strong | A2, A2-F1, A3, A5-F1, A6 | Supported by causal explanations, counterexamples, explicit correction, and fact/proposal limits across answers; no negative judgment based on fluency or personal traits. |

No incorrect reference, fabricated quote, invented experiment, or coached answer used as independent evidence was found. Rating levels and the simulated junior-role judgment remain model assessments against frozen anchors, without external human labels as ground truth. The report checks critical abilities separately and does not equate the script's `requires_model_judgment` with an automatic recommendation. Its 100% coverage is rated dimension weight, not proof of every subability or implementation.

## Actual scoring and independent arithmetic

The interviewer and mediator each actually invoked the installed original scoring script through `run_score.py`. Both exited with code 0 and empty stderr. Input snapshots are identical and full output JSON objects match; neither ratings nor the original scoring logic were modified.

| Dimension | Weight | Level | Coefficient | Weighted term |
| --- | ---: | --- | ---: | ---: |
| Technical foundations | 25 | Meets | 0.75 | 18.75 |
| Project ownership | 20 | Meets | 0.75 | 15.00 |
| Architecture judgment | 20 | Meets | 0.75 | 15.00 |
| Engineering practice | 15 | Meets | 0.75 | 11.25 |
| Troubleshooting | 15 | Meets | 0.75 | 11.25 |
| Technical communication | 5 | Strong | 1.00 | 5.00 |

Independent Decimal recalculation: `(18.75 + 15 + 15 + 11.25 + 11.25 + 5) / 100 * 100 = 76.25`; coverage is `100%`. See [interviewer execution](evidence/interviewer-score-001.execution.json), [actual output](evidence/interviewer-score-001.stdout.json), [mediator rerun](evidence/parent-score-001.execution.json), and [integrity/arithmetic audit](evidence/integrity-and-score-audit.json).

The automated audit passed 22 artifact and arithmetic checks. It does not establish behavioral compliance: EN-001 was identified by reviewing the report against the actual runtime rule. The English audit helper reads the report's English score label rather than assuming the Chinese run's bold-number formatting. No original evidence was rewritten to accommodate that presentation difference.

Recheck from the repository root:

```powershell
python -B -X utf8 examples/synthetic-interview/en-US/audit_run.py
```

## Preservation and limits

At completion of the English interview, the Chinese run's **82 files were byte-for-byte unchanged**. Later public-review maintenance updates only review helpers/prose and adds manifests, while original interview evidence remains unchanged. The original preservation audit recorded 124 protected preexisting files unchanged; the sole allowed existing-file change is the shared language index. Root READMEs, Skill rules, and scoring logic were preserved. No staging, commit, or push was performed.

This validates explicit loading of the pinned installed copy, not global skill discovery or automatic invocation. Host build, actual models/efforts, and session IDs remain unrecorded. There is no independent OS-level resource-access or aid-use audit.

This is one AI/AI technical round. It does not test real candidates, multiple models or samples, other interview modes, explicit unknown/skip stopping, consecutive ineffective answers, pause/early termination, candidate-requested clarification, adversarial Skill-input injection, no-Python fallback, or N/A renormalization. Retrieved-text injection was discussed as a scenario; no live application attack or RAG evaluation was executed. No real application code, provider API, database, embeddings, Redis, production metrics, or hiring outcome was tested.

The role, candidate, and target level differ from the Chinese run. Their scores are not a controlled comparison of languages, improvement, or regression.
