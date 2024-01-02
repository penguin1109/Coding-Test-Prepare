import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N, M, Q = map(int, readl().strip().split(' ')) # 세로, 가로, 바람이 부는 횟수 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]
"""
- 직사각형의 가장자리 부분의 회전을 수행하기 위해서는 어쩔 수 없이 왼쪽, 아래, 오른쪽, 위의 4개의 부분을 나눠서 shift를 해야 한다.
- 동시에 어떤 작업이 일어나는 경우에는 당연히 새로운 배열에 copy해 주면 된다.
"""
def blow_wind(x1,y1,x2,y2):
    # 주의 할 것은 경계에 있는 값만 변경을 하게 된다는 것이다. #
    import copy
    global board
    new_board = copy.deepcopy(board)
    px, py = x1, y1
    for x in range(x1, x2+1):
        new_board[y1][x] = board[py][px]
        px, py = x, y1; # indexes.append([x, y1])
    for y in range(y1+1, y2+1):
        new_board[y][x2] = board[py][px]
        px, py = x2, y; # indexes.append([x2, y])
    for x in range(x2-1, x1-1, -1):
        new_board[y2][x] = board[py][px]
        px, py = x, y2; # indexes.append([x, y2])
    for y in range(y2-1, y1-1, -1):
        new_board[y][x1] = board[py][px]
        px, py = x1, y; # indexes.append([x1, y])
    # print(board, new_board)
    new_board = change_value(x1,y1,x2,y2, new_board)
    return new_board

def in_range(x, y):
    return 0 <= x < M and 0 <= y < N
def change_value(x1, y1, x2, y2, new_board):
    import copy
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    new = copy.deepcopy(new_board)

    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            add = new_board[y][x];cnt = 1
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) == False:
                    continue
                add += new_board[ny][nx];cnt += 1
            new[y][x] = add // cnt
            # print(x, y, add, cnt)
    return new



for q in range(Q):
    y1, x1, y2, x2 = map(int, readl().strip().split(' '))
    y1 -= 1;x1 -= 1;y2 -= 1;x2 -=1
    board = blow_wind(x1,y1,x2,y2)
    print(board)

for y in range(N):
    arr = [str(n) for n in board[y]]
    print(' '.join(arr))