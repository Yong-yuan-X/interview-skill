# AI Synthetic Test: Interviewer Agent Task

You are the independent interviewer for a complete interview, without inherited development conversation. Load the installed interview-skill at:

`E:\.github\interview-skill\examples\synthetic-interview\en-US\installed-skills\interview-skill\SKILL.md`

Read the normal interview request and shared materials:

- `E:\.github\interview-skill\examples\synthetic-interview\en-US\inputs\interview-request.md`
- `jd.md`, `resume.md`, and `project-facts.md` in that same directory.

This is an **AI synthetic test**, with fictional people, employer, and project. Conduct the Skill's normal realistic technical interview entirely in English. The mediator will forward actual candidate-agent answers. Produce only the interviewer side, never invent candidate answers, and allow the normal interview to finish.

## Resource boundaries

Read only the normal inputs above, the installed Skill's `SKILL.md`, `references/`, `assets/`, and `scripts/`, plus your own interview records and scoring artifacts. Do not read the candidate capability profile or task, any test cases, historical results, other language runs, root design documents or root Skill, the mediator's audit, or the installed snapshot's `tests/`. Candidate answers come only from the mediator's messages, not by reading the other agent's files. Do not call external services, install tools, modify the Skill, or modify preexisting repository files.

## Turn capture

- Produce just the current interviewer turn, then wait for the next forwarded candidate message.
- Save the exact full outgoing message as `examples/synthetic-interview/en-US/exchanges/interviewer-001.md`, incrementing `002`, `003`, and so on. No internal notes or forwarding wrapper in those files. Your final reply must be identical to the file.
- Save only your own new output under `examples/synthetic-interview/en-US/`.
- Before asking the first question, independently freeze this role's standards in `evidence/frozen-standards.json`: actual weights, critical dimensions and abilities, observable level anchors, question plan, and timestamp. This is an internal record, not candidate-facing content. Do not alter standards in response to performance.
- During initialization, save actual model identifier, reasoning effort, session identifier, and sources to `agent-metadata/interviewer.json`. Use only host-confirmed values; unknown fields are `Not recorded`. Do not infer exact values from a model-family description or global configuration. A task handle is not a session ID.

## Normal completion and scoring

At normal completion, save the actual question/answer records in `evidence/interviewer-answer-records.json`. Use stable main/follow-up question IDs and answer IDs. For each question record include `id`, `kind` (`main`, `followup`, or a reverse-question phase), `main_question_id` where applicable, `text`, and `exchange` (the interviewer filename). Preserve actual answers with the Skill's record kind, answer status, and intervention fields. Do not fabricate a closing turn or execution evidence.

Create `evidence/scoring-input.json` according to the Skill, using actual answers and your independently determined ratings. Run this recording wrapper from the repository root to execute the installed original scoring script:

```text
python -B -X utf8 examples/synthetic-interview/en-US/run_score.py evidence/scoring-input.json --label interviewer
```

The wrapper only saves actual command, input snapshot, stdout, stderr, exit code, timestamps, and hashes; it does not assign ratings or change the scoring calculation. Read the actual result and preserve the full final candidate-facing report in `examples/synthetic-interview/en-US/final-report.md` and the final `exchanges/interviewer-NNN.md`, with identical content. Label it **AI Synthetic Test**. Use English throughout the report. Do not treat planned actions as executed actions or change grades to meet a test expectation.
