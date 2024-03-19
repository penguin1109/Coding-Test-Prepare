import sys
input = sys.stdin.readline

N, M, H, K = map(int, input().strip().split(' '))

RUNNER = []
TREE = [[False for _ in range(N)] for _ in range(N)] # 나무는 고정되기 때문에 그냥 위치 확인용으로 배열 사용 #
DX, DY = [0, 1, 0, -1], [-1, 0, 1, 0] # 위-오-아-왼 #
RX, RY = N//2, N//2 # 술래의 초기 위치 #
IS_CLOCK = True # 0이면 시계 방향 회전, 1이면 반시계 방향 회전 #
CLOCK = [[-1 for _ in range(N)] for _ in range(N)]
COUNTER = [[-1 for _ in range(N)] for _ in range(N)]
BOARD = [[[] for _ in range(N)] for _ in range(N)]
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def init_runner_dir():
    global CLOCK, COUNTER
    sx, sy = N//2, N//2
    move = 1
    iter = 1
    dir = 0
    while True:
        for _ in range(move):
            CLOCK[sy][sx] = dir
            nx, ny = sx + DX[dir], sy + DY[dir]
            sx, sy = nx, ny
            COUNTER[sy][sx] = (dir+2)%4
            if sx == 0 and sy == 0:
                return

        if iter == 2:
            iter = 1;move += 1
        else:
            iter += 1
        dir = (dir+1)%4
    COUNTER[0][0] = 2
    CLOCK[N//2][N//2] = 0

for m in range(M):
    y, x, d = map(int, input().strip().split(' '))
    if d == 1:
        RUNNER.append((x-1, y-1, 1))
    else:
        RUNNER.append((x-1, y-1, 2))

    BOARD[y-1][x-1].append(m)

for _ in range(H):
    y, x = map(int, input().strip().split(' '))
    TREE[y-1][x-1] = True

'''[출력] 술래가 K번의 턴동안 얻게 되는 총 점수'''
def can_move(x, y, dir):
    nx, ny = x + DX[dir], y + DY[dir]
    if in_range(nx, ny):
        if (RX, RY) == (nx, ny): # 술래가 위치하는 경우 #
            return x, y, dir
        return nx, ny, dir
    else:
        dir = (dir+2)%4
        nx, ny = x + DX[dir], y + DY[dir]
        if (RX, RY) == (nx, ny):
            return x, y, dir
        return nx, ny, dir

def move_runner():
    global BOARD
    new_board = [[[] for _ in range(N)] for _ in range(N)]
    for i, (x, y, dir) in enumerate(RUNNER):
        if dir == -1:
            continue
        dist = abs(x-RX) + abs(y-RY)
        if dist <= 3:
            xx, yy, new_dir = can_move(x, y, dir)
            RUNNER[i] = (xx, yy, new_dir)
            new_board[yy][xx].append(i)
        else:
            new_board[y][x].append(i)
    BOARD = new_board

def move_catcher(turn):
    global RX, RY, IS_CLOCK, answer
    cur_dir = CLOCK[RY][RX] if IS_CLOCK else COUNTER[RY][RX]
    RX, RY = RX + DX[cur_dir], RY + DY[cur_dir]
    if (RX, RY) == (0, 0):
        IS_CLOCK = False
    if (RX, RY) == (N//2, N//2):
        IS_CLOCK = True
    # 이동 후에 위치의 방향을 사용 #
    DIR = CLOCK[RY][RX] if IS_CLOCK else COUNTER[RY][RX]
    ## 잡기 ##
    nx, ny = RX, RY
    cnt = 0
    for _ in range(3):
        if in_range(nx, ny) == False:
            break
        if TREE[ny][nx] == False:
            cnt += len(BOARD[ny][nx])
            for i in BOARD[ny][nx]:
                xx, yy = RUNNER[i][0], RUNNER[i][1]
                RUNNER[i] = (xx, yy, -1)
            BOARD[ny][nx] = []
        nx, ny = nx + DX[DIR], ny + DY[DIR]
    answer += cnt * turn





#################### MAIN ####################
init_runner_dir()
answer = 0
def simulate(turn):
    move_runner()
    move_catcher(turn)

for turn in range(1, K+1):
    simulate(turn)

print(answer)