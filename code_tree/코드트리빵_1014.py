import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline
# [출력] 사람들이 총 몇 분 후에 모두 편의점에 도착하는가 #

N, M = map(int, readl().strip().split(' ')) # 격자의 크기, 사람의 수 #
camps = [] # 이동 가능한 베이스 캠프의 위치 좌표를 저장하는 배열 #
board = [[[] for _ in range(N)] for _ in range(N)] # 한 칸에 2명 이상의 사람이 이동하면서 들어갈 수 있음 #
stores = [] # 각각의 사람들이 이동하고자 하는 편의점의 위치 좌표를 저장하는 배열 #
check = [] # 더이상 이동이 불가능한 위치에 대해서 업데이트 하기 위한 배열 #

for y in range(N):
    arr = list(map(int, readl().strip().split(' ')))
    check.append(arr)
    for x in range(N):
        if arr[x] == 1:
            camps.append([x, y])

for m in range(M):
    y, x = map(int, readl().strip().split(' ')) # 각 사람들이 원하는 편의점의 좌표 #
    y -= 1;x -= 1
    stores.append([x, y])

DX, DY = [0, -1, 1, 0], [-1, 0, 0, 1]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N
def bfs(sx, sy, ex, ey):
    """시작점인 (sx, sy)에서 도착점인 (dx, dy)로 도달하는데 필요한 최단 거리를 계산한다."""
    from collections import deque
    q = deque([[sx, sy, 0]])
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True

    while q:
        x, y, d = q.popleft()
        if x == ex and y == ey:
            return d
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) == False:
                continue
            if check[ny][nx] == -1:
                continue
            if visited[ny][nx] == True:
                continue
            q.append([nx, ny, d+1])
            visited[ny][nx] = True

    return -1

def move_people(time):
    global board, check
    import heapq
    # (1) 격자위의 사람들을 편의점으로 1칸 이동 시키기 #
    invalid = []

    new_board = [[[] for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            temp = board[y][x]
            if len(temp) == 0:
                continue
            for i in temp:
                q = []
                for dx, dy in zip(DX, DY):
                    nx, ny = x + dx, y + dy
                    if in_range(nx, ny) == False:
                        continue
                    if check[ny][nx] == -1:
                        continue
                    min_dist = bfs(nx, ny, stores[i][0], stores[i][1])
                    if min_dist != -1:
                        heapq.heappush(q, [min_dist, ny, nx])
                if q:
                    min_dist, min_y, min_x = heapq.heappop(q)
                    if min_dist == 0: # 편의점에 도달하였다는 뜻이다. #
                        invalid.append([min_x, min_y])
                    else:
                        new_board[min_y][min_x].append(i) # 편의점에는 도달하지 못했기 때문에 그냥 새로운 배열에 이동한 사람의 위치를 업데이트 해 줌 #
                else:
                    new_board[y][x].append(i) # 이동을 못하는 상황이면 그냥 그대로 넣어주면 된다. #

    # (2) 격자 위의 사람을 모두 이동 시켰으니 invalid 배열을 이동 불가능이라고 업데이트 한다. #
    for x, y in invalid:
        check[y][x] = -1

    # (3) 현재 시간과 동일한 사람이 자신이 가고 싶은 편의점과 제일 가까이 있는 캠프에 들어간다. #
    if time >= M:
        board = new_board
        return

    store_x, store_y = stores[time] # 현재 시간과 같은 번호의 사람이 가고 싶어하는 편의점의 좌표 #
    q = []
    for x, y in camps:
        if check[y][x] == -1: # 이미 방문한 베이스 캠프면 안됨 #
            continue
        min_dist = bfs(x, y, store_x, store_y)
        print(store_x, store_y, '->', x, y, 'dist: ', min_dist)
        if min_dist != -1:
            heapq.heappush(q, [min_dist, y, x])
    if q:
        min_dist, camp_y, camp_x = heapq.heappop(q)
        new_board[camp_y][camp_x].append(time) # 현재 이동한 사람의 번호를 넣어준다. #
        check[camp_y][camp_x] = -1 # 이동이 불가능한 위치임. 이미 누군가 이 캠프에 도달했기 때문이다. #

    # (4) 바뀐 새 board 배열을 업데이트 해 준다. #
    board = new_board

def do_finish():
    for x, y in stores:
        if check[y][x] != -1:
            return False
    return True


time = 0
while True:
    move_people(time)
    # print(board)
    time += 1
    # break
    ret = do_finish()
    if ret:
        break
print(time)


