# Levenshtein Distance Function

def distance(s: str, t: str) -> int:
    # get the length of each string...
    n, m = len(s), len(t)

    # and create a matrix to hold the minimum distances
    # between each prefix of the two strings
    d = [[0] * (m + 1) for _ in range(n + 1)]

    # Base cases
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Calculate minimum distance between 
            # string prefixes by comparing character positions.
            
            # If the characters at position i and j match, 
            # we can assume that no edit operation is required for these characters. 
            # Therefore, we take the value from the previous diagonal entry, 
            # which represents the minimum distance between the prefixes without considering the current characters.
            if s[i - 1] == t[j - 1]:
                cost = 0
            else:
                # If the characters don't match, we have three possible edit operations: 
                # - substitution (replace s[i] with t[j])
                # - deletion (delete s[i])
                # - insertion (insert t[j] after s[i])
                # We choose the operation that results in the minimum distance.
                cost = 1

            d[i][j] = min(
                d[i - 1][j] + 1,       # deletion
                d[i][j - 1] + 1,       # insertion
                d[i - 1][j - 1] + cost  # substitution
            )

    # The final Levenshtein distance is the value in the bottom right corner of the matrix.
    return d[n][m]
