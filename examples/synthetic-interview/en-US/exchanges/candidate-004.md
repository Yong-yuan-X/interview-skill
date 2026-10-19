I would use two organizations in a test database and exercise the actual retrieval query. Organization A would have one relevant passage. Organization B would have four passages that rank more highly for the same question. That arrangement matters because our retrieval limit is four.

I would make the request with trusted middleware context for organization A. I would assert that retrieval returns A’s passage and none of B’s chunk IDs. I would also capture the passages passed to the fake generation client and assert that none belong to B.

If we selected the global top four first, we would select only B’s passages. Filtering afterward would leave no passages, so the assertion that A’s passage is returned would fail. This tests both isolation and the placement of the organization filter before top-k selection.

This is a test I would add. Our existing tests use fake retrievers to check that the endpoint passes the trusted organization context; those alone don’t verify the SQL query against a real database.
