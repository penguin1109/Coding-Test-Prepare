N = int(input())
MAX = 1000
dp = [0 for _ in range(MAX + 1)]

## 한번에 가져가면 되니까 무조건 1, 3, 4개의 돌이 있는 경우 SK가 이긴다. (모두 최적의 플레이를 한다는 가정하에)
dp[1] = 1
dp[3] = 1
dp[4] = 1 ## 1개와 3개를 합치면 4개가 된다는 것으로 볼때..

for n in range(5, N+1):
    # (1, 1, 1)이 아닌 경우를 의미 한다. 즉, 1, 3, 4중에 몇개의 돌을 가져가던 CY가 한번이라도 돌을 가져간 적이 있는 경우라면
    # 상대방이 돌을 가져간 시점으로부터 1, 3, 4개중에 1개를 가져가면 내가 (SK) 이기는 것이 된다.
    # 역시나 <돌게임1>처럼 숫자의 가져감의 순서는 전혀 중요하지가 않고, 그래서 결국에 마지막에는 누가 가져가게 되는지가 중요하다.
    if dp[n-1] == 0 or dp[n-3] == 0 or dp[n-4] == 0:
        dp[n] = 1
    # if (dp[n-1] + dp[n-3] + dp[n-4] < 3):
    #     dp[n] = 1
    else:
        dp[n] = 0

if dp[N] % 2 == 0: ## CY
    print("CY")
else:
    print("SK")



