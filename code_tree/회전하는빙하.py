import sys
sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, Q = map(int, readl().strip().split(' ')) # 회전 가능 레벨, 회전 횟수 #

board = [list(map(int, readl().strip().split(' '))) for _ in range(2**N)]

levels = list(map(int, readl().strip().split(' ')))
import copy
# DX, DY = [1, 0, -1, 0], [0, 1, 0, -1]
DX, DY = [0, 1, 0, -1], [-1, 0, 1, 0] # 상-우-하-좌
def rotate_patch(patch):
    n = len(patch)
    new_patch = [[0 for _ in range(n)] for _ in range(n)]
    for y in range(n):
        for x in range(n):
            new_patch[n-y-1][x] = patch[y][x]

def get_four_idx(x, y, x1, y1, ps):
    if (x1 <= x < x1 + ps):
        if (y1 <= y < y1 + ps):
            return 1 # 0->1
        else:
            return 0 # 3->0
    else:
        if (y1 <= y < y1+ps):
            return 2 # 1->2
        else:
            return 3 # 2->3
def rotate_all():
    global board
    new_board = [[0 for _ in range(2**N)] for _ in range(2**N)]
    for level in levels:
        if level == 0:
            board = melt_ice()
            continue
        patch_size = 2 ** (level)
        for y in range(0, 2**N, patch_size):
            for x in range(0, 2**N, patch_size):
                x1, y1, x2, y2 = x, y, x+patch_size, y+patch_size
                for yy in range(y1, y2):
                    for xx in range(x1, x2):
                        idx = get_four_idx(xx, yy, x1, y1, patch_size//2)
                        # print(xx, yy, idx)
                        nx, ny = xx + DX[idx]*patch_size//2, yy + DY[idx]*patch_size//2
                       #  print(nx, ny, board[yy][xx], xx, yy, idx)
                        new_board[ny][nx] = board[yy][xx]
        board = copy.deepcopy(new_board)
        board = melt_ice()
        # print(board)
    # print(new_board)
    
def in_range(x, y):
    return 0 <= x < 2**N and 0 <= y < 2**N

def melt_ice():
    global board
    new_board = [[0 for _ in range(2**N)] for _ in range(2**N)]
    for y in range(2**N):
        for x in range(2**N):
            cnt_ice=  0
            # if board[y][x] == 0:
            #     continue
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) == False:
                    continue
                if board[ny][nx] == 0:
                    continue
                cnt_ice += 1
            if cnt_ice < 3:
                new_board[y][x] = max(board[y][x] - 1, 0)
            else:
                new_board[y][x] = board[y][x]
    # board = copy.deepcopy(new_board)
    return new_board
    # board = new_board

def get_largest_ice():
    global board
    from collections import deque
    
    check = [[False for _ in range(2**N)] for _ in range(2**N)]
    MAX_SIZE = 0
    total_ice = sum([sum(arr) for arr in board])
    # print(board)
    for y in range(2**N):
        for x in range(2**N):
            if check[y][x] == True:
                continue
            if board[y][x] == 0:
                continue
            q = deque([[x, y]])
            visited = [[False for _ in range(2**N)] for _ in range(2**N)]
            visited[y][x] = True
            check[y][x] = True
            s = 0
            while  q:
                xx, yy= q.popleft()
                s += 1
                for dx, dy in zip(DX, DY):
                    nx, ny = xx + dx, yy + dy
                    if in_range(nx, ny) == False:
                        continue
                    if board[ny][nx] == 0:
                        continue
                    if visited[ny][nx] != False:
                        continue
                    visited[ny][nx] = True
                    q.append([nx, ny])
                    check[ny][nx] = True
                    
            MAX_SIZE= max(MAX_SIZE, s)
                    
    return total_ice, MAX_SIZE

rotate_all()
total, size = get_largest_ice()
print(f"{total}\n{size}")

# print(board)