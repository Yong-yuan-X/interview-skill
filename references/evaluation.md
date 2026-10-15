# Evidence and evaluation

Before a new interview or retest, read this file and the relevant type's goal, six dimensions, weights, observation focus, and four-level standards in [rubrics.json](../assets/rubrics.json). The JSON file is the sole runtime source for those numerical values and table entries. Establish standards before collecting evidence; question-category planning shares are not dimension weights.

## Freeze standards before interviewing

Extract critical role abilities from the JD, map them to dimensions, and establish observable performance at each level. Weights may be adapted to the JD before the interview. Include all dimensions for that interview type, with numeric percentages from 0–100 totaling 100. A zero weight may explicitly exclude a dimension from the total; keep its record, and do not let it increase weighted coverage. During the interview, adapt questions and follow-ups, never weights, critical abilities, or readiness anchors in response to performance.

For each dimension, form a short internal basis: “JD requirement -> target level -> observable behavior -> question direction for evidence.” Tell the user the type, mode, target level, and assessment focus without revealing answers. If there is insufficient information to establish readiness standards, clarify first; do not infer standards retrospectively from answers.

The documents provide general four-level standards rather than complete behavioral anchors for every role. The following are **implementation examples** to adapt to this JD, target level, and observation focus. They are not universal role thresholds.

| Level | Example observable behavior |
| --- | --- |
| Strong | Independently explains key rationale, weighs solutions under changing constraints, and provides verification evidence; exceeds role expectations |
| Meets | Independently explains understanding and application within the role's scope, with concrete examples and necessary validation; meets the predefined requirements |
| Below | Explains some content, but has clear role-related gaps in application, trade-offs, or verification |
| Weak | Sufficient evidence shows inability to meet core role requirements; this is not merely a lack of observable information |

For technical interviews, anchor principles, genuine contributions, selection rationale, engineering quality, troubleshooting, and technical communication. For comprehensive interviews, anchor business goals, constrained decisions, responsibility and outcomes, collaboration, learning, and thinking. For HR interviews, anchor motivation, experience consistency, conflict handling, growth, planning, and professional communication. Asking about a dimension once does not establish sufficient evidence for every critical ability.

## Separate answer status from dimension evidence

| Event or status | Handling |
| --- | --- |
| Not assessed | Dimension N/A, evidence status not_assessed; do not score |
| Insufficient evidence | Dimension N/A, evidence status insufficient; do not infer ability level |
| Explicitly does not know | Keep evidence of that specific gap; do not automatically rate the entire dimension Weak |
| Chooses to skip | Record non-answer; skipping alone does not establish inability or support a dimension rating |
| Incorrect answer | Evaluate the specific error, neutral clarification, and later responses; do not let one incorrect statement define the entire dimension |
| Ends early | Record the session end reason; assess completed portions normally and leave unassessed dimensions N/A |

Use sufficient and one of the four ratings only with adequate evidence. The model judges sufficiency and level; the script validates structure and references. Never rate by answer length, keywords, or terminology density.

Every reason must identify the main question or follow-up and the corresponding answer, explaining why it supports the dimension. One answer may support several dimensions, with a separate reason for each. Distinguish technical errors from unclear expression and avoid mechanically penalizing the same issue repeatedly. Evaluate reasonable alternatives by constraints, correctness, trade-offs, and validation, not agreement with a reference answer.

When a candidate self-corrects without hints, assess the complete process. Do not treat improvements after teaching as first-attempt independent ability. Keep post-guidance answers separate in coaching and coached retests, preserving the intervention content, timing, and independent performance.

## Major errors

Mark a major error only when it directly concerns a critical role ability and its actual effect on correctness, reliability, or safety can be explained. First use necessary neutral clarification to rule out slips, misunderstood questions, or terminology differences. Clarification still counts toward follow-up limits. Record the original answer, clarification, impact, and related dimensions.

Inability to explain a core module the candidate claims to own primarily affects project ownership and personal contribution. Other dimensions need their own evidence. Do not infer fabricated experience from fluency; clarify contradictions or mark them for verification.

The original design specifies no numerical cap. The confirmed first-version decision is no fixed rating or score cap: rate against evidence and frozen anchors, and separately explain major-error impact. Do not automatically cap scores. See [design-notes.md](design-notes.md) for the decision source.

## Total score and coverage

Overall score = sum(original weight × level coefficient for sufficiently assessed dimensions) / sum(original weights for those dimensions) × 100. Read coefficients from JSON. Exclude N/A from numerator and denominator.

Coverage is the sum of original weights for dimensions with sufficient rating evidence, displayed as a percentage. With no scorable weight, the overall score is null and the reason is insufficient evidence; do not substitute zero. Display scores with two decimal places using decimal half-up rounding. This is a presentation choice, not a new passing threshold.

When critical role abilities lack evidence, provide interim feedback and reserve the simulated hiring judgment. The script's requires_model_judgment status only means the named critical dimensions have rating evidence. The model must still check each critical ability against requirements; this status does not automatically recommend a candidate. Even rated critical dimensions may contain unverified subabilities, so judgment may still need to be reserved. List salary, availability, location, and working-arrangement conditions separately from ability scores.

When historical materials contain only an old report, distinguish quoting old scores from reassessing original question-and-answer records. Do not invent original evidence or claim to have recalculated and verified old scores when verification is impossible. Differences in JD, target level, weights, coverage, or intervention prevent treating total-score changes alone as ability changes.

## Run the scoring script

See [scoring-input.md](scoring-input.md) for the input structure, fields, and commands. Prefer the supplied local script when Python is available. Without execution tools, use the same formula and explicitly state that the script was not run. Do not invent execution results. Do not upload interview materials or call model APIs merely to calculate a score.
