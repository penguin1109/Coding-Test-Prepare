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

for m in range(M):
    new_rider = Rider(*list(map(int, input().strip().split(' '))))
    riders.append(new_rider)

def _in_range(x, y):
    return (0 <= x < N) and (0 <= y < N)

def bfs(sx, sy, fx, fy):
    """
    (sx, sy): 출발하는 위치의 좌표
    (fx, fy): 도착하는 위치의 좌표
    """
    global DX, DY, board
    visited = [[False for _ in range(N)] for _ in range(N)]
    # track_x = [[0 for _ in range(N)] for _ in range(N)]
    # track_y = [[0 for _ in range(N)] for _ in range(N)]
    
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
                    # track_x[ny][nx] = x
                    # track_y[ny][nx] = y
                    q.append([nx, ny, d+1])
    return -1

answer = -1
driving_success = True
while riders:
    q = []
    left_riders = []
    ## 모든 손님마다 BFS를 계산해 주는 것이 맞지 않을 수 있겠다. ##
    for idx, rider in enumerate(riders):
        dist = bfs(cx, cy, rider.sx, rider.sy) # 택시와 승객 사이의 최단 거리 계산
        if dist != -1 and dist < F:
            heapq.heappush(q, [dist, rider.sx, rider.sy, idx])    
        else:
            left_riders.append(rider)

    next_info = heapq.heappop(q)
    t2s_dist = next_info[0]
    next_rider = riders[next_info[-1]]
    s2d_dist = bfs(next_rider.sx, next_rider.sy, next_rider.fx, next_rider.fy)
    if s2d_dist + t2s_dist < F: # 이동이 가능할 만큼 연료가 남아 있다면
        # print(f"승객으로 : {t2s_dist} 도착지로 : {s2d_dist}")
        F -= t2s_dist
        F += s2d_dist
        cx = next_rider.fx
        cy = next_rider.fy
        
    else:
        driving_success=False
        break
            # left_riders.append(next_rider)
    
    while q:
        next_rider = riders[heapq.heappop(q)[-1]]
        left_riders.append(next_rider)
    riders = left_riders
    
    # if len(riders) == len(left_riders):
    #     driving_success = False
    #     break
    # else:
    #     riders = left_riders

if driving_success:
    answer = F
print(answer)


    
    
            
        
    
    
        

    
            