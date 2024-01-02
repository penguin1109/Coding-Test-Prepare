import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

def print_answer(board):
    for y in range(N):
        arr = [str(i) for i in board[y]]
        print(' '.join(arr))

N = int(readl().strip()) # 격자의 크기 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

y, x = map(int, readl().strip().split(' '))
y -= 1;x -= 1

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def gravity(board):
    import copy
    new_board = copy.deepcopy(board)
    for x in range(N):
        prev_empty = -1
        for y in range(N-1, -1, -1):
            if board[y][x] == 0: # 밑에서부터 찾다가 비어 있으면 #
                prev_empty = y
                break
        if prev_empty != -1:
            py = prev_empty
            for y in range(prev_empty, 0, -1):
                if board[y-1][x] != 0:
                    new_board[py][x] = board[y-1][x]
                    new_board[y-1][x] = 0
                    py -= 1
            new_board[0][x] = 0

    return new_board
def bomb(x, y):
    global board
    size = board[y][x]
    # if size == 1:
    #     board[y][x] = 0
    #     board = gravity(board)
    #     return
    mv = 0
    board[y][x] = 0
    for yy in range(y-1, -1, -1):
        mv += 1;board[yy][x] = 0
        if mv == size-1:break
    mv = 0
    for yy in range(y+1, N):
        mv += 1;board[yy][x] = 0
        if mv == size-1:break
    mv = 0
    for xx in range(x-1, -1, -1):
        mv += 1;board[y][xx] = 0
        if mv == size-1:break
    mv = 0
    for xx in range(x+1, N):
        mv += 1;board[y][xx] = 0
        if mv == size-1:break
    print(board)
    board = gravity(board)


bomb(x, y)
print_answer(board)