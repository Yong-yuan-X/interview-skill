I would first try increasing the chunk overlap from 80 characters to something like 160, while keeping the 600-character chunk size and top four unchanged for the comparison. My reason is that this example points to evidence being split at a boundary. More overlap might keep the rule and its nearby exception together in a retrieved passage.

I would inspect the actual text first to see how far apart they are. Increasing overlap wouldn’t guarantee that both fit, especially if the exception is long or farther into the next chunk.

I haven’t run this experiment, and the current settings came from a senior engineer. I would compare the existing setting with the proposed overlap using the same evaluation questions, check whether the retrieved passages include both the rule and exception, and then inspect the answers. I would also look for repeated passages taking up the four retrieval slots. I would treat 160 as a trial setting, not an established improvement.
