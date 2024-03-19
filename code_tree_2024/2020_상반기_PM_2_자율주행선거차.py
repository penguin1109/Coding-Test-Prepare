import sys
import heapq # 근데 heapq를 사용하는 것보다 sorted를 사용하는 것이 더 빠른 경우도 있다. #
input = sys.stdin.readline
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
N, M, C = map(int, input().strip().split(' ')) # 격자의 크기, 승객의 수, 초기 배터리 충전량 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 0 : 도로 1 : 벽 #
y, x = map(int, input().strip().split(' '))
CAR = [x-1, y-1]
GONE = [-1, -1, -1, -1]
RIDER = []
INF = 10 ** 7
total_left = M

for _ in range(M):
    sy, sx, ey, ex = map(int, input().strip().split(' ')) # 승객의 시작 위치, 도착 위치 #
    sx -= 1;sy -= 1;ex -= 1;ey -= 1;
    RIDER.append([sx, sy, ex, ey])


def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def simulate_move(idx, min_dist):
    sx, sy, ex, ey = RIDER[idx]
    global C
    to_end_dist = single_rider_dist(sx, sy, ex, ey, C-min_dist)
    
    if to_end_dist + min_dist <= C:
        C -= (to_end_dist + min_dist)
        C += (to_end_dist * 2)
        return True
    return False
    
def single_rider_dist(sx, sy, ex, ey, charge):
    q = [[0, sx, sy]]
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True
    
    while q:
        dist, x, y = heapq.heappop(q)
        if dist > charge:
            return INF
        if x == ex and y == ey:
            return dist
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) and board[ny][nx] == 0 and visited[ny][nx] == False:
                visited[ny][nx] = True
                heapq.heappush(q, [dist+1, nx, ny])
    return INF

def all_place_dist(sx, sy):
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True
    step = [[0 for _ in range(N)] for _ in range(N)]
    from collections import deque
    q = deque()
    q.append([sx, sy])
    while q:
        x, y = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) and board[ny][nx] == 0 and visited[ny][nx] == False:
                visited[ny][nx] = True
                q.append([nx, ny])
                step[ny][nx] = step[y][x] + 1
    return step, visited

def calculate_all_riders():
    global RIDER, CAR, total_left
    q = []
    bfs_step, bfs_visited = all_place_dist(*CAR)
    
    for ri, rider in enumerate(RIDER):
        # dist = single_rider_dist(*rider[:2], *CAR, C)
        dist = bfs_step[rider[1]][rider[0]]
        # if dist == INF:
        if bfs_visited[rider[1]][rider[0]] == False:
            continue
        if C >= dist: # 현재 연료로 감당 가능한 거리인 경우 #
            heapq.heappush(q, [dist, rider[1], rider[0], ri]) # [dist, y, x] #
    if q: # 이동 가능한 승객이 있으면 #
        min_dist, next_y, next_x, next_idx = heapq.heappop(q)
        # 이동 시뮬레이션 #
        can_move = simulate_move(next_idx, min_dist)
        if can_move == True:
            CAR = [RIDER[next_idx][2], RIDER[next_idx][3]]
            RIDER.remove(RIDER[next_idx])
            total_left -= 1
            return True
        else:
            return False
    else: # 이동 가능한 승객이 없으면 #
        return False
        

while True:
    can_continue = calculate_all_riders()
    if can_continue == False:
        print(-1)
        exit(0)
    if total_left == 0:
        break

print(C)
        
        
