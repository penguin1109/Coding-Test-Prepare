""" BOJ 14719 - 빗물
[출력] 블록 사이에 고이는 빗물의 총량
[풀이 방법] 값이 감소하다가 증가하는 구간 찾기

-> 첫번째 풀이는 양 옆을 세계의 높이 H와 같은 크기의 블록이 막고 있는 상황을 고려하지 못했었다.
-> 두번째 풀이는 각각의 블록을 기준으로 이후, 이전에 제일 큰 값을 저장하는 것이다.
"""
import sys
input = sys.stdin.readline

H, W = map(int, input().strip().split(' '))

heights = list(map(int, input().strip().split(' '))) 
left_max_dp = [0 for _ in range(W)]
right_max_dp = [0 for _ in range(W)]

for i in range(1, W-1):
    right_max_dp[i] = max(heights[i:])
    left_max_dp[i] = max(heights[:i])
    # if i == 0:
    #     right_max_dp[i] = heights[-1]
    #     left_max_dp[i] = heights[0]
    # else:
    #     right_max_dp[W-i-1] = max(right_max_dp[W-i], heights[W-i-1])
    #     left_max_dp[i] = max(left_max_dp[i-1], heights[i])
answer = 0
# print(left_max_dp, right_max_dp)
for hi, height in enumerate(heights):
    if hi == 0 or hi == W-1:
        continue
    block = min(right_max_dp[hi],left_max_dp[hi])
    answer += block - height if block > height else 0 
print(answer)
# heights = [0] + heights + [0]
# # diff = [0 for _ in range(len(heights))]
# answer = 0

# divs = []
# for i in range(1, W+1):
#     l, c, r = i-1, i, i+1
#     if (heights[c] - heights[l] >= 0 and heights[r] - heights[c] <= 0):
#         divs.append(i)
# # print(divs)
# for di, div in enumerate(divs):
#     if di == len(divs)-1:
#         break
#     first, second = heights[div], heights[divs[di+1]]
#     block = min(first, second)
#     for i in range(div, divs[di+1]+1):
#         answer += block - heights[i] if block > heights[i] else 0
# for i in range(1, W-1):
#     left, right = heights[i-1], heights[i+1]
    
# print(answer)