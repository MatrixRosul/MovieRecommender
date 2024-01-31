class Searcher:
    def levenshtein_distance(self, s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],  # Deletion
                                       dp[i][j - 1],  # Insertion
                                       dp[i - 1][j - 1])  # Substitution

        return dp[m][n]

    def search_words(self, movie_title, movie_list, max_operations=10):
        matches = []
        for target in movie_list:
            distance = self.levenshtein_distance(movie_title, target)
            if distance <= max_operations:
                matches.append((distance, target))

        matches = sorted(matches, key=lambda x: x[0])

        return matches[:6]
