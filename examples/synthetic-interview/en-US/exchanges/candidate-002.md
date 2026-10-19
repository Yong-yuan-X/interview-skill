The Pydantic check establishes that the response has the expected fields and field types. The citation check establishes that every returned citation ID refers to a passage we actually retrieved for this request, within the trusted organization scope.

My understanding has been that those checks are enough to call the answer grounded: it has the expected structure and points back to the supplied evidence. That is what I meant in my earlier answer.

The implementation doesn’t separately compare each statement in the answer with the text of its cited passage. For example, the citation membership check operates on IDs; it doesn’t read the passage to check the wording of the answer.
