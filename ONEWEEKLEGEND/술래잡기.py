""" 술래잡기
<조건>
1. m명의 도망자가 있으며, 격자는 nxn의 크기.
2. 술래의 위치: 무조건 격자의 중앙
   도망자 m명의 위치: 처음 지정된 곳
3. 도망자는 좌우 / 상하 로 움직이는 2개의 유형.
   좌우: 오른쪽     상하: 아래쪽
4. 나무와 도망자는 초기에 겹쳐서 주어질 수 있다.

<게임 진행 방법>
1. (m명의 도망자가 먼저 -> 술래) x K번 반복

2. 도망자는 현재 술래와의 거리가 3이하인 경우에만 움직일 수 있음 (유클리디안 거리로 계산)
    2-1-1. 바라보는 방향으로 1칸 이동하는데 격자 안에 있는 경우 술래가 있으면 움직이지 않는다.
    2-1-2. 움직이려는 칸에 술래가 없으면 이동 가능
    2-2-1. 격자를 벗어나는 경우 반대로 방향을 이동
    2-2-2. 술래가 없으면 이동, 없으면 이동할 수 없음. (대신 방향이 반대로 바뀐건 유지 해야 함)

3. 술래는 위 방향에서 시작하여 달팽이 모양으로 움직인다. (이걸 1TURN이라고 한다.)
    3-1-1. 이동 직후 바라보는 방향 기준 현재 칸 포함 3칸 이내에 있는 도망자를 잡는다. 잡힌 도망자는 없어진다.
    3-1-2. 만약에 도망자가 나무에 가려지면 잡지 못한다.
    3-1-3. (현재 턴 x 현재 턴에서 잡힌 도망자의 수) 만큼의 점수를 술래가 얻는다.
    3-2-1. 이동 후에 이동방향이 틀어지는 지점이면 바로 방향을 틀어준다.
    3-2-2. 양끝, 정중앙에 도달하게 되는 경우에는 방향을 2번 틀어주어야 한다.

K번에 걸쳐 술래잡기를 하는 동안 술래가 얻게 되는 점수를 출력하여라.
"""

N, M, H, K = map(int, input().split(' '))

catcher = [N//2, N//2, 0, 1] # 술래의 위치 (처음에는 좌표의 중앙), 술래의 방향, 술래의 이동 거리
runners = []
trees = [[0 for _ in range(N)] for _ in range(N)] # 나무의 위치는 변하지 않음
SNAIL = 1 # 술래가 정방향을 향해 움직이면 1, 아니면 -1

DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]

def swap_dir(d):
    if d in [0, 2]:
        return abs(2-d)
    if d in [1, 3]:
        return (4-d)

def calc_dist(ax, ay, bx, by):
    return abs(ax-bx) + abs(ay-by)

def check_range(x, y):
    if (0 <= x < N) and (0 <= y < N):
        return True
    return False

VALID_RUNNER = [True for _ in range(M)]
def find_runner(x, y):
    cnt = 0
    for idx, runner in enumerate(runners):
        if (VALID_RUNNER[idx] is True) and runner[0] == x and runner[1] == y:
            VALID_RUNNER[idx] = False
            cnt += 1
    return cnt


for m in range(M):
    x, y, d = map(int, input().split(' ')) # 도망자의 위치, 이동 방법
    if d == 1: # 좌우로만 움직이는 경우
        runners.append([x-1, y-1, 1]) # 오른쪽
    elif d == 2: # 상하로만 움직이는 경우
        runners.append([x-1, y-1, 2]) # 아래

for h in range(H):
    x, y = map(int, input().split(' ')) # 나무의 위치
    trees[x-1][y-1] = 1 # 나무가 있음을 나타내 준다.

def get_catcher_dir():
    cx, cy = catcher[0], catcher[1]
    move_dir = 0
    if SNAIL == 1:
        move_dir = catcher_next_dir[cx][cy]
    else:
        move_dir = catcher_rev_dir[cx][cy]
    return move_dir

def catcher_view():
    cx, cy, cd, cm = catcher # 술래의 좌표, 술래의 방향, 술래의 이동 거리
    cd = get_catcher_dir()
    catcher[2] = cd
    catched = 0
    for i in range(3):
        nx, ny = cx + DX[cd] * i, cy + DY[cd] * i # 시야에는 현재 술래가 있는 칸도 포함한다.
        if check_range(nx, ny):
            # 해당 칸에 나무가 있으면 안됨
            if trees[nx][ny] != 1:
                caught = find_runner(nx, ny)
                # print(caught)
                catched += caught

    return catched

def move_runner(x, y, d, cx, cy):
    nx, ny = x + DX[d], y + DY[d]
    if check_range(nx, ny):
        d = swap_dir(d)
        nx, ny = x + DX[d], y + DY[d]
    if (nx == cx and ny == cy):
        return x, y, d
    else:
        return nx, ny, d

catcher_next_dir = [
    [0 for _ in range(N)] for _ in range(N)
]

catcher_rev_dir = [
    [0 for _ in range(N)] for _ in range(N)
]

def make_catcher_path():
    cx, cy, cd, cm = catcher
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

def check_snail():
    global SNAIL
    # 정방향이면서 좌측 상단에 있으면 역방향으로 변경
    if catcher[0] == 0 and catcher[1] == 0 and SNAIL == 1:
        SNAIL = -1
    #  역방향이면서 중점에 있으면 정방향으로 변경
    if catcher[0] == N//2 and catcher[1] == N//2 and SNAIL == -1:
        SNAIL = 1

def move_catcher():
    cx, cy, cd, cm = catcher
    nd = get_catcher_dir()
    catcher[2] = nd

    nx = cx + DX[nd]
    ny = cy + DY[nd]
    catcher[0] = nx
    catcher[1] = ny

    check_snail() # 역방향 회전인지 정방향 회전인지 확인한다.

    return nx, ny


def simulate():
    catcher_score = 0

    for k in range(K):
        cx, cy, cd, cm = catcher
        # STEP 1: 먼저 도망자들이 움직인다.
        for idx, runner in enumerate(runners):
            if VALID_RUNNER[idx] and calc_dist(runner[0], runner[1], cx, cy) <= 3:
                nx, ny, nd = move_runner(runner[0], runner[1], runner[2], cx, cy)
                runners[idx][:3] = [nx, ny, nd]

        # STEP 2: 이제 술래가 움직인다.
        cx, cy = move_catcher()
        catcher[0] = cx
        catcher[1] = cy

        # STEP 3: 술래의 시야를 바탕으로 점수를 업데이트 한다.
        md = get_catcher_dir()
        catcher[2] = md
        score = catcher_view()
        catcher_score += (k+1) * score

        # STEP 4: 술래가 방향을 틀어야 한다면 방향을 바꾸어 준다.
        # cd = check_catcher_change_dir()
        # catcher[2] = cd

    return catcher_score

make_catcher_path()
print(simulate())








