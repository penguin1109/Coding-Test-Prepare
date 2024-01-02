import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N, M, H, K = map(int, readl().strip().split(' ')) # 칸의 수, 도망자의 수, 나무의 개수, 턴의 개수 #
"""
이동방향 (d)가 1인 경우 <좌우>, 2인 경우 <상하>로만 움직임
- 좌우 이동이면 오른쪽 보고 시작, 상하 이동이면 아래쪽 보고 시작 
- 풀이에 나와 있는대로 각각의 도망자의 거리를 업데이트하는 방법을 사용하면 오히려 시간 복잡도가 커지는 것을 확인하였다. 불필요하게 배열 복사 하는 과정에서 for문이 반복되기 때문인 것 같다.
"""
DX, DY = [0, 1, 0, -1], [-1, 0, 1, 0] # 상 - 우 - 하 - 좌 #
catcher_clock = [[0 for _ in range(N)] for _ in range(N)] # 시계방향으로 회전할때 술래의 이동 방향 #
catcher_anticlock = [[0 for _ in range(N)] for _ in range(N)] # 반시계방향으로 회전할 때 술래의 이동 방향 #
IS_CLOCK = True
def setup_move():
    """술래의 격자 위치별 이동방향을 설정해 주기 위한 함수임 -> 이동방향만 알면 다음 격자 위치는 알아서 정할 수 있다."""
    sx, sy = N//2, N//2
    move = 1
    dir = 0
    while sx or sy:
        for _ in range(move):
            catcher_clock[sy][sx] = dir
            sx, sy = sx + DX[dir], sy + DY[dir]
            catcher_anticlock[sy][sx] = (dir+2)%4
            if sx == 0 and sy == 0:
                break
        dir = (dir+1)%4
        if dir == 0 or dir == 2:
            move += 1




runners = []
board = [[[] for _ in range(N)] for _ in range(N)]
tree = [[0 for _ in range(N)] for _ in range(N)]
X, Y = N//2, N//2 # 술래의 위치 좌표 #

for m in range(M):
    y, x, d = map(int, readl().strip().split(' '))
    # if d == 1:
    #     runners.append([x-1, y-1, 1])
    # else:
    #     runners.append([x-1, y-1, 2])
    runners.append([x-1, y-1, d])

for h in range(H):
    y, x = map(int, readl().strip().split(' '))
    tree[y-1][x-1] = 1 # 사실 나무의 위치는 불변이기 때문에 따로 배열로 관리를 하는게 편할 것이다. #

##### (1) 도망자 이동 ######
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N
def runner_move():
    global runners
    for idx, runner in enumerate(runners):
        x, y, dir = runner
        dist = abs(x-X) + abs(y-Y)
        if dist > 3:
            continue
        nx, ny = x + DX[dir], y + DY[dir]
        # if nx == X and ny == Y: # 이동하려는 위치에 숧래가 있으면 그냥 이동을 안함 #
        #     continue
        if in_range(nx, ny) == False:
            dir = (dir+2)%4 # 격자를 벗어나는 경우에는 반대 방향으로 바꿔서 이동 #
            nx, ny = x + DX[dir], y + DY[dir]
        if nx == X and ny == Y: # 역시나 위치에 술래가 있으면 이동할 수 없음 #
            runners[idx] = [x, y, dir] # 방향만 바뀐채로 업데이트 #
        else:
            runners[idx] = [nx, ny, dir]


def catcher_move(turn):
    global IS_CLOCK, X, Y, answer, runners
    # (1) 이동 방향에 맞춰서 1칸 이동 #
    move_dir_arr = catcher_clock if IS_CLOCK else catcher_anticlock
    move_dir = move_dir_arr[Y][X]
    nx, ny = X + DX[move_dir], Y + DY[move_dir]
    if nx == 0 and ny == 0 and IS_CLOCK == True:
        IS_CLOCK = False
    if nx == N//2 and ny == N//2 and IS_CLOCK == False:
        IS_CLOCK = True
    X, Y = nx, ny
    move_dir_arr = catcher_clock if IS_CLOCK else catcher_anticlock
    move_dir = move_dir_arr[Y][X]
    # print("Catcher", X, Y)
    # (2) 시야 안에 있는 도망자를 잡음 #
    sx, sy = X, Y
    caught = 0
    # print(f"Catcher MD : {move_dir}")
    import copy
    # print(f"RUNNERS : {runners}")
    for i in range(3): # 본인이 있는 위치부터 시작을 하기 때문에 (0, 1, 2) 움직임 모두에 대해서 확인을 해야 한다. #
        nx, ny = sx + DX[move_dir]*i, sy + DY[move_dir]*i
        # print(nx, ny)
        if in_range(nx, ny) == False:
            continue
        if tree[ny][nx] == 1: # 해당 위치에 나무가 있으면 도망자는 이동이 불가능 #
            continue
        new_runners = []
        for x, y, d in runners:
            if x == nx and y == ny:
                # print("Caught", x, y)
                caught += 1
                # new_runners.remove([x, y, _])
                # runners.remove([x, y, d])
            else:
                new_runners.append([x, y, d])
        runners = new_runners
    # runners = new_runners
    answer += caught * turn


answer = 0
setup_move()
# print(catcher_anticlock)
# print(catcher_clock)
for k in range(K):
    runner_move()
    # print(runners)
    catcher_move(turn=k+1)
    # print(answer)
    # print(X, Y)
print(answer)
