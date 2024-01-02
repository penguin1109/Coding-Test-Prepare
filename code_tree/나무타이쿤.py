import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' ')) # 격자의 크기, 리브로수를 키우는 년수 #
# [출력] 해당 년수가 모두 지난 뒤 남아있는 리브로수의 높이의 총 합 #
DX, DY = [1, 1, 0, -1, -1, -1, 0, 1], [0, -1, -1, -1, 0, 1, 1, 1]
nutritions = [[0, N-1], [0, N-2], [1, N-1], [1, N-2]]
def new_pos(x, y):
    if x == N:x=0
    if x == -1:x=N-1
    if y == N:y=0
    if y == -1:y=N-1
    return x, y

def in_range(x, y):
    return 0 <= x < N and 0 <= y  <N

def simulate(dir, move_n):
    global nutritions, board
    ## (1) 영양제 이동 ##
    new = []
    for nutrition in nutritions:
        x, y = nutrition
        for n in range(move_n):
            x, y = new_pos(x + DX[dir], y + DY[dir])
        new.append([x, y])
        board[y][x] += 1
    # print(new)
    nutritions = []

    ## (2) 특수 영양제 투입 ##

    dirs = [1, 3, 5, 7]
    new_board = board
    for x, y in new:
        cnt = 0
        for d in dirs:
            # nx, ny = new_pos(x + DX[d], y + DY[d])
            nx, ny = x + DX[d], y + DY[d]
            if in_range(nx, ny) == False:
                continue
            if board[ny][nx] >= 1:
                cnt += 1
        new_board[y][x] += cnt
    # print(new_board)

    ## (3) 특수 영양제 투입한 리브로수 제외하고 높이가 2 이상인 경우 잘라서 특수 영양제 구매 ##
    for y in range(N):
        for x in range(N):
            if [x, y] not in new:
                if new_board[y][x] >= 2:
                    new_board[y][x] -= 2
                    nutritions.append([x, y])
    # print(new_board)
    return new_board



board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]
for m in range(M):
    D, P = map(int, readl().strip().split(' ')) # 이동 방향, 이동 칸 수 #
    board = simulate(D-1, P)
    # print(board)

    # print(nutritions)
answer = sum([sum(arr) for arr in board])
print(answer)