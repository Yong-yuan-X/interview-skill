# AI Synthetic Test: Session Setup

Both agents were actually created with `collaboration.spawn_agent`, using `fork_turns="none"` and no model or reasoning-effort override. Returned handles identify tasks, not host session IDs.

## Candidate

Task name: `english_candidate`. Returned handle: `/root/english_candidate`.

Actual startup message:

> Read and execute E:\.github\interview-skill\examples\synthetic-interview\en-US\inputs\candidate-agent-task.md. You are the independent candidate in this AI synthetic test. Use only the task's specified synthetic materials and capability profile. For this initialization turn, prepare and return READY; wait for actual interviewer messages before answering.

## Interviewer

Task name: `english_interviewer`. Returned handle: `/root/english_interviewer`.

Actual startup message:

> Read and execute E:\.github\interview-skill\examples\synthetic-interview\en-US\inputs\interviewer-agent-task.md. You are the independent interviewer in this AI synthetic test. Load the task's installed interview-skill and normal materials, then begin the complete realistic technical interview in English. Save and return only one actual interviewer turn at a time, waiting for the mediator to forward the candidate's real answer.

The candidate's initialization status is outside the interview transcript. All later recorded dialogue must come from actual outputs. The installed snapshot was copied locally from the Chinese run's previously installed pinned copy and independently compared byte-for-byte to all 18 commit files; no network installer or global installation occurred in this run.
