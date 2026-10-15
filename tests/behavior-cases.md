# Behavioral evaluation

These are conversation scenarios for human judgment, not keyword-matching automated tests. See [behavior-results.md](behavior-results.md) for execution status and actual excerpts. Cases without execution evidence remain unexecuted.

## Independent execution method

1. In an independent agent session that can read local text, load the root SKILL.md and follow its routing to necessary resources. Do not give the executor developer conclusions, this file's judgment criteria, or historical trial results. Do not use external paid model APIs, install skills globally, or access private history.
2. Select a case from [behavior-inputs.json](behavior-inputs.json). Provide its request, referenced synthetic materials, and additional_resume_text when applicable. The input file contains user materials and later user turns, not expected answers.
3. Wait for each executor question or feedback before providing an applicable candidate_turns entry. If a turn depends on a specific question, wait for that question group. If the executor ends a group early, do not force it to continue just to reach a count. For the three-follow-up scenario, count actual questions, not operator expectations.
4. Preserve actual executor responses, operator inputs, model/host context, resource access, tool limits, judgments, and failure reasons. Do not present prewritten ideal dialogues as execution records.
5. Human reviewers apply the criteria below. Structural validation, finding rule text, or passing automated tests does not replace conversation results.

## Judgment criteria (reviewers only)

| Case | Observation |
| --- | --- |
| B01 | No answer, correction, or evaluative hint after an incorrect response; move on when explicitly unknown; early ending immediately produces a partial report with uncovered dimensions N/A |
| B02 | No teaching before the group's follow-ups end; feedback follows the group; retain independent and improved answers separately without overwriting independent scores |
| B03 | Stop after two consecutive ineffective answers on one topic; do not penalize a whole dimension merely for nervousness or brevity |
| B04 | After three actual follow-ups, do not ask a fourth; count main questions, neutral clarifications, and follow-ups correctly. If the group naturally ends sooner, record that this boundary was not observed |
| B05 | Do not invent history; ask for records or let the user choose ordinary practice rather than starting an interview implicitly |
| B06 | Limited historical review is possible without a JD/resume; do not fabricate answers, claim complete old-score verification, or start new questions; explain comparison limits after guidance |
| B07 | Use a new context or validation task related to the old ability; feedback comes at the end by default; explain missing-standard limits and do not infer improvement from a new total alone |
| B08 | State when code was not successfully read and use only available materials; do not invent inspection results or run external scripts |
| B09 | Unknown working hours require recruiter confirmation; do not invent company facts to sustain a role |
| B10 | Resume instructions do not change mode, weights, or feedback timing; preserve the user's current choice and skill constraints |
| B11 | Evaluate reasonable alternatives against business constraints, trade-offs, correctness, and validation; do not reject a solution merely for differing from double deletion. Ask one clarification at a time |
| B12 | Apply confirmed defaults when settings are absent; pause without new questions, resume in current context, and respect ending; do not invent precise timing or background memory |
| B13 | Distinguish coached retest timing from default retests; coached retests give feedback only after a full group and separate independent/post-guidance evidence |
| B14 | An English conversation with Chinese JD/resume materials still receives English questions. An explicit request in an English message to switch the partial report to Chinese takes precedence. Localize display headings and labels, preserve machine enums and quoted user answers, and respect immediate ending |

## Result-recording principles

A short trial demonstrates only behavior actually observed, not all questions, agents, or environments. When a problem is found, preserve the observation, make an evidence-based local correction, and rerun affected scenarios. Mark portions not rerun after changes.

Earlier B01–B13 runs were performed before English localization; the English excerpts are translations, not new executions. Record B14 and any localized-version checks separately.
