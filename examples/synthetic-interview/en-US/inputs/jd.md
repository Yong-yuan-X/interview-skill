# AI Synthetic Test: Job Description

All names, employers, and requirements in this scenario are fictional.

## Role

Junior AI Application Developer at Harborlight Tools, an internal knowledge-software company. Target experience: **1 year of professional development**. Assess ownership of a small AI application feature with normal senior code review.

## Product and stack

A read-only internal document assistant helps employees find answers in documents their organization can access. Stack: Python, FastAPI, Pydantic, PostgreSQL with pgvector, an external text-generation service, pytest, and Docker. Authentication, the ingestion worker framework, and deployment are maintained by other engineers.

## Responsibilities and expectations

- Explain a basic retrieval-augmented generation request from validated input through retrieval, prompt construction, generation, response validation, and citations.
- Apply trusted organization identity to document retrieval and avoid treating client-supplied identities or retrieved document text as trusted instructions.
- Explain personally implemented features and distinguish working code, assumptions, proposed improvements, and colleagues' work.
- Handle provider timeouts and temporary errors with bounded attempts, clear API failure semantics, and useful request logs that avoid secrets and full confidential prompts.
- Write tests for successful and unsuccessful requests. Use a small evaluation set to separate retrieval failures from answer-generation failures; recognize the limits of schema validation and citation checks.
- Discuss elementary chunking/top-k choices using concrete examples and propose a modest verification method. Advanced model training, vector-index internals, and production-scale ML infrastructure are outside the required scope.
- Ask for help when evidence is insufficient; discuss trade-offs at the feature level rather than claiming system-wide ownership.

Changes require code review and automated tests before merge. Salary, on-call schedules, incident staffing, overtime, team size, and detailed mentoring arrangements are not provided.
