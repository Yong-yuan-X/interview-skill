I would supply a valid question and trusted middleware context for organization A. The fake retriever would return two known passages from A, and the fake provider would return valid JSON with a known answer, one of those chunk IDs, and `insufficient_evidence` set to false.

I would assert that:

- The endpoint returns HTTP 200, and the response contains the expected answer, citation IDs, and false insufficient-evidence flag.
- Retrieval is called once with the question and the trusted organization ID from middleware.
- The provider is called once, so a successful response doesn’t trigger a retry.
- The prompt passed to the provider contains the question and the returned passages, including their chunk IDs. I would also check that the passages are in the delimited data section and that the instruction identifies them as untrusted content. I would avoid asserting every character of the prompt.
- The returned citation ID is preserved correctly after parsing and belongs to the retrieved set.

That test verifies the successful endpoint flow and the data passed between its stages. It doesn’t verify the database’s actual organization filtering because the retriever is fake. It also doesn’t establish that a real model will answer correctly or resist instructions in document text; the provider’s output is predetermined in this test.
