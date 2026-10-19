I haven’t used reference lookup, other AI, or code execution to prepare this answer.

For `POST /questions`, I first validate the request with Pydantic. The question must be nonempty and at most 1,000 characters; an invalid request receives 422. Authentication middleware supplies the trusted organization and user identity. I integrated that context into the endpoint, but I didn’t implement authentication, and I don’t use an organization ID from the request body to decide access.

Next, the endpoint calls retrieval using that trusted organization ID. The database query restricts documents to that organization before selecting the four most similar passages. Each passage includes its chunk ID, document ID, title, and text. If retrieval returns nothing, I return an insufficient-evidence response without calling the generation service.

Otherwise, I assemble a prompt with instructions to answer from those passages, cite chunk IDs, and report insufficient evidence when needed. The passages go into a separate delimited section identified as untrusted content. I then call our external generation service through the wrapper I implemented. It allows at most two attempts, with a six-second timeout per attempt, and retries only the temporary error categories we selected.

The expected output is JSON containing `answer`, `citation_ids`, and `insufficient_evidence`. I parse it with Pydantic and check that every citation ID belongs to the passages retrieved for this request. With valid structured output and those citation checks passing, I treat the answer as grounded and return it. Malformed output returns 502 with `MODEL_RESPONSE_INVALID`; exhausted provider attempts return 503 with `MODEL_UNAVAILABLE`.

I log the request ID, organization ID, stage durations, attempt count, error category, and retrieved chunk IDs so I can investigate a request without logging confidential passage text or the complete prompt. My ownership was the endpoint and provider wrapper; the ingestion framework, embedding service, index configuration, and deployment were handled by other engineers.
