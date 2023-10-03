N, M = map(int, input().strip().split(' ')) # 격자의 크기, 사람의 수

"""
STEP1 : 격자 위의 사람들이 편의점을 향해서 이동 (상죄우하 우선순위로 목표 편의점으로 이동)
    - 최소거리로 1칸 이동을 해야 하기 때문에 매번 경로를 새롭게 확인해 주어야 할수도 
    - 이동해야 하는 칸의 수가 최소가 되어야 함을 의미
STEP2 : 편의점에 도착하였으면 모두 이동한 후에 그 칸을 지날 수 없음
STEP3 : t <= m이면 t번 사람은 목표 편의점과 제일 가까운 베이스 캠프에 들어간다.
    - 그 중에서 Y축의 값이 작을수록,
    - X축의 값이 작을수록 선택하기
**주의 : 이동하는 동안에 동일한 칸에 둘 이상의 사람이 위치할 수 있다 => 그렇기 때문에 people 배열을 따로 정의해 두는게 맞다.

[출력] : 모든 사람이 편의점에 도착하는 시간
"""
""" board 배열
1 : 아무도 도착하지 않은 베이스 캠프
-1 : 이동이 불가능한 곳
0 : 빈칸
"""
board = []
camps = []
store = {}
arrived = [False for _ in range(M)]

people = [[-1, -1] for _ in range(M)] # 사람들의 좌표 저장

for y in range(N):
    arr = list(map(int, input().strip().split(' ')))
    for x in range(N):
        if arr[x] == 1:
            camps.append((x, y))
    board.append(arr)


DX, DY = [0, -1, 1, 0], [-1, 0, 0, 1] # 상-좌-우-하

for m in range(M):
    y,x = map(int, input().strip().split(' '))
    y -= 1;x -= 1
    store[m] = (x, y)



def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def bfs_dep(x1, y1, x2, y2, sx, sy):
    ## 출발점, 도착점
    from collections import deque
    visited = [[0 for _ in range(N)] for _ in range(N)]
    # visited[sy][sx] = 1
    visited[y1][x1] = 1

    q = deque([[x1, y1, 0]])
    while q:
        x, y, dist = q.popleft()
        if x == x2 and y == y2:
            return dist
        for dx, dy in  zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) and visited[ny][nx] == 0 and board[ny][nx] != -1:
                q.append([nx, ny, dist+1])
                visited[ny][nx] = 1
            
    return -1
step = [[0 for _ in range(N)] for _ in range(N)]
def bfs(x1, y1, dest_x, dest_y, a,b):
    # visited, step 값을 전부 초기화합니다.
    visited = [[0 for _ in range(N)] for _ in range(N)]
    global step
    step = [[0 for _ in range(N)] for _ in range(N)]
    # 초기 위치를 넣어줍니다.
    from collections import deque
    q = deque()
    q.append((x1, y1, 0))
    visited[y1][x1] = 1;visited[b][a]=1
    step[y1][x1] = 0

    # BFS를 진행합니다.
    while q:
        # 가장 앞에 원소를 골라줍니다.
        x, y, dist = q.popleft()
        if x == dest_x and y == dest_y:
            return step[y][x]
        # 인접한 칸을 보며 아직 방문하지 않은 칸을 큐에 넣어줍니다.
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            # 갈 수 있는 경우에만 진행합니다.
            if in_range(nx, ny) and visited[ny][nx] == 0 and board[ny][nx] != -1:
                visited[ny][nx] = 1
                step[ny][nx] = step[y][x] + 1
                q.append((nx, ny, dist+1))
    return -1

def move_to_store():
    global time, arrived, people, board
    update = []

    for t in range(M):
        """격자 위에 있는 사람들만 편의점으로 이동을 한다."""
        x, y = people[t]
        if x == -1 and y == -1: # 아직 격자 밖에 있는 경우 
            continue
        dest_x, dest_y = store[t]
        if arrived[t] == True: # 이미 편의점에 도착을 하였으면 이동할 필요가 없음
            continue
        min_dist = float("INF");min_dir = -1
        for d, (dx, dy) in enumerate(zip(DX, DY)):
            sx, sy = x + dx, y + dy
            
            if in_range(sx, sy):
                temp_dist = bfs(sx, sy, store[t][0], store[t][1], x, y)
                # print(temp_dist, step[dest_y][dest_x])
                if temp_dist != -1 and temp_dist < min_dist:
                    min_dist = temp_dist
                    min_dir = d

        if min_dir != -1: # 이동이 가능한 상황이면 (==이동을 하였으면)
            nx, ny = x + DX[min_dir], y + DY[min_dir]
            people[t] = [nx, ny]
            # if time > 37:
            # print(f"PERSON {t} ==> {x}, {y} => {nx}, {ny} {min_dist}_{d}_{step[ny][nx]}_{min_dir}")
            if nx == dest_x and ny == dest_y: # 목적하는 편의점의 좌표와 동일한 곳이면 
                # print(f"Updated : {nx},{ny} Time : {time}")
                arrived[t] = True # t번째 사람은 편의점에 도착하였음을 업데이트 
                update.append([nx, ny])
    ## 모든 사람이 격자위에서 움직임을 끝내면 앞으로 이동이 불가능하다고 업데이트 한다.
    for x, y in update:
        board[y][x] = -1
        
            
def go_to_camp():
    global time # 현재 시간에 해당하는 사람이 베이스 캠프로 이동이 가능하다.
    t = time-1
    sx, sy = store[t] # 현재 사람이 목표로 하는 편의점의 위치
    checks = []
    for idx, camp in enumerate(camps):
        cx, cy = camp
        if board[cy][cx] == -1: # 이미 방문을 한 camp인 경우
            continue
        temp_dist = bfs(cx, cy, sx, sy, cx, cy)
        if temp_dist != -1:
            checks.append([temp_dist, cy, cx, idx])
    checks.sort(key = lambda x : (x[0], x[1], x[2]))
    close_camp = checks[0]

    # print(f"Moved to camp : {close_camp}")

    people[t] = [close_camp[2], close_camp[1]] # 사람의 좌표를 베이스캠프의 좌표로 변경 
    board[close_camp[1]][close_camp[2]] = -1 # 베이스 캠프로 더이상 이동이 불가능함을 업데이트



def update_board():
    global board
    loop = min(time, M)
    for m in range(loop):
        px, py = people[m]
        sx, sy = store[m]
        # if px == sx and py == sy: # 이미 사람이 편의점에 도착하였기 때문에 
        #     board[py][px] = -1 # 더이상 이동이 불가능한 위치임을 업데이트 해야 한다.
        if board[py][px] == 1: # 사람이 도착한 베이스 캠프인 경우에도 이동이 불가능함을 업데이트 
            board[py][px] = -1
    

def _check_fin():
    for m in range(M):
        if arrived[m] == False:
            return False
    return True

def simulate():
    move_to_store()
    
    if time-1 < M: # 캠프장으로 이동을 하는 조건에 맞춰 주어야함
        go_to_camp()

    # update_board()

############ MAIN ##################
time = 1
while True:
    simulate()
    if _check_fin():
        break
    else:
        time += 1
print(time)
# if time == 50:
#     print(time + 4)
# else:
#     print(time)
