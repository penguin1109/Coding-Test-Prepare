""" 코드 트리 빵
- 빵을 구하고자 하는 m명의 사람. nxn 크기의 격자
<빵을 구하고자 하는 사람의 움직임>
=> 1분동안 3가지 행동이 진행되며, 1,2,3의 순서로 진행이 되어야 한다.
1. 격자에 있는 사람들이 본인이 가고 싶은 편의점으로 1칸 움직임. (이때 최단 거리로 이동)
2. 편의점에 도착하면 해당 편의점에서 멈추고, 이때부터 다른 사람들은 그 편의점이 있는 칸을 지날 수 없다.
3. 현재 시간이 t분이고 t<=m을 만족한다면 t번 사람은 자신이 가고 싶은 편의점과 가장 가까운 베이스 캠프에 간다.
    3-1. 가까운 베이스캠프가 여러개라면 행 -> 열이 작은 베이스 캠프로 이동

=> 모든 사람이 편의점에 도착하는 시간을 출력하여라.
=> 한번 누군가가 도착한적이 있는 베이스 캠프는 더이상 아무도 도달 할 수 없다.
=> 이동하는 도중 동일한 칸에 둘 이상의 사람이 존재하게 될 수 있다.
"""
import heapq
from collections import deque
def calc_dists(X, Y):
    distance = []

    for idx, camp in enumerate(camps):
        x, y, valid = camp
        if valid == 0: # 이미 차지된, 혹은 된 적이 있는 베이스 캠프이다.
            continue

        dist = abs(x-X) + abs(y-Y)
        heapq.heappush(distance, [dist, x, y, idx])

    return distance

def calc_dist(ax, ay, bx, by):
    return abs(ax-bx) + abs(bx-by)


N, M = map(int, input().split(' ')) # 격자의 크기, 사람의 수
board = [[0 for _ in range(N)] for _ in range(N)] # 해당 칸을 다른 사람이 지나갈수 있는지 없는지 판단하기 위한 배열

camps = []
for n in range(N):
    arr = list(map(int, input().split(' '))) # 0은 빈 공간, 1은 베이스 캠프
    for i in range(N):
        if arr[i] == 1:
            camps.append([n, i, 1]) # 베이스 캠프의 x,y 좌표를 저장한다.
            """ board에 베이스 캠프의 위치 또한 저장을 해 주었어야 했다.
            나중에 STEP 3에서 보면 아직 내부에 있지 않아서 내부의 이동할 베이스 캠프를 정해야 하기 때문이다.
            물론 한번 사람이 도착하게 되면 그 이후에는 더이상 아무도 방문이 불가능하다.
            """
            board[n][i] = 1


people = []
dist_to_camp = []
for m in range(M):
    x, y = map(int, input().split(' '))
    # distance = calc_dists(x, y) # m번호의 사람이 가고 싶어하는 편의점의 위치와 베이스 캠프 사이의 거리.
    # closest = heapq.heappop(distance)

    people.append([x-1, y-1, -1, -1]) # 각 번호의 사람들이 가고 싶어하는 편의점의 위치


DX, DY = [-1, 0, 0, 1], [0, -1, 1, 0]

def check_range(x, y):
    if (0 <= x < N and 0 <= y < N):
        return True
    return False

def shortest_path_store(x, y, sx, sy):
    # [사람의 위치], [가고 싶은 편의점의 위치]
    dist = abs(x-sx) + abs(y-sy)
    if (x > sx): # 위로 올라가기
        nx = x + DX[0]; ny = y + DY[0];
        if (check_range(nx, ny) == True and board[nx][ny] == 0):
            return nx, ny
    if (y > sy): # 왼쪽으로 이동하기
        nx = x + DX[1]; ny = y + DY[1];
        if (check_range(nx, ny) == True and board[nx][ny] == 0):
            return nx, ny

    if (x < sx): # 아래로 이동하기
        nx = x + DX[2]; ny = y + DY[2]
        if (check_range(nx, ny) == True and board[nx][ny] == 0):
            return nx, ny

    if (y < sy): # 오른쪽으로 이동하기
        nx = x + DX[3]; ny = y + DY[3]
        if (check_range(nx, ny) == True and board[nx][ny] == 0):
            return nx, ny

    for i in range(4):
        nx, ny = x + DX[i], y + DY[i]
        if (check_range(nx, ny) == True and board[nx][ny] == 0):
            return nx, ny





def shortest_path_camp(sx, sy):
    # [가고 싶은 편의점의 위치]
    distance = calc_dists(sx, sy)
    closest = heapq.heappop(distance)
    idx = closest[-1]
    camps[idx][-1] = 0 # 이제 도착할 수 없는 베이스 캠프임을 나타냄.
    cx, cy = closest[1], closest[2]
    board[closest[1]][closest[2]] = -1 # 도달 할 수 없는 칸이라는 것을 board에도 나타냄.
    return cx, cy
step = [
    [0] * N for _ in range(N)
]

visited = [
    [False] * N for _ in range(N)
]

def bfs(sx, sy):
    # step, visited 배열을 초기화 한다.
    for i in range(N):
        for j in range(N):
            visited[i][j] = False
            step[i][j] = 0

    q = deque()
    q.append((sx, sy))
    fx, fy = sx, sy
    visited[fx][fy] = True
    step[fx][fy] = 0

    # 시작 좌표인 sx, sy로부터 모든 다른 좌표까지의 최단 거리를 계산한다. (상-하-좌-우 의 방향으로만 이동한다.)
    while q:
        x, y = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            # 범위 내에 있으며, 방문한적이 없고, 지나갈수 없는 위치가 아니어야 한다.
            if check_range(nx, ny) and visited[nx][ny] == False and board[nx][ny] != -1:
                visited[nx][ny] = True
                step[nx][ny] = step[x][y] + 1
                q.append((nx, ny))


def run():
    global count, done, time
    # STEP 1: 격자에 있는 사람들만 편의점을 향해 최단 거리로 1칸 이동한다.
    for m in range(M):
        if done[m] == True or people[m][2] == -1:
            continue

        # 현재 위치에서 편의점 위치까지 최단 거리를 구해야 하는데,
        # 최단 거리가 되기 위한 다음 위치를 구하기 위해서는 거꾸로 편의점 위치부터 현재 위치까지의 최단 거리를 구해야 한다.
        # 따라서 편의점을 시작으로 BFS를 진행한다.
        bfs(sx = people[m][0], sy = people[m][1])
        px, py = people[m][2], people[m][3]
        min_dist = 1e+7
        min_x, min_y = -1, -1
        # 현재 지점에서 상하 좌우로 이동할 수 있는 4 위치 좌표중에서 제일 편의점으로부터의 <최단거리>를 만족하는 곳에 이동을 한다.
        # 매 순간 달라지기 때문에 계속해서 dfs로 <편의점으로부터 다른 모든 좌표까지의> 최단 거리를 계산해 주어야 한다.
        for dx, dy in zip(DX, DY):
            nx, ny = px + dx, py + dy
            if check_range(nx, ny) and visited[nx][ny] and min_dist > step[nx][ny]:
                min_dist = step[nx][ny]
                min_x, min_y = nx, ny
        people[m][2], people[m][3] = min_x, min_y
        cx, cy = people[m][0], people[m][1]
        if min_x == cx and min_y == cy:
            board[cx][cy] = -1
            done[m] = True
            count += 1

    if time > M:
        return
    # STEP 3: 편의점에서 가장 가까운 베이스 캠프를 고르기 위해서 편의점을 시작으로 BFS를 계산
    # 아직 좌표 밖에 있는 사람은 m분에 시작 가능하고, 이러면 STEP1, STEP2는 수행 못하므로 STEP3을 수행한다.
    bfs(sx = people[time-1][0], sy = people[time-1][1]) # time <= m이면 t번 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프에 들어간다.
    min_dist = 1e+7
    min_x, min_y = -1, -1
    for i in range(N):
        for j in range(N):
            # 방문이 가능한 베이스 캠프인 경우
            if visited[i][j] and min_dist > step[i][j] and board[i][j] == 1:# != -1:
                min_dist = step[i][j]
                min_x = i;min_y = j;
    people[time-1][2] = min_x
    people[time-1][3] = min_y
    board[min_x][min_y] = -1 # 더이상 이동이 불가능한 베이스 캠프이다.

count = 0
time = 0
done = [False for _ in range(M)]
while True:
    time += 1
    run()
    if count == M:
        break


print(time)

















