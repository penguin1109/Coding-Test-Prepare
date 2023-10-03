""" 문제 설명
<조건>
1. NxN 크기의 격자
2. M명을 태우는 것이 목표
3. 택시가 빈칸에 있을 때, 상하좌우로 인접한 빈칸 중 하나로 이동할 수 있으며 무조건 이동할 때 최단 경로로만 이동.
4. 한 승객을 태워 목적지로 M명의 승객을 모두 반복하여 이동시켜야 하고, 출발지에서만 택시에 탑승이 가능함
5. 현재 위치에서 최단거리가 제일 짧 -> 행번호가 작고 -> 열번호가 작은 승객 선택
6. 승객을 목적지로 이동시키면 소모한 연료x2만큼 충전
7. 이동시키고 동시에 연료가 바닥나면 실패한게 아님. 즉, 도착지에서 연료=0이면 괜찮다는 뜻이다.

<출력>
모둔 손님을 이동시키고 연료를 충전했을 때 남은 연료의 양은?
단, 모든 손님을 이동시킬 수 없거나 이동 중에 연료가 받닥나서 이동이 불가능하면 -1을 출력

"""
import sys
import heapq
from collections import deque


input = sys.stdin.readline

N, M, gas = map(int, input().split(' ')) # 격자 크기, 승객의 숫자, 초기 연료의 양
board = []
for n in range(N):
    board.append(list(map(int, input().split(' '))))


car_y, car_x = map(int, input().split(' ')) # 운전을 시작하는 행과 열의 번호
car_y -= 1
car_x -= 1
def check_range(x, y):
    return (0 <= x < N) and (0 <= y < N)

def bfs(sx, sy, fx, fy, thresh=None):
    # 한번 계산한 최단 거리는 바뀌지 않는다.
    # sx, sy: startX, startY
    # dx, dy: destX, destY
    # 최단 거리 계산하는 함수
    DX, DY = [-1, 1, 0, 0], [0, 0, 1, -1]
    q =  [[0, sy, sx]]
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True
    if sx == fx and sy == fy:
        return 0
    min_dist = float("INF")
    while q:
        dist, y, x = heapq.heappop(q)
       #  print(x, y, fx, fy)
        """
        if thresh is not None:
            if dist > thresh:
                return -1
            elif (dist == thresh) and (x != fx or y != fy):
                return -1
        """
        if y == fy and x == fx:
            return dist
          #   min_dist = min(dist, min_dist)
           #  continue

        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if check_range(nx, ny) and (visited[ny][nx] == False):
                if board[ny][nx] == 0: # 빈칸인 경우
                    # q.append([dist+1, ny, nx])
                    heapq.heappush(q, [dist+1, ny, nx])
                    visited[ny][nx] = True
                #elif board[ny][nx] == 2 and nx == fx and ny == fy: # 도착지에 도달을 한 경우
                 #  return dist + 1
    if min_dist == float("INF"):
        return -1
    return min_dist # 이동을 할 수 없는 경우이다. (이런 경우가 있는지는 모르겠음)


people = []

for m in range(M):
    sy, sx, fy, fx = map(int, input().split(' '))
    # board[sy-1][sx-1] = 2 # 사람이 위치하고 있음
    people.append([sx-1, sy-1, fx-1, fy-1])

while True:
    distances = []
    for p in people:
        sx, sy, fx, fy = p
        board[sy][sx] = 0
        min_dist = bfs(car_x, car_y, sx, sy) # 자동차가 얼마나 이동해야 하는지 확인한다.

        if min_dist < gas and min_dist != -1:
            # print(min_dist, sx, sy)
            heapq.heappush(distances, (min_dist, sy, sx, fy, fx))
        # else:
          #   board[sy][sx] = 2
    move_success = False
    if len(distances) == 0:
        # 자동차가 이동할 수 이는 출발점이 없는 경우
        print(-1)
        # print(-1, "NOT ABLE TO MOVE")
        break

    else:

        dist, sy, sx, fy, fx = heapq.heappop(distances)

            # 출발지에서 도착지까지의 이동거리 계산
            # 시작지점은 다르지만 각 손님의 도착 지점은 같을 수 있다.
        board[sy][sx] = 0 # 임시로 변경
        ret = bfs(sx, sy, fx, fy, gas-dist)
        if gas-dist < ret: # 중간에 이동을 할 수 없게 연료가 떨어지는 경우
                # board[sy][sx]  = 2
            print(-1)
            break
        if ret != -1:
            move_success = True
            board[sy][sx] = 0 # 이동이 끝난 경우에는 빈칸으로 이동해 준다.
            car_x, car_y = fx, fy # 자동차의 위치 업데이트
            gas -= dist # 고객 출발지까지 도달하는데 사용한 연료 제거
            people.remove([sx, sy, fx, fy])
            gas += ret # 이동하였다는 가정하에 gas를 소모 후 충전시킴
                # print(f"DIST:{dist} RET:{ret}")

           #  else:
              #   board[sy][sx] = 2
    if not move_success:
        print(-1)
        break
    if len(people) == 0: # 모든 사람을 이동시킨 경우
        print(gas)
        break


