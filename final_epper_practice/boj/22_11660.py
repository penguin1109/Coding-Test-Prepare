""" BOJ 11660 - 구간 합 구하기 5
"""
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10 ** 8)

N, M = map(int, input().strip().split(' ')) # 표의 크기, 합을 구해야 하는 횟수 #

board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
dp = [[0 for _ in range(N)] for _ in range(N)]

dp[0][0] = board[0][0]
dp[0][1] = board[0][1] + dp[0][0]
dp[1][0] = board[1][0] + dp[0][0]
for x in range(1, N):
    dp[0][x] = dp[0][x-1] + board[0][x]
for y in range(1, N):
    dp[y][0] = dp[y-1][0] + board[y][0]
    
for y in range(1, N):
    for x in range(1, N):
        # dp[y][x] = dp[y-1][x] + sum(board[y][:x]) + board[y][x]
        dp[y][x] = dp[y][x-1] + dp[y-1][x] - dp[y-1][x-1] + board[y][x]
        
# print(dp)
for m in range(M):
    x1, y1, x2, y2 = map(int, input().strip().split(' '))
    x1 -= 1;y1 -= 1;x2 -= 1;y2 -= 1;
    top_rm = dp[x1-1][y2] if x1 != 0 else 0
    left_rm = dp[x2][y1-1] if y1 != 0 else 0
    save = dp[x1-1][y1-1] if x1 != 0 and y1 != 0 else 0
    # print(f"{top_rm} {left_rm} {save}")
    print(dp[x2][y2] - top_rm - left_rm + save)
    

