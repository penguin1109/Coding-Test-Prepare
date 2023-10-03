import sys
from collections import deque

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' '))
"""
0 : 빈 칸
-1 : 이동이 불가능한 위치
1 : 베이스 캠프 존재
"""

board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

stores = []
for _ in range(M):
    y, x = map(int, readl().strip().split(' '))
    y -= 1;x -= 1;
    stores.append([x, y])

people = [[-1, -1] for _ in range(M)] # 초기의 사람들의 위치 좌표는 (-1, -1)로 둔다.
DX, DY = [0, -1, 1, 0], [-1, 0, 0, 1]

step = [[0 for _ in range(N)] for _ in range(N)]

visited = [[False for _ in range(N)] for _ in range(N)]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def _init():
    global step, visited
    step = [[0 for _ in range(N)] for _ in range(N)]
    visited = [[False for _ in range(N)] for _ in range(N)]
    
    return step, visited
    
def bfs(sx, sy):
    step, visited = _init()
    from collections import deque
    q = deque([[sx, sy]])
    visited[sy][sx] = True
    
    while q:
        x, y = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) and visited[ny][nx] == False and board[ny][nx] != -1:
                q.append([nx, ny])
                visited[ny][nx] = True
                step[ny][nx] = step[y][x] + 1

def simulate():
    global board, time, people
    for i in range(M):
        if people[i] == [-1, -1] or people[i] == stores[i]:
            continue
        bfs(stores[i][0], stores[i][1]) ## i번째 편의점을 시작으로 다른 모든 위치까지의 최단 이동거리를 계산하여 step에 저장
        px, py = people[i]
        min_dist = float("INF");min_x= -1;min_y = -1
        for dx, dy in zip(DX, DY):
            nx, ny = px + dx, py + dy
            if in_range(nx, ny) and visited[ny][nx] == True and min_dist > step[ny][nx]:
                min_dist = step[ny][nx]
                min_x, min_y = nx, ny
        people[i] = [min_x, min_y]
        
    for i in range(M):
        if people[i] == stores[i]:
            board[people[i][1]][people[i][0]] = -1
    
    if time > M:
        return

    bfs(stores[time-1][0], stores[time-1][1])
    min_dist = float("INF")
    min_x, min_y = -1, -1
    for i in range(N):
        for j in range(N):
            if visited[i][j] == True and board[i][j] == 1 and min_dist > step[i][j]:
                min_dist = step[i][j]
                min_x, min_y = j, i
        
    people[time-1] = [min_x, min_y]
    board[min_y][min_x] = -1 # 다른 사람이 베이스 캠프에 도착하였기 때문에 이동이 불가능한 칸이 되었음

def is_finish():
    for i in range(M):
        if people[i] != stores[i]:
            return False
    return True
time = 1
while True:
    simulate();
    if is_finish():
        break
    time += 1

print(time)
        
            
        
        
    
        
          