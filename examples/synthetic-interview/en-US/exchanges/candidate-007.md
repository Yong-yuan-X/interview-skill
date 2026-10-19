I would inspect the retrieved passages before judging the generated answer. My existing records include the expected source document IDs, retrieved IDs, output, and manual notes. There are 16 answerable questions and four intentionally unanswerable ones, but I haven’t consistently labeled whether each answer’s claims are supported.

For an answerable question, I would first check whether the returned passages actually contain the evidence needed to answer it. Matching the expected document ID is useful, but the retrieved chunk could still omit the relevant section. If the needed evidence is missing from the passages, I would record a retrieval failure. I would then investigate whether the relevant text was indexed and whether the chunk boundaries or ranking kept it out of the top four, without assuming which caused it.

If the necessary evidence is present in the passages supplied to generation, but the answer contradicts it, adds unsupported details, or incorrectly says there is insufficient evidence, I would record a generation failure. I would compare individual claims with the passage text; valid JSON and an allowed citation ID wouldn’t settle that check.

For the four unanswerable questions, I would expect an insufficient-evidence response. Nonempty retrieval can still contain irrelevant passages. A confident answer unsupported by those passages would be a generation problem, even though retrieval returned results.

I would add separate manual notes for evidence availability and answer support, allowing both problems to be recorded where appropriate. This would improve the diagnosis, but 20 questions are a small set, and I don’t have an accuracy-improvement result to claim from it.
