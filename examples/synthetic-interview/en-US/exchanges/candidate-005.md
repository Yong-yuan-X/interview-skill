The first attempt has a six-second timeout. When it times out, the wrapper classifies that as retryable. Since one attempt remains, it waits 250 milliseconds and makes the second call, again with a six-second timeout.

The second call returns HTTP 503. That is also a retryable category, but we have now used the maximum of two attempts, so the wrapper stops. It does not make a third call or restart the attempt counter.

The endpoint returns HTTP 503 with our API error code `MODEL_UNAVAILABLE`. It does not return a successful empty answer or set `insufficient_evidence` to represent this failure, because the problem is that generation was unavailable, not that we established the documents lacked evidence.

The request logs let me correlate the timeout and provider 503 with the request ID, attempt count, error categories, and generation duration, without recording the confidential prompt. I wouldn’t say this request necessarily takes the full two timeout periods: the second call might return its 503 quickly.

For a unit test, I would configure the fake provider to time out once and then return 503, and assert exactly two calls and the final API status and error code.
