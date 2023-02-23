if __name__ == "__main__":
  T = int(input())
  for test_case in range(T):
    N, K = map(int, input().split(' '))
    dp = [[0 for _ in range(K+1)] for _ in range(N+1)]
    weights = []
    costs = []
    for n in range(N):
      v, c = map(int, input().split(' ')) # 부피, 가치
      # dp[n][v] = c
      weights.append(v)
      costs.append(c)
    
    for i in range(1, N+1):
      for j in range(1, K+1):
        cur_weight = weights[i-1]
        cur_cost = costs[i-1]
        if j > cur_weight:
          dp[i][j] = max(dp[i-1][j-cur_weight] + cur_cost, dp[i-1][j])
        elif j == cur_weight:
          dp[i][j] = max(dp[i-1][j], cur_cost)
        else:
          dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    answer = max(dp[-1])
    print(f"#{test_case+1} {answer}")
    

