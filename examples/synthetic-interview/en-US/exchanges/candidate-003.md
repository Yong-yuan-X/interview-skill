The current protection is in how I assemble the prompt: the system instruction says to answer from the supplied evidence and report insufficient evidence when needed. Retrieved passages are placed in a separate delimited section and explicitly described as untrusted data. So that sentence should be treated as document content, not as an instruction the assistant should follow.

I can’t claim that this guarantees the model will ignore it. We haven’t completed a comprehensive prompt-injection evaluation. The schema and citation-ID checks also wouldn’t detect the model following that instruction if it still returned valid JSON and cited an ID from the retrieved set.

Thinking through this example, my earlier statement about grounding was too strong. A response could pass both checks and still give an unsupported answer. The checks establish the response structure and where the citation IDs came from; they don’t establish that the cited text supports the answer.

Organization filtering still happens in the retrieval query, outside the model, and this assistant has no action tools or write capability. Those constraints limit access and actions, but they don’t solve misleading answers. I would propose adding this example to our evaluation and manually checking the answer against the passages; that is a next step, not a defense we have already verified.
