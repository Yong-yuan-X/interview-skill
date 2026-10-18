# Design verification and decisions

The original local design source is `interview-skill.docx`, which is not included in the public release. Its baseline SHA-256 was `DF914549B17E89BA51E8B4BEB4E7E674260BD8A23FF0302BB2A46071CCB65E46`. The original implementation record states that all eleven chapters, ten PNG tables, and ten embedded Excel source tables were read. Running the skill does not require reparsing Word.

## Confirmed decisions (2026-10-15)

The user explicitly accepted the following three recommendations during the original implementation. They resolve design ambiguities and must not be presented as requirements already specified in the source. Runtime behavior follows workflows.md and evaluation.md; do not request these decisions again.

| Issue | Original design | Confirmed decision | Implementation |
| --- | --- | --- | --- |
| Defaults | Chapter 3 lists modes; Chapter 2 makes type optional without defaults; Chapter 1 specifies only the 0–3-year audience | Ordinary new interviews default to realistic technical simulations. Use an explicit target level or a clear JD requirement; otherwise ask once | workflows.md: Settings and inputs |
| Historical review and retest separation | Chapter 2 uniformly requires a JD and resume; Chapter 3 reviews existing records; Section 11.2's image still describes review as focused questioning, and Section 10.3 broadly mentions weak-area questions during review | Historical review does not require a new JD/resume and marks missing context. Retests obtain these or confirm recovered context. Follow-ups and new questions belong to retesting | workflows.md: Historical review and Weakness retest |
| Major-error caps | Section 8.2 covers triggers, clarification, self-correction, and primary dimension impact, with no numerical cap | No fixed first-version cap. Rate against frozen anchors and record impact; other dimensions need independent evidence | evaluation.md: Major errors |

## Explicit source requirements and implementation choices

- Coaching feedback follows the main question and all follow-ups. Keep first independent and post-guidance performance separate. Rules repeated across Chapters 3, 5, 8, and 11 are consolidated in workflows.md; other files retain entry constraints.
- Technical-question proportions in Chapter 6 and Section 10.1 are planning references, not rigid integer quotas. Comprehensive and HR interviews use their own observation focus.
- Observation focus, weights, and coefficients come from the original images/tables and are centralized in rubrics.json. The technical table image clipped the project-ownership focus. Cell C3 in embedded `Microsoft_Excel_Worksheet2.xlsx` provides the complete meaning: personal contributions, implementation details, technical challenges, project results, and answer consistency. The clipped text was not guessed.
- Section 8.4 requires behavioral standards adapted to the JD and target level without providing complete role-specific anchors. Observable examples in evaluation.md are implementation additions, not thresholds already established by the original source.
- Chapter 9's three highest-priority issues is implemented as at most three, per the user's request: report only supported issues rather than filling a quota.
- The standard-library Python implementation, strict JSON structure, percentage weights, zero weights, two-decimal score display, and stable evidence IDs are implementation choices. The model judges semantics; the program calculates and validates structure. No hiring-score threshold was added.
- User-requested separation of embedded material instructions, read-only code inspection, authorized historical access, and sensitive-output boundaries are implemented in SKILL.md, workflows.md, and the report template.

## Language and publication update (2026-10-15)

The maintainer requested English Markdown for the public release and local Chinese development sources. The sources mirror release paths under `local/zh-CN/`; Git ignores them and the original Word document. Edit Chinese first and faithfully translate to the release paths. JSON labels and synthetic materials are also translated while preserving keys, IDs, enums, numerical values, and calculator behavior.

README.md, LICENSE, and the original Word document are protected files. Preserve their existing content and layout unless the maintainer explicitly requests a change to that file. README.md is a bilingual exception to the English release convention; do not translate or expand it alongside skill documents. Keep its local copy identical to the original.

The conversation-language rule follows explicit user preference, then the current conversation language. It covers questions, follow-ups, coaching, and reports. The language of supplied materials does not override it, technical terms may retain their original form, and users may switch languages at any time. Localize display headings and labels while preserving machine identifiers and original quoted answers.

Historical validation excerpts in the English release are labeled as translations. Earlier runs do not establish behavior of the localized release; record any new checks separately.

## Design alignment confirmed (2026-10-18)

- Candidate answers default to no reference lookup, other AI, or code execution. Allow only the scope proactively and explicitly permitted by the user, without asking for exceptions at the start. workflows.md defines policy and actual-use records, which appear in the report. The candidate rule does not restrict interviewer material reading or the scoring script.
- Follow the design's allowance for clarification of problem background, terminology, and constraints without solution hints or evaluations of the current answer. Coaching guidance follows the completed group.
- Retain the existing recording rule of verbatim answers or explicitly labeled accurate summaries. The maintainer requested a parenthetical implementation note at the corresponding location in the local Chapter 9 design document.
- Separate priority improvements from reference answers for key questions. Improvements remain limited to at most three; reference answers are not limited by that count or to weak answers.

## Chapter mapping

| Original chapter | Implementation |
| --- | --- |
| 1: Positioning; 2: User input | SKILL.md; workflows.md: Settings and inputs; confirmed defaults and material decisions in this file |
| 3: Interview modes | Four separate workflows in workflows.md |
| 4: Simulation flow; 5: Core rules | SKILL.md, workflows.md, questions.md |
| 6: Question composition | Planning table in questions.md, separate from scoring configuration |
| 7: Three evaluation systems | Complete type-specific dimensions and observation focus in assets/rubrics.json |
| 8: Unified evaluation rules | evaluation.md, scoring-input.md, scripts/score.py, tests/test_score.py |
| 9: Output | assets/report-template.md |
| 10: Adaptive questions | questions.md; workflows.md: Weakness retest |
| 11: Interviewer behavior | Expression and follow-ups in questions.md, feedback timing in workflows.md, evidence separation in the report template; historical-review table conflict noted above |

## Capability and validation boundaries

This repository supplies readable skill instructions, runtime resources, and a deterministic local calculator. It does not supply an interview application, storage service, automatic timer, cross-session memory, or model API. The host must support text loading and ongoing conversation. Project inspection, Python execution, report saving, and accurate timing depend on actual host tools and user authorization.

Automated tests check program and input boundaries; skill format validation checks entry structure. Behavioral scenarios are in tests/behavior-cases.md. Do not claim unexecuted cases passed. The original implementation did not call paid model APIs or install the skill globally.
