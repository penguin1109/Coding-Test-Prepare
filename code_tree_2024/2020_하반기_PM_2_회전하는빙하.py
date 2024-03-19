import sys
from collections import deque

input = sys.stdin.readline
'''[출력] 격자에 남은 빙하의 총 양 (= 숫자의 합) & 가장 큰 얼음 군집의 크기'''
N, Q = map(int, input().strip().split(' ')) # 회전 가능 레벨, 회전 횟수 #
board = [list(map(int, input().strip().split(' '))) for _ in range(2**N)]
levels = list(map(int, input().strip().split(' '))) # 길이가 Q -> 긱긱의 레벨대로 회전을 시켜 주면 됨 #

DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]

def in_range(x, y):
    return 0 <= x < 2**N and 0 <= y < 2**N

def make_group(x, y, visited):
    q = deque([(x, y)])
    cnt = 1 # board[y][x]
    visited[y][x] = True
    while q:
        a, b = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = a + dx, b + dy
            if in_range(nx, ny) and visited[ny][nx] == False and board[ny][nx] > 0:
                visited[ny][nx] = True
                cnt += 1 # board[ny][nx]
                q.append((nx,ny))
    return cnt, visited

def get_answer():
    max_size = 0
    visited = [[False for _ in range(2**N)] for _ in range(2**N)]
    total_size = sum([sum(arr) for arr in board]) # 숫자의 합 #
    for y in range(2 ** N):
        for x in range(2**N):
            if board[y][x] != 0 and visited[y][x] == False:
                temp, visited = make_group(x, y, visited)
                max_size = max(max_size, temp)
    return total_size, max_size
        
def melt():
    global board
    new_board = [[0 for _ in range(2**N)] for _ in range(2**N)] # 동시에 얼음이 녹기 때문에 new_board를 사용해야 함 #
    for y in range(2**N):
        for x in range(2**N):
            cnt = 0
            if board[y][x] > 0:
                for di, (dx, dy) in enumerate(zip(DX, DY)):
                    nx, ny = x + dx, y + dy
                    if in_range(nx, ny) and board[ny][nx] > 0:
                        cnt += 1
                if cnt < 3:
                    new_board[y][x] = board[y][x] - 1
                else:
                    new_board[y][x] = board[y][x]
    return new_board

def get_dimension(sx, sy, xx, yy, square_size):
    dx, dy = xx - sx, yy - sy
    if dx < square_size and dy < square_size:
        dim = 0
    elif dx >= square_size and dy < square_size:
        dim = 1
    elif dx >= square_size and dy >= square_size:
        dim = 2
    else:
        dim = 3
        
    return dim

def rotate(level):
    square_size = 2 ** (level-1)

    DIM_DICT = {
        0 : [square_size, 0], 
        1 : [0, square_size],
        2 : [-square_size, 0],
        3 : [0, -square_size]
    }
    global board
    if level == 0:
        return board
    new_board = [[0 for _ in range(2**N)] for _ in range(2**N)]
    # 큰 2^L x 2^L짜리 구역으로 나누기 #
    for sy in range(0, 2**N, 2**level):
        for sx in range(0, 2**N, 2**level):
            # 각 영역을 4등분 하기 #
            # print("SXSY ",sx, sy)
            for yy in range(sy, sy+2**level, 1): #, square_size):
                for xx in range(sx, sx+2**level, 1): #, square_size):
                    # print("XXYY ", xx, yy)
                    dim = get_dimension(sx, sy, xx, yy, square_size)
                    nx,ny= DIM_DICT[dim][0] + xx, DIM_DICT[dim][1] + yy
                    new_board[ny][nx] = board[yy][xx]
                    # new_board[ny:ny+square_size][nx:nx+square_size] = board[yy:yy+square_size][xx:xx+square_size]
        
        
    return new_board
        

for level in levels:
    board = rotate(level)
    # print(board)
    board = melt()
    # print(board)
    
total_size, max_size = get_answer()
print(total_size)
print(max_size)