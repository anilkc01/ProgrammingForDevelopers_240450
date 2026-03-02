def segment_marketing_query(user_query, marketing_dict):
    word_set = set(marketing_dict)
    memo = {}

    def solve(start):
        if start in memo:
            return memo[start]
        
        # If we reach the end, return a list with an empty string to start building
        if start == len(user_query):
            return [""]
        
        results = []
        for end in range(start + 1, len(user_query) + 1):
            word = user_query[start:end]
            if word in word_set:
                # Get all possible ways to finish the sentence from this point
                suffixes = solve(end)
                for suffix in suffixes:
                    # Join the word with the rest of the sentence
                    full_sentence = (word + " " + suffix).strip()
                    results.append(full_sentence)
        
        memo[start] = results
        return results

    return solve(0)

# Example Usage
query = "nepaltrekkingguide"
keywords = ["nepal", "trekking", "guide", "nepaltrekking"]
print(segment_marketing_query(query, keywords))


