With the wrapper as implemented, a 429 on the first attempt causes a retry after our fixed 250-millisecond delay. We don’t currently read `Retry-After`, so it would retry before the ten seconds requested by the provider. If the second attempt also fails with a retryable error, we stop and return 503 with `MODEL_UNAVAILABLE`.

That is a limitation in my implementation. I wouldn’t describe it as correctly handling this header.

I would propose changing the wrapper to account for the provider’s requested delay while keeping a bounded overall wait. For this example, if waiting ten seconds would exceed the request budget we agree on, I would stop and return the unavailable error instead of retrying after 250 milliseconds. If the budget permits it, we could wait ten seconds and use the remaining attempt.

I haven’t implemented that policy or established an overall request budget. I would review those choices with a senior engineer and add fake-provider tests for the delay decision, the attempt limit, and the final API response.
