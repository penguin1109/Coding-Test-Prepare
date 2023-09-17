from collections import deque


N, M, K = map(int, input().strip().split(' '))

board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
rec = [[0] * M for _ in range(N)] ## 언제 각각의 포탑들이 각성을 하였는지를 기록

DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] ## 우-하-좌-상
DY8, DX8 = [0, 0, 0, -1, -1, -1, 1, 1, 1], [0, -1, 1, 0, -1, 1, 0, -1, 1]
# [-1, -1, -1, 1, 1, 1, 0, 0], [0, -1, 1, 0, -1, 1, -1, 1] 

turn = 0 ## 현재 몇번째 순서인지를 저장하는 변수

vis = [
    [0] * M for _ in range(N)
] ## 레이저 공격을 할 떄 방문한 포탑인지 아닌지 확인하기 위한 배
back_x = [
    [0] * M for _ in range(N)
]
back_y = [
    [0] * M for _ in range(N)
]

is_active = [
    [False] * M for _ in range(N)
]

class Tower:
    def __init__(self, x, y, r, p):
        self.x = x
        self.y = y
        self.r = r
        self.p = p

live_tower = [] ## 아직까지 부서지지 않고 남아있는 포탑들

def init():
    global turn
    
    turn += 1
    for y in range(N):
        for x in range(M):
            vis[y][x] = False
            is_active[y][x] = False
            
def move_point(x, y):
    nx, ny = x, y
    if x == M:
        nx = 0
    if x == -1:
        nx = M-1
    if y == N:
        ny = 0
    if y == -1:
        ny = N-1
    
    return nx, ny
   
def awake():
    global live_tower
    live_tower.sort(key=lambda x: (x.p, -x.r, -(x.x + x.y), -x.x))
    weak_tower = live_tower[0]
    x = weak_tower.x
    y = weak_tower.y
    
    board[y][x] += N+M
    rec[y][x] = turn ## 최근에 각성을 하였으니 현재 turn 정보를 저장해 준다.
    weak_tower.p = board[y][x]
    weak_tower.r = rec[y][x]
    is_active[y][x] = True
    
    live_tower[0] = weak_tower
    
def bomb_attack():
    weak_tower = live_tower[0]
    sx, sy = weak_tower.x, weak_tower.y
    power = weak_tower.p
    
    strong_tower = live_tower[-1]
    ex, ey = strong_tower.x, strong_tower.y
    
    for dx,dy in zip(DX8, DY8):
        nx, ny = ex + dx, ey + dy
        nx, ny = move_point(nx, ny)
        
        if nx == sx and ny == sy:
            continue
        
        if nx == ex and ny == ey:
            board[ny][nx] -= power
            # if board[ny][nx] < 0:
            #     board[ny][nx] = 0
            is_active[ny][nx] = True
        
        else:
            board[ny][nx] -= power // 2
            # if board[ny][nx] < 0:
            #     board[ny][nx] = 0
            is_active[ny][nx] = True
            
def attack():
    global live_tower
    weak_tower = live_tower[0]
    sx = weak_tower.x
    sy = weak_tower.y
    power = weak_tower.p
    
    strong_tower = live_tower[-1]
    ex = strong_tower.x
    ey = strong_tower.y
    
    vis[sy][sx] = True
    q = deque([[sx, sy]])
    
    attack_success = False
    
    while q:
        x, y = q.popleft()
        
        if x == ex and y == ey:
            attack_success = True
            break
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            nx, ny = move_point(nx, ny)
            
            if vis[ny][nx] == True:
                continue
            if board[ny][nx] <= 0:
                continue
                
            vis[ny][nx] = True
            
            back_x[ny][nx] = x
            back_y[ny][nx] = y
            q.append([nx, ny])
    
    if attack_success == False:
        bomb_attack()
    else:
        board[ey][ex] -= power
        # if board[ey][ex] < 0:
        #     board[ey][ex] = 0
        is_active[ey][ex] = True
        cx, cy = back_x[ey][ex], back_y[ey][ex]
        
        while not (cx == sx and cy == sy):
            board[cy][cx] -= power// 2
            # if board[cy][cx] < 0:
            #     board[cy][cx] = 0
            is_active[cy][cx] = True
            next_cx = back_x[cy][cx]
            next_cy = back_y[cy][cx]
            
            cx, cy = next_cx, next_cy
        
            
def reserve():
    for y in range(N):
        for x in range(M):
            if is_active[y][x]:
                continue
            if board[y][x] <= 0:
                continue
            board[y][x] += 1

for k in range(K):
    live_tower = []
    for y in range(N):
        for x in range(M):
            if board[y][x] > 0:
                new_tower = Tower(x, y, rec[y][x], board[y][x])
                live_tower.append(new_tower)
    if len(live_tower) <= 1:
        break
    init()
    awake()
    attack()
    
    reserve()

answer = max([max(a) for a in board])

print(answer)