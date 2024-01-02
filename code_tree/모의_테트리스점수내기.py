import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1] # 좌-우-상-하 #
shapes = [
    [[1,1,1,1]], [[1,1],[1,1]], [[0,1,0],[1,1,1]], [[1,0,0],[1,1,1]], [[0,1,1],[1,1,0]],
    [[1],[1],[1],[1]],
    [[0,1],[1,1],[0,1]], [[1,0],[1,1],[1,0]], [[1,1,1],[0,1,0]],
    [[0,1],[0,1],[1,1]], [[1,1,1],[0,0,1]], [[1,1],[1,0],[1,0]], [[1,1],[0,1],[0,1]], [[1,0],[1,0],[1,1]], [[1,1,1],[1,0,0]], [[0,0,1],[1,1,1]],
    [[0,1],[1,1],[1,0]], [[1,0],[1,1],[0,1]]
]
## [출력] 하나의 블럭을 떨어뜨려 얻을 수 있는 최대 점수 ##

N,M = map(int, readl().strip().split(' ')) # 세로, 가로 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

def in_range(x, y):
    return 0 <= x < M and 0 <= y < N

def drop_block(col, shape, board):
    import copy
    new_board = copy.deepcopy(board)
    real_points = []
    Y, X = len(shape), len(shape[0])
    for row in range(N):
        points = []
        valid = True
        for y in range(Y):
            for x in range(X):
                nx, ny = x + col, y + row
                if shape[y][x] == 1:
                    if in_range(nx, ny) == True:
                        if board[ny][nx] == 1 or y == N-1: # 바닥에 닿거나 해당 칸이 이미 채워져 있을 떄 #
                            valid = False
                            break
                    else:
                        valid = False
                        break
                    points.append([nx, ny])

        if valid == False:
            break
        else:
            real_points= points
    if len(real_points) != 0:
        for x, y in real_points:
            new_board[y][x] = 1
        return True, new_board
    else:
        return False, new_board


def check_score(board):
    score = 0
    for y in range(N-1, -1, -1):
        if sum(board[y]) == M:
            score += 1
    return score


answer = 0
def simulate(shape, board):
    global answer
    for col in range(M):
        ret, new_board = drop_block(col, shape, board)
        if ret == True:
            score = check_score(new_board)
            # print(new_board)
            answer = max(answer, score)
        # if ret == False:
        #     score = check_score(board)
        #     answer = max(answer, score)
        # else:
        #     simulate(shape, new_board)

import copy

for shape in shapes:
    new_board = copy.deepcopy(board)
    simulate(shape, new_board)

print(answer)

