import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline
# ADX, ADY = [1, -1, -1, 1], [-1, -1, 1, 1] # 반시계 #
# CDX, CDY = [-1, 1, 1, -1], [-1, -1, 1, 1]# 시계 #
DX, DY = [1, -1, -1, 1], [-1, -1, 1, 1]
idx = [
    [0, 1, 2, 3], [1, 0, 3, 2]
]
# [출력] 회전 이후의 격자의 상태 #

N= int(readl().strip()) # 격자의 크기 #

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]
import copy

new_board = copy.deepcopy(board)

r, c, m1, m2, m3, m4, dir = map(int, readl().strip().split(' '))
moves = [m1, m2, m3, m4]
r -= 1;c -= 1
# if dir == 0: # 반시계 #
#     DX, DY = ADX, ADY
# else:
#     DX, DY = CDX, CDY
prev_x, prev_y = c, r
for i in range(4):
    dx, dy = DX[idx[dir][i]], DY[idx[dir][i]]
    # print(f"MOVE : {moves[idx[dir][i]]}, {idx[dir][i]}")
    for m in range(moves[idx[dir][i]]):
        x, y = prev_x + dx, prev_y + dy
        # print(prev_x, prev_y, x, y)
        if in_range(x, y) == False:
            # print(x, y)
            break
        new_board[y][x] = board[prev_y][prev_x]
        prev_x, prev_y = x, y

for y in range(N):
    arr = [str(i) for i in new_board[y]]
    print(' '.join(arr))

