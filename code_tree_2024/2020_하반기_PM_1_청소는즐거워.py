import sys
input = sys.stdin.readline
import math
N = int(input().strip())
board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
'''

[출력] 격자 바깥으로 나간 먼지의 양
'''
DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1] # 좌 하 우 상 #
DIR_DICT = {
    ## 전부 prev 기준으로! ##
    # 0 : [[0, -1, 1], [0, 1, 1], [-1, -1, 7], [-1, -2, 2], [-1, 1, 7], [-1, 2, 2], [-2, -1, 10], [-2, 1, 10], [-3, 0, 5]],
    0 : [[1, -1, 1], [1, 1, 1], [0, -1, 7], [0, -2, 2], [0,1,7], [0, 2, 2], [-1, -1, 10], [-1, 1, 10], [-2, 0, 5]],
    1 : [[-1, -1, 1], [1, -1, 1], [-1, 0, 7], [-2, 0, 2], [1,0,7], [2, 0, 2], [-1, 1, 10], [1, 1, 10], [0, 2, 5]],
    2 : [[-1, -1, 1], [-1,1, 1], [0, -1, 7], [0, -2, 2], [0, 1, 7], [0, 2, 2], [1, -1, 10], [1, 1, 10], [2, 0, 5]],
    3 : [[-1, 1, 1], [1, 1, 1], [-1, 0, 7], [-2, 0, 2], [1, 0, 7], [2, 0,2], [-1, -1, 10], [1, -1, 10], [0, -2, 5]]
}

# DIR_DICT[1] = [[y, -x, p] for (x, y, p) in DIR_DICT[0]]
# DIR_DICT[2] = [[-y, -x, p] for (x, y, p) in DIR_DICT[0]]
# DIR_DICT[3] = [[-y, x, p] for (x, y, p) in DIR_DICT[0]]
# print(DIR_DICT)
# 좌 -> 하 -> 우 -> 상 #
# dir_board = [[0 for _ in range(N)] for _ in range(N)]
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N
answer = 0
## (1) 먼저 방향 격자를 initialize 해줌 ##
# def initialize():
def run():
    # global dir_board
    sx, sy = N // 2, N // 2
    step = 1;iter = 1
    dir = 0
    # dir_board[sy][sx] = dir
    
    while True:
        for s in range(step):
            # clean(sx, sy, dir)
            sx, sy = sx + DX[dir], sy + DY[dir]
            clean(sx, sy, dir)
            if sx == 0 and sy == 0:
                return
        dir = (dir+1)%4
        iter += 1
        if iter % 2 == 1:
            step += 1
            
def clean(x, y, dir):
    global board, answer

    # prev_x, prev_y = x, y
    # curr_x, curr_y = x + DX[dir], y + DY[dir]
    curr_x, curr_y = x, y
    prev_dust = board[curr_y][curr_x]
    add = 0
    for (dx, dy, p) in DIR_DICT[dir]:
        # nx, ny = prev_x + dx, prev_y + dy
        nx, ny = curr_x + dx, curr_y + dy
        move_dust = math.floor(prev_dust * (0.01 * p))
        # move_dust = math.floor(prev_dust * p / 100)
        if in_range(nx, ny) == False:
            answer += move_dust
        else:
            board[ny][nx] += move_dust
        add += move_dust
    ## a% 처리하기 ##
    # nx, ny = prev_x + DX[dir]*2, prev_y + DY[dir]*2
    nx, ny = curr_x + DX[dir], curr_y + DY[dir]
    if prev_dust > add:
        if in_range(nx, ny) == False:
            answer += (prev_dust - add)
        else:
            board[ny][nx] += (prev_dust-add)
    # board[y][x] = 0
    board[curr_y][curr_x] = 0
        
run()
    
print(answer)
            
            
    