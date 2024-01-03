import sys

input = sys.stdin.readline

N = int(input().strip()) # 작업장의 수 #

"""가장 빠른 조립 시간 출력
풀이 방식은 dp를 사용하는 것으로 맞게 했는데, 보니까 
N = 1인 경우에는 ab, ba가 없는데 prev_ab, prev_ba에 할당하려고 하고 있었다.
"""
dp = [[0, 0] for _ in range(N+1)]
prev_ab, prev_ba = 0, 0

for n in range(1, N+1, 1):
    # A, B 작업장에서의 작업 시간, A->B 이동시간, B->A 이동시간 #
    if n < N:
        a, b, ab, ba = map(int, input().strip().split(' '))
    else:
        a, b = map(int, input().strip().split(' '))  
        
    dp[n][0] = min(dp[n-1][0], dp[n-1][1] + prev_ba) + a
    dp[n][1] = min(dp[n-1][0] + prev_ab, dp[n-1][1]) + b
    if N != 1:
        prev_ab, prev_ba = ab, ba # a->b, b->a #
    # prev_ab, prev_ba = ab, ba
# print(dp)
print(min(dp[-1]))
    
 

    