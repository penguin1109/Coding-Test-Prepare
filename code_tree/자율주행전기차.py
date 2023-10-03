class Customer:
    def __init__(self, sy, sx, fy, fx):
        self.sy=sy-1
        self.sx=sx-1
        self.fy=fy-1
        self.fx=fx-1
        

N, M, C = map(int, input().strip().split(' ')) # 격자의 크기, 승객 수, 초기 배터리 충전량
board = []
for n in range(N):
    arr = list(map(int, input().strip().split(' '))) # 0: 도로, 1: 벽
    board.append(arr)
cy, cx = map(int, input().strip().split(' ')) # 전기차의 초기 위치
cy-=1;cx-=1

customers = []
for m in range(M):
    sy, sx, fy, fx = map(int, input().strip().split(' ')) # 출발지 - 도착지
    new_cust = Customer(sy, sx, fy, fx)
    customers.append(new_cust)   

"""
- nxn 격자의 도로 위에 차가 지나갈 수 없는 벽의 위치와 m명의 승객의 위치가 주어질 때 
- 항상 최단 거리로 이동
- 0: 도로 1: 벽
- 한 칸 이동 => -1
- 승객을 태우는데 성공하면 태우고 이동하는데 소모한 2배+
(1) 현재 택시에서 승객까지의 거리가 짧은 승객
(2) Y 좌표가 작은 승객
(3) X 좌표가 작은 승객
[출력] 모든 손님을 이동 시키고 남은 연료의 양 (모든 손님을 이동할수 없으면 -1 출력)
"""
def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

def bfs(sx, sy, fx, fy):
    """
    (sx, sy): 출발지의 좌표
    (fx, fy): 도착지의 좌표
    """
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    from collections import deque
    cnt = [[-1 for _ in range(N)] for _ in range(N)]
    cnt[sy][sx] = 0
    q = deque([[sx, sy]])

    while q:
        x, y = q.popleft()
        if x == fx and y == fy:
            return cnt[y][x]
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) and cnt[ny][nx] == -1 and board[ny][nx] == 0:
                q.append([nx, ny])
                cnt[ny][nx] = cnt[y][x] + 1
    
    return -1 ## 현재 이동이 불가능한 승객 


import heapq
answer = -1

for m in range(M):
    q = []
    for i, c in enumerate(customers):
        dist = bfs(cx, cy, c.sx, c.sy)
        if dist != -1 and dist < C:
            heapq.heappush(q, [dist, c.sy, c.sx, i])
    # print(q)
    if len(q) == 0: # 현재 차가 더이상 이동할 수 없는 경우에 
        answer = -1
        break
    
    t2c, sy, sx, i = heapq.heappop(q)
    C -= t2c # 이동한만큼 연료를 빼줌
    customer = customers[i]
    del(customers[i]) # 승객 배열에서 i번째 승객을 빼줌

    cx, cy = customer.sx, customer.sy
    c2d = bfs(cx, cy,customer.fx, customer.fy)

    if c2d == -1:
        answer = -1
        break
    if c2d > C:
        answer = -1
        break
    
    C += c2d # 연료 충전 완료
    cx, cy = customer.fx, customer.fy
    answer = C


print(answer)

