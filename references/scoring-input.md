# Scoring script input and output

Use a host with local Python 3.10+; the script depends only on the standard library. Replace `<skill-dir>` with the actual skill directory. It can run from any working directory:

```powershell
python -X utf8 <skill-dir>/scripts/score.py <input.json>
```

Omit the filename or pass `-` to read standard input. Input files support UTF-8 with or without a BOM. The script emits JSON to standard output and does not save materials. Invalid input emits `{"error":"specific reason"}` to standard error, exits with code 2, and leaves standard output empty. Successful execution exits with code 0. Do not write sensitive materials into the repository by default merely to call the script; prefer supported standard input or a user-authorized location.

The complete synthetic example is [score-input.json](../tests/fixtures/score-input.json). Its demonstration ratings are predefined; they verify the interface and do not represent an actual model assessment of candidate ability.

## Top-level fields

| Field | Meaning |
| --- | --- |
| interview_type | technical, comprehensive, or hr |
| critical_dimensions | Array of dimension IDs associated with this round's critical role abilities; required explicitly. An empty array reserves the hiring judgment |
| weights | Optional object containing every dimension ID for the type. If omitted, use rubrics.json defaults. If present, include all dimensions, numeric finite values from 0–100 totaling 100; booleans and numeric strings are invalid |
| answers | Array of answer records; may be empty. Never fabricate historical question-and-answer records to satisfy the format |
| ratings | Object containing every dimension's rating and evidence for the type. Explicitly use N/A when evidence is absent; missing dimensions are not silently filled |

Read stable dimension IDs, names, observation focus, default weights, and coefficients only from [rubrics.json](../assets/rubrics.json). Freeze weights before asking questions; the script cannot establish that the caller did not change them later. The host must enforce interview rules.

## Each record in answers

| Field | Constraint |
| --- | --- |
| id | Unique, nonempty answer ID |
| question_id | Actual main-question or follow-up ID; nonempty |
| status | answered, explicitly_unknown, skipped, or incorrect, as assessed by the model |
| text | Actual answer or summary; nonempty. A skipped record may contain the user's actual skip statement |
| record_kind | raw for available original wording, or summary. A report-only source cannot be claimed as raw |
| feedback_intervened | Strict boolean. Set true for answer hints, teaching, or improvement guidance; such answers cannot support independent-performance scoring |

Not assessed and insufficient evidence are dimension evidence states; do not fabricate answers for them. Ending early is a session event to list separately. Pass actual answers and leave remaining dimensions N/A. Post-guidance improvements may remain in the answers array but cannot be cited as sufficient rating evidence.

## Each dimension in ratings

```json
{
  "level": "Meets",
  "evidence_status": "sufficient",
  "evidence": [
    {"answer_id": "A1", "reason": "Explain why this actual answer supports this dimension's predefined focus and rating."}
  ]
}
```

- `level` must be one of the four levels in rubrics.json or the string `N/A`.
- `evidence_status` is sufficient, not_assessed, or insufficient. sufficient requires nonempty evidence and a four-level rating. The other statuses require N/A. not_assessed cannot cite answers; insufficient may retain references to available but inadequate evidence.
- Each reference requires an existing `answer_id` and a nonempty `reason`. Do not repeat the same reference within a dimension. One answer may support multiple dimensions with separate reasons.
- Skipped and post-guidance answers cannot support sufficient. Explicitly unknown or incorrect answers may provide evidence, but the program does not automatically rate them Weak or generalize them to an entire dimension.

Reject unknown fields, duplicate JSON keys, invalid levels, NaN/Infinity, missing dimensions, and inconsistent evidence states rather than silently correcting errors. The model remains responsible for semantic truth, evidence sufficiency, and rating appropriateness.

## Output

`score` is the score renormalized over assessed original weights, with two decimal places, or JSON `null` when there is no scorable weight. `coverage_percent` is the sum of original weights for sufficiently assessed dimensions. `dimensions` lists names, original weights, levels, evidence states, and references in the original table order.

`critical_dimensions` preserves input. `unassessed_critical_dimensions` lists critical dimensions without sufficient rating evidence. `judgment_status` is either:

- `reserved`: evidence for critical abilities is missing, no critical abilities are defined, or there is no scorable weight, as explained in `notes`.
- `requires_model_judgment`: there is scorable evidence and all named critical dimensions have ratings. The model must still check each role requirement; this is not an automatic hiring recommendation.

There is no fixed major-error cap or total-score recommendation threshold. High scores, complete coverage, or any output status do not replace an evidence-based role judgment.
