N, M, H, K = map(int, input().split(' '))

runners = [
    [[] for _ in range(N)] for _ in range(N)
]

next_runners = [
    [[] for _ in range(N)] for _ in range(N)
]

tree = [[0 for _ in range(N)] for _ in range(N)]

catcher_next_dir = [
    [0 for _ in range(N)] for _ in range(N)
]

catcher_rev_dir = [
    [0 for _ in range(N)] for _ in range(N)
]
CATCHER_POS = (N//2, N//2)
SNAIL = 1
CATCHER_SCORE = 0

for _ in range(M):
    x, y, d = map(int, input().split(' '))
    runners[x-1][y-1].append(d)
for _ in range(H):
    x, y = map(int, input().split(' '))
    tree[x-1][y-1] = 1

def make_catcher_path():
    DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]
    cx, cy = N//2, N//2
    cd, cm = 0, 1

    # 계산의 편의를 위해서 각 위치마다 술래가 이동해야 하는 방향을 저장해둔다.
    while cx or cy:
        for _ in range(cm):
            # cm만큼 움직인다.
            catcher_next_dir[cx][cy] = cd
            cx, cy = cx + DX[cd], cy + DY[cd]
            catcher_rev_dir[cx][cy] = cd + 2 if cd < 2 else cd -2

            if cx == 0 and cy == 0:
                break
        cd = (cd + 1) % 4
        if cd == 0 or cd == 2:
            cm += 1

def check_range(x, y):
    return (0 <=  x < N and 0 <= y < N)

def move_runner(x, y, dir):
    DX, DY = [0, 0, 1, -1], [-1, 1, 0, 0]
    nx, ny = x + DX[dir], y + DY[dir]

    if not check_range(nx, ny):
        dir = 1 - dir if dir < 2 else 5 - dir
        nx, ny = x + DX[dir], y + DY[dir]
    if (nx, ny) != CATCHER_POS:
        next_runners[nx][ny].append(dir)
    else:
        next_runners[x][y].append(dir)

def calc_dist(x, y):
    cx, cy = CATCHER_POS
    return abs(x-cx) + abs(y-cy)

def check_snail():
    global SNAIL
    # 정방향이면서 좌측 상단에 있으면 역방향으로 변경
    if CATCHER_POS == (0, 0) and SNAIL == 1:
        SNAIL = -1
    #  역방향이면서 중점에 있으면 정방향으로 변경
    if CATCHER_POS == (N//2, N//2) and SNAIL == -1:
        SNAIL = 1

def get_catcher_dir():
    cx, cy = CATCHER_POS
    move_dir = 0
    if SNAIL == 1:
        move_dir = catcher_next_dir[cx][cy]
    else:
        move_dir = catcher_rev_dir[cx][cy]
    return move_dir

def move_catcher():
    global CATCHER_POS
    x, y = CATCHER_POS
    DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]
    md = get_catcher_dir()
    CATCHER_POS = (x + DX[md], y + DY[md])
    check_snail()

def catcher_view():
    DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]
    x, y = CATCHER_POS
    md = get_catcher_dir()
    caught = 0
    for i in range(3):
        nx, ny = x + DX[md] * i, y + DY[md] * i
        if check_range(nx, ny) and tree[nx][ny] == 0:
            caught += len(runners[nx][ny])
            runners[nx][ny] = []
    return caught

def move_runners():
    for i in range(N):
        for j in range(N):
            next_runners[i][j] = []
    for i in range(N):
        for j in range(N):
            if calc_dist(i, j) <= 3:
                for md in runners[i][j]:
                    move_runner(i, j, md)
            else:
                for md in runners[i][j]:
                    next_runners[i][j].append(md)
    for i in range(N):
        for j in range(N):
            runners[i][j] = next_runners[i][j]

def run():
    ANSWER = 0
    make_catcher_path()
    for k in range(K):
        move_runners()
        move_catcher()
        score = catcher_view()
        ANSWER += (k+1)*score
    return ANSWER

print(run())


