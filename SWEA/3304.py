``` 동적 계획법
- 애초에 문제 이해를 잘 해야 하는게, 연속적인게 아니라 순서 측면에서 두 문자열의 현재 위치까지의 원소들의 최장 부분의 길이를 찾아야 한다.
점화식: 
  - a[i] == b[j]일 때: dp[i][j] = dp[i-1][j-1] + 1
  - a[i] != b[j]일 때: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
if __name__ == "__main__":
  T = int(input())
  for test_case in range(T):
    answer = 0
    a, b = map(str, input().split(' '))
    dp = [[0 for _ in range(len(b))] for _ in range(len(a))]
    valid = False
    for i in range(len(b)):
      if a[0] == b[i]:
        valid = True
      if valid:
        dp[0][i] = 1
      
    for i in range(1, len(a)):
      for j in range(len(b)):
        if (a[i] == b[j]):
          if (j == 0):
            dp[i][j] = 1 # dp[i-1][j] + 1
          else:
            dp[i][j] = dp[i-1][j-1] + 1 # max(dp[i-1][j], dp[i][j-1] + 1)
        else:
          if (j == 0):
            dp[i][j] = dp[i-1][j]
          else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    answer = max(dp[-1])
    print(f"#{test_case+1} {answer}")
