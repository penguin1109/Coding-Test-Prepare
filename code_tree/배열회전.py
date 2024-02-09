n, m, k = map(int, input().strip().split(' '))
board = [list(map(int, input().strip().split(' '))) for _ in range(n)]

# 각 회전마다 돌려야 하는 배열의 크기로 modular 연산으로 반복을 k번 전부 하지 않도록 한다 #
# 회전을 하려 할 때 전체를 1D로 flatten하고 index를 더하는 방법으로 계산해야 한다 #
def print_answer(board):
    for arr in board:
        print(*arr)
    
def answer():
    global n, m
    p = 0
    for _ in range(min(n, m) // 2):
        rotate(p, p)
        p += 1
        n -= 2
        m -= 2
    print_answer(board)
           
def rotate(sx, sy):
    global board
    length_1d = (n-1) * 2 + (m-1) * 2
    # n, m은 각각 세로 길이, 가로 길이 #
    row = [0 for _ in range(length_1d)]
    idx = 0
    # (1) Flattened 1D 배열 만들기 #
    for x in range(sx, sx+m-1):
        row[(idx-k) % length_1d] = board[sy][x]
        idx += 1
    for y in range(sy, sy+n-1):
        row[(idx-k) % length_1d] = board[y][sx+m-1]
        idx += 1
    for x in range(sx+m-1,sx, -1):
        row[(idx-k)%length_1d] = board[sy+n-1][x]
        idx += 1
    for y in range(sy+n-1, sy, -1):
        row[(idx-k) % length_1d] = board[y][sx]
        idx += 1
    
    # (2) 다시 2D 배열에 채워 넣기 #
    idx = 0
    for x in range(sx, sx+m-1):
        board[sy][x] = row[idx]
        idx += 1
    for y in range(sy, sy+n-1):
        board[y][sx+m-1] = row[idx]
        idx += 1
    for x in range(sx+m-1, sx, -1):
        board[sy+n-1][x] = row[idx]
        idx += 1
    for y in range(sy+n-1, sy, -1):
        board[y][sx] = row[idx]
        idx += 1

answer()

