import sys, copy
input = sys.stdin.readline

N, M = map(int, input().strip().split(' ')) # 격자의 크기, 총 라운드의 수 #
DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # [오, 아래, 왼, 위] #
INDEX = []

board = [list(map(int, input().strip().split(' '))) for _ in range(N)]

def debug(board):
    print("*" * 30)
    for arr in board:
        print(' '.join([str(a) for a in arr]))
    print("*" * 30)
    
def make_board():
    global INDEX
    ## 미리 소용돌이 모양으로 회전 했을 때 배열에 들어갈 수 있는 각 위치를 나타내 줌 ##
    move = 1
    x, y = N//2, N//2
    INDEX.append((x, y))
    while True:
        if x == 0 and y == 0:
            return
        for di in [2, 1, 0, 3]:
            for mv in range(move):
                x, y = x + DX[di], y + DY[di]
                INDEX.append((x, y))
                if x == 0 and y == 0:
                    return
            if di == 1 or di == 3:
                move += 1

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def get_index(x, y):
    global INDEX
    return INDEX.index((x, y))

def remove(board):
    search_idx = 1
    color_list = []
    score = 0
    REMOVED = []
    while (search_idx < len(INDEX)):
        start_idx = search_idx
        color = board[INDEX[search_idx][1]][INDEX[search_idx][0]]
        if color == 0:
            break
        cnt = 0
        while (color == board[INDEX[search_idx][1]][INDEX[search_idx][0]]):
            search_idx += 1
            cnt += 1
            if search_idx == len(INDEX):
                break
        if cnt >= 4:
            score += cnt * color
            REMOVED.extend([i for i in range(start_idx, search_idx)])
            # print(start_idx, search_idx)
        elif color != 0:
            color_list.append(cnt)
            color_list.append(color)
            # color_list.append((cnt, color))
    if REMOVED:
        for i in REMOVED:
            x, y = INDEX[i]
            board[y][x] = -2

        return color_list, score
    return color_list, score

def simulate(d, p):
    global board, answer
    score = 0
    
    ax, ay = N//2, N//2
    for i in range(p):
        x = ax + DX[d] * (i+1)
        y = ay + DY[d] * (i+1)
        if in_range(x, y) and board[y][x] > 0:
            score += board[y][x]
            board[y][x] = -2
    # debug(board)
    
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    dst_idx = 0
    for i, (x, y) in enumerate(INDEX):
        if board[y][x] >= 0:
            dst_x, dst_y = INDEX[dst_idx]
            new_board[dst_y][dst_x] = board[y][x]
            dst_idx += 1
    # debug(new_board)
    ## (3) ##
    while True:
        color_list, removed = remove(new_board)
        score += removed
        # print(color_list, removed)
        temp = copy.deepcopy(new_board)
        dst_idx = 0
        for i, (x, y) in enumerate(INDEX):
            if new_board[y][x] >= 0:
                dst_x, dst_y = INDEX[dst_idx]
                temp[dst_y][dst_x] = new_board[y][x]
                dst_idx += 1
        new_board = temp
        if removed == 0:
            break
    ## (4) ##
    final_board = [[0 for _ in range(N)] for _ in range(N)]
    idx = 1
    for i in range(len(color_list)):
        final_board[INDEX[idx][1]][INDEX[idx][0]] = color_list[i]
        if idx+1 == len(INDEX):
            break
        idx += 1
    board = final_board
    answer += score
    
make_board()
answer = 0

for _ in range(M):
    d, p = map(int, input().strip().split(' '))
    simulate(d, p)
    # debug(board)
    

print(answer)
        