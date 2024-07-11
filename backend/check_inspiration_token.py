# import requests,json
# url =  "https://kawo.sentry.io/issues/?environment=production&project=215896&query=expired&referrer=issue-list&statsPeriod=24h"
# # headers = {"Authorization": "Bearer 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"}
# res = requests.get(url=url)
# print(res.text)

# 小红定义一个字符串是可爱串，当且仅当该字符串包含子序列"red"，且不包含子串"red"。
# 我们定义子序列为字符串中可以不连续的一段，而子串则必须连续。例如rderd包含子序列"red"，且不包含子串"red"，因此该字符串为可爱串。
# 小红想知道，长度为n的、仅由'r'、'e'、'd'三种字母组成的字符串中，有多少是可爱串？

# 3*3*3 -1*1
# 4*4*4 - 3*2
# 5*5*5 - 8*3
# 6*6*6 - 15*4
def count_cute_strings(n):
    MOD = 10**9 + 7
    
    # dp[i][j] will store the number of strings of length i with j characters of "red" matched
    dp = [[0] * 4 for _ in range(n + 1)]
    
    # Initialization
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(4):
            # Current state
            current = dp[i - 1][j]
            
            # If adding 'r'
            if j == 0:
                dp[i][1] = (dp[i][1] + current) % MOD
            else:
                dp[i][j] = (dp[i][j] + current) % MOD
            
            # If adding 'e'
            if j == 1:
                dp[i][2] = (dp[i][2] + current) % MOD
            else:
                dp[i][j] = (dp[i][j] + current) % MOD
            
            # If adding 'd'
            if j == 2:
                dp[i][3] = (dp[i][3] + current) % MOD
            else:
                dp[i][j] = (dp[i][j] + current) % MOD
    
    # The number of strings of length n containing "red" as a subsequence
    total_with_subsequence_red = dp[n][3]
    
    # Now we need to subtract the number of strings containing "red" as a substring
    count_with_substring_red = 0
    
    # Iterate through possible positions where "red" can be a substring
    for i in range(n - 2):
        # Count valid prefixes and suffixes
        count_prefixes = 3 ** i
        count_suffixes = 3 ** (n - i - 3)
        
        count_with_substring_red = (count_with_substring_red + count_prefixes * count_suffixes) % MOD
    
    # The result is the number of strings with "red" as a subsequence minus the ones with "red" as a substring
    result = (total_with_subsequence_red - count_with_substring_red + MOD) % MOD
    
    return result

# Example usage
n = 4
print(count_cute_strings(n))
