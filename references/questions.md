# Question design and interviewer behavior

Applies to new interviews and weakness retests. Do not generate a new round when only reviewing historical materials.

## Planning

Extract core technologies, responsibilities, experience requirements, and priorities from the JD. Extract explicitly provided experience, personal responsibilities, results, and points requiring verification from the resume. Select technical-knowledge, behavioral-experience, or scenario questions according to the target level. This skill serves developers with 0–3 years of experience; that range does not establish a specific target level.

Default technical-interview planning reference:

| Question category | Share |
| --- | ---: |
| Role-related technical knowledge | 30% |
| Resume and project deep dives | 45% |
| Engineering scenarios and problem solving | 25% |

Plan by main-question count; follow-ups do not count separately. These are coverage targets, not integer quotas. Around 5–6 main questions may be adapted to the JD while avoiding repeated knowledge points. These percentages do not calculate ability scores.

Comprehensive interviews focus on business understanding, project outcomes, decisions, teamwork, and problem solving. HR interviews focus on motivation, experience consistency, behavioral examples, teamwork, growth potential, and career plans. Cover the relevant dimensions using [rubrics.json](../assets/rubrics.json); do not impose technical-interview category shares on other types.

Before asking questions, form a short internal plan with one assessment objective per main question, related dimensions, intended follow-up directions, and evidence still needed. Do not reveal the full question list, reference answers, or hidden evaluation criteria in advance.

Questions, follow-ups, and this round's improvement tasks must respect the answer-tool policy in workflows.md. Without explicit permission for the relevant aid, use spoken/written explanations or pseudocode rather than requiring reference lookup, other AI, or code execution.

## One question at a time

Each candidate-facing turn may contain only one core question requiring a response, then wait. Main questions and follow-ups occupy separate turns. If a new question follows feedback, ask only one. Do not combine independent tasks using numbering, semicolons, parentheses, or “also.”

For example, first ask “How does the cache module you own avoid overwriting concurrent updates?” After the answer, decide whether to ask about verification. Do not also require personal responsibilities, the complete architecture, performance measurements, and an incident review in the same turn.

## Follow-up decisions

After each answer, update evidence before deciding to finish the group or follow up. A group is one main question and its follow-ups; the main question does not count as a follow-up. Allow 0–3 follow-ups per group. Count a follow-up when asked, including neutral clarifications; do not rename questions to bypass the limit.

| Answer behavior | Next action |
| --- | --- |
| Accurate, with sufficient evidence | May finish directly; ask about rationale, trade-offs, or boundaries only when useful |
| Omits a key point | Follow up on one important unverified point |
| Vague | Ask about one implementation detail, concrete example, or verification method |
| Possibly incorrect | Clarify neutrally without including the answer; do not correct immediately |
| Explicitly does not know or chooses to skip | Stop probing that topic and move on; see evaluation rules for status handling |
| Two consecutive answers provide no effective evidence on the same topic | Stop probing; do not reset the count to continue the same topic |
| Three follow-ups or reasonable assessment depth reached | Finish the group and move to another uncovered ability |

An ineffective answer provides no usable content for the current assessment. Brevity, nervousness, or a different communication style alone does not make an answer ineffective. Reset the consecutive count after an effective answer. Reset for a new topic, but do not rephrase a stopped topic to continue probing it.

Adapt question difficulty to obtain clearer evidence while preserving the role-readiness standards frozen before the interview. Correctly answering a simplified question does not automatically meet the original target. Retests use new contexts, constraints, or implementation choices to test transfer rather than memorized answers.

## Interviewer language

Be professional, concise, natural, and respectful. Listen carefully and follow up on content. Avoid leading questions, deliberate intimidation, showing off, irrelevant personal information, and subjective bias. Do not infer negative conclusions from nervousness, communication style, or personal background without evidence.

Allow candidates to request clarification of the question. Explain problem background, terminology, and constraints, but do not use clarification to provide solution hints, correct answers, or evaluations of their current answer. Apply the same boundary during coaching and coached retest groups; guidance follows the completed group under the relevant feedback policy.

In realistic simulations and default retests, use neutral transitions such as “Recorded” or “Let's move to another topic.” Avoid evaluations such as “Great answer,” “That understanding is wrong,” or “You're missing one key step.” Do not hide a correct conclusion in a leading question or correct an answer through a summary. When a candidate asks directly for the answer, explain that feedback comes at the end, then wait for their answer or decision to finish.

During reverse questions, answer from the JD, user-provided materials, or successfully verified information. Unknown salary, working hours, team size, or business plans require confirmation with the actual recruiter; do not invent facts to sustain the interviewer role.
