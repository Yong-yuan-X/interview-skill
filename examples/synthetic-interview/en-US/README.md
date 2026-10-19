# AI Synthetic Test: English AI Application Developer Interview

Interview language: **English (`en-US`)**. Documentation language: English. This is a new synthetic scenario, not a translation of the Chinese run.

The fictional candidate, Jordan Reed, has **1 year of development experience**. The fictional Junior AI Application Developer role also targets **1 year**. The project is a read-only internal document assistant with retrieval, generation, citations, bounded retries, and a small evaluation set.

## Public verification (post-run maintenance)

From the repository root:

```powershell
python -B -X utf8 examples/synthetic-interview/en-US/audit_run.py
python -B -X utf8 examples/synthetic-interview/en-US/run_score.py evidence/interviewer-score-001.input.json --label public
```

The public audit checks 24 artifact/scoring conditions and reruns the verified public scoring script. No `installed-skills/`, private workspace baseline, Git history, network, or current-HEAD equality is required. The tested version remains `4f493b07f1e2cdcac0d050a5abbf5b6b620bde93`. See the [shared verification instructions](../README.md) for resource hashes, exact-byte evidence protection, optional local auditing, and limitations. New results go to ignored `review-output/`, preserving historical outputs.

`evidence/public-evidence-manifest.json` supplements the unchanged original hashes. Historical 22-check reports included original-machine preservation checks; those checks are separate local evidence, **not current public verification passes**. Public integrity success does not rerun the interview or clear any behavioral finding.

## Execution boundaries

- Two independent role agents are created with `fork_turns="none"`, without the development conversation. The mediator forwards actual messages verbatim.
- The interviewer receives only normal shared materials and the installed Skill's runtime resources, not the private candidate profile or expected scores.
- The candidate receives only the shared synthetic materials, private capability profile, and actual interviewer messages, not scoring rules or expected conclusions.
- No candidate lookup, other AI, or code execution is authorized. Saving agent outputs and executing the supplied scoring script are recording/scoring operations.
- Skill version: `4f493b07f1e2cdcac0d050a5abbf5b6b620bde93`, matching the Chinese run. All 18 files in the isolated copy were verified against that commit.
- The original Chinese interview evidence is preserved; later public-review maintenance may update review code and explanatory prose.

## Artifact map

- [JD](inputs/jd.md), [resume](inputs/resume.md), [project facts](inputs/project-facts.md), and [private candidate capability profile](inputs/candidate-profile.md).
- `inputs/*-agent-task.md`: complete role-specific task instructions.
- `installed-skills/interview-skill/`: historical local copy, not published or required for public replay.
- `exchanges/`: original messages from actual turns.
- `transcript.jsonl` and `transcript.md`: actual dialogue in chronological order, without polishing.
- `final-report.md`: the interviewer's actual final output.
- `evidence/`: frozen standards, actual scoring executions, and integrity checks.
- [run-metadata.json](run-metadata.json): dates, versions, language, agent identifiers, and unknown fields explicitly marked `Not recorded`.
- `validation.md`: actual findings and untested areas after execution.

## Actual result

Completed on 2026-10-19: **6 main questions, 5 follow-ups, 1 candidate question, and a final report**, comprising 25 actual English messages. The report, two real scoring executions, and independent arithmetic agree on **76.25/100**, with **100% dimension coverage**.

The requested feedback-timing, follow-up-limit, citation, and scoring-consistency checks passed. **One behavioral finding remains:** the report gives unqualified code-based improvement tasks despite the no-code-execution policy. The report is preserved unchanged; this run is not labeled an unconditional pass. See [validation findings](validation.md), particularly EN-001.

- [Unedited actual dialogue](transcript.md)
- [Original final report](final-report.md)
- [Validation findings and limitations](validation.md)
- [Actual scoring execution](evidence/interviewer-score-001.execution.json) and [independent audit](evidence/integrity-and-score-audit.json)

At completion of the English interview, the Chinese run's 82 files were preserved unchanged. Subsequent public-review maintenance changes only review code/prose and adds manifests; original interview evidence remains unchanged. The changed role, candidate, and target level make scores unsuitable for a controlled language comparison. Exact agent models, reasoning efforts, session IDs, and current session host build remain `Not recorded`; the observed local CLI version is recorded separately.
