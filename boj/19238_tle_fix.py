""" 19238 : 스타트 택시
- 손님을 도착지에 데려다 줄때마다 연료 충전. 연료 바닥나면 그 날의 업무 끝
- 이동할 때 항상 최단 경로로만 이동 가능
- 한 승객을 태워 이동시키는 일을 M번 반복해야 함.
0 : 빈칸 1 : 벽
- 출발지에서만 탈 수 있고, 목적지에서만 내릴 수 있다.
- 짧은 거리 -> 작은 행 번호 -> 작은 열 번호
- 한 칸 이동할 때마다 연료가 1만큼 소모됨
- 이동 중에 연료가 바닥나면 이동 실패 / 목적지로 이동 시킴과 동시에 연료가 바닥나면 이동 성공 

- 이동 거리만큼 -1
- 승객을 성공적으로 이동시키면 태워서 이동하면서 소모한 연료의 *2만큼 충전

[출력]: 모든 손님을 성공적으로 이동 시킬 수 있는지, 그리고 가능하다면 남은 연료의 양을 출력하고 불가능하면 -1을 출력하여라.
"""
"""반례 상황들
1. 택시의 시작 지점에 바로 손님이 있는 경우

"""

from collections import deque
import heapq

class Rider:
    def __init__(self, sy,sx,fy,fx):
        self.sx = sx-1
        self.sy = sy-1
        self.fx = fx-1
        self.fy = fy-1
        
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
N, M, F = map(int, input().strip().split(' ')) # 세로, 가로, 초기 연료의 양
board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 활동할 영역의 지도

cy, cx = map(int, input().strip().split(' ')) # 운전 시작 행, 열
cx -= 1;cy -= 1

riders = []
passenger_start = []

for m in range(M):
    new_rider = Rider(*list(map(int, input().strip().split(' '))))
    riders.append(new_rider)
    passenger_start.append([new_rider.sx, new_rider.sy])

def _in_range(x, y):
    return (0 <= x < N) and (0 <= y < N)

def find_passenger(sx, sy):
    global passenger_start
    
    q = deque()
    q.append([sx, sy])
    visited = [[0 for _ in range(N)] for _ in range(N)]
    min_dist = float("INF")
    hubo = []
    
    while q:
        x, y = q.popleft()
        if visited[y][x] > min_dist:
            break
        if [x, y] in passenger_start:
            print("IN PASSENGER")
            min_dist = visited[y][x]
            heapq.heappush(hubo, [min_dist, y, x]) ## 최소 이동거리, 최소 행(가로), 최소 열(세로)
        else:
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if _in_range(nx, ny) and board[ny][nx] == 0 and visited[ny][nx] == 0:
                    visited[ny][nx] = visited[y][x] + 1
                    q.append([nx, ny])
    if hubo:
        return heapq.heappop(hubo)
    else:
        return -1, -1, -1
    
def bfs(sx, sy, fx, fy):
    """
    (sx, sy): 출발하는 위치의 좌표
    (fx, fy): 도착하는 위치의 좌표
    """
    global DX, DY, board
    visited = [[False for _ in range(N)] for _ in range(N)]
    
    q = deque([[sx, sy, 0]])
    visited[sy][sx] = True
    
    while q:
        x, y, d = q.popleft()
        if x == fx and y == fy:
            return d ## 최단 경로 return
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if _in_range(nx, ny):
                if visited[ny][nx] == False and board[ny][nx] == 0:
                    visited[ny][nx] = True
                    q.append([nx, ny, d+1])
    return -1

answer = -1
driving_success = True
for _ in range(M):
    # ## 모든 손님마다 BFS를 계산해 주는 것이 맞지 않을 수 있겠다. ##
    # for idx, rider in enumerate(riders):
    #     dist = bfs(cx, cy, rider.sx, rider.sy) # 택시와 승객 사이의 최단 거리 계산
    #     if dist != -1 and dist < F:
    #         heapq.heappush(q, [dist, rider.sx, rider.sy, idx])    
    #     else:
    #         left_riders.append(rider)

    # next_info = heapq.heappop(q)
    # t2s_dist = next_info[0]
    # next_rider = riders[next_info[-1]]
    t2s_dist, next_y, next_x = find_passenger(cx, cy)
    # print(f"승객한테 : {t2s_dist}")
    if t2s_dist == -1 or t2s_dist > F:
        driving_success=False
        break
    
    next_rider_idx = passenger_start.index([next_x, next_y])
    next_rider = riders[next_rider_idx]
    del passenger_start[next_rider_idx]
    del riders[next_rider_idx]
    
    F -= t2s_dist
    s2d_dist = bfs(next_rider.sx, next_rider.sy, next_rider.fx, next_rider.fy)
   
    if s2d_dist != -1 and s2d_dist <= F: # 이동이 가능할 만큼 연료가 남아 있다면
        # print(f"승객으로 : {t2s_dist} 도착지로 : {s2d_dist}")
        F += s2d_dist
        
        # board[cy][cx] = 0
        # board[next_rider.sy][next_rider.sx] = 0
        
        ## 택시의 위치를 이전 승객의 도착지로 갱신 ## 
        cx = next_rider.fx
        cy = next_rider.fy
        
    else:
        driving_success=False
        break
            # left_riders.append(next_rider)
    
    # while q:
    #     next_rider = riders[heapq.heappop(q)[-1]]
    #     left_riders.append(next_rider)
    # riders = left_riders
    
    # if len(riders) == len(left_riders):
    #     driving_success = False
    #     break
    # else:
    #     riders = left_riders

if driving_success:
    answer = F
    
print(answer)


    
    
            
        
    
    
        

    
            