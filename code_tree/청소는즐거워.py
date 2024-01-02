import sys
sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 크기 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

# [출력] 바깥으로 나간 먼지의 양 #

MOVE_MAP = {
    0 : [[1, -1, 1], [1, 1, 1], [0, -1, 7], [0, -2, 2], [0,1,7], [0, 2, 2], [-1, -1, 10], [-1, 1, 10], [-2, 0, 5]],
    1 : [[-1, -1, 1], [1, -1, 1], [-1, 0, 7], [-2, 0, 2], [1,0,7], [2, 0, 2], [-1, 1, 10], [1, 1, 10], [0, 2, 5]],
    2 : [[-1, -1, 1], [-1,1, 1], [0, -1, 7], [0, -2, 2], [0, 1, 7], [0, 2, 2], [1, -1, 10], [1, 1, 10], [2, 0, 5]],
    3 : [[-1, 1, 1], [1, 1, 1], [-1, 0, 7], [-2, 0, 2], [1, 0, 7], [2, 0,2], [-1, -1, 10], [1, -1, 10], [0, -2, 5]]
}

answer = 0

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]

def arange_dust(x2, y2, dir):
    import math
    global board, answer
    org_dust = board[y2][x2]
    sum_dust = 0
    for dx, dy, p in MOVE_MAP[dir]:
        nx, ny = x2 + dx, y2 + dy
        temp = math.floor(org_dust * p / 100)
        # print(temp, end = ' ')
        if in_range(nx, ny):
            board[ny][nx] += temp
            # sum_dust += temp
        else:
            answer += temp
        sum_dust += temp
    ax, ay = x2+DX[dir], y2+DY[dir]
    left = org_dust - sum_dust
    if left > 0:
        if in_range(ax, ay):
            board[ay][ax] += left
        else:
            answer += left
    # board[y1][x1] = 0
    board[y2][x2] = 0
        
            
def simulate():
    global answer
    x, y = N//2, N//2
    move = 1
    # print(board)
    while True:
        for idx, (dx, dy) in enumerate(zip(DX, DY)):
            # print(x, y)
            for dist in range(move):
                nx, ny = x + dx, y + dy
                arange_dust(nx, ny, dir=idx)
                x, y = nx, ny
                if (x==0 and y==0):
                    return
            if idx == 1:
                move += 1
        move += 1
        
                
            
        
simulate()
print(answer)