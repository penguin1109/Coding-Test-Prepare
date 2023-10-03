""" 16236 - 아기 상어
<문제 조건>
- NxN 크기의 공간에 물고기 M마리과 아기 상어 1마리가 존재. 1칸에 최대 1마리 존재.
- 0: 빈칸 1,2,3,4,5,6: 칸의 물고기 크기 9: 아기상어의 위치
- 아기 상어는 1마리만 존재한다.
- 아기 상어보다 작은 물고기만 먹을 수 있다.
- 아기 상어보다 큰 물고기가 있는 칸은 지날 수 없다.

<상어 이동 방법>
1. 먹을 수 있는 물고기가 공간에 없으면 엄마에 도움 요청
2. 먹을 수 있는 물고기가 1마리면 그 물고기를 먹으러 감
3. 먹을 수 있는 물고기가 1마리보다 많으면 거리가 가장 가까운 물고기를 먹으러 감.
    - 거리 = 아기 상어가 있는 칸에서 물고기 칸으로 이동할 수 있는 최단 거리
    - 거리가 가까운 물고기가 많으면 가장 위의 물고기(y좌표가 작은) - 가장 왼쪽의 물고기(x좌표가 작은)
4. 아기 상어는 자신의 크기와 같은 개수의 물고기를 먹어야 크기가 1이 증가한다.

<출력>
- 아기 상어가 몇 초동안 엄마 상어에게 도움을 요청하지 않고 물고기를 잡아먹을 수 있는지?

"""

N = int(input())
fish = []
baby_x, baby_y = 0, 0
baby_size = 2 # 처음 아기 상어의 크기
eat_count = 0
for n in range(N):
    arr = list(map(int, input().split(' ')))
    fish.append(arr)
    for i in range(N):
        if arr[i] == 9:
            baby_x = i
            baby_y = n
            fish[n][i] = 0

DX, DY = [0, -1, 1, 0], [-1, 0, 0, 1]

import heapq # 우선순위 큐를 사용해서 가장 가까운 - 가장 위 - 가장 왼쪽에 있는 물고기를 찾도록 해야 한다.
def eat_fish(fy, fx, dist):
    """아기 상어가 물고기를 먹고 이후의 변화한 값들을 갱신하기 위한 함수"""
    global baby_size, baby_y, baby_x, eat_count, time
    eat_count += 1
    if eat_count == baby_size:
        baby_size += 1
        eat_count = 0
    fish[fy][fx] = 0 # 원래 물고기 있던 자리는 빈칸으로 처리
    baby_y = fy
    baby_x = fx
    time += dist

def shortest_distance():
    """아기 상어가 있는 칸에서 물고기가 있는 칸으로 이동 할 때 지나야 하는 칸의 개수의 최솟값을 BFS를 사용하여 계산한다."""
    q = [(0, baby_y, baby_x)]
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[baby_y][baby_x] = True # 아기 상어는 방문을 하였음.
    ## 최단 경로 문제이기 때문에 당연히 너비 우선 탐색을 사용했어야 했다.
    min_dist = N**2
    min_x = N+1
    min_y = N+1
    while q:
        dist, y, x = heapq.heappop(q)
        visited[y][x] = True
        if dist >= min_dist:
            break

        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if (0 <= nx < N and 0 <= ny < N) and visited[ny][nx] == False:

                if (fish[ny][nx] == 0): # 빈칸으로는 당연히 이동 가능
                    heapq.heappush(q, (dist+1, ny, nx))
                    visited[ny][nx] = True
                elif (fish[ny][nx] == baby_size): # 해당 경로로 이동은 가능한 경우 (크기가 같은 물고기이기 때문)
                    heapq.heappush(q, (dist+1, ny, nx))
                    visited[ny][nx] = True
                elif (fish[ny][nx] < baby_size): # 드디어 먹을 수 있는 물고기가 생긴 경우
                    if (min_dist > dist+1):
                        min_dist = dist + 1 # 거리 업데이트
                    if dist+1 == min_dist:
                        if min_y > ny:
                            min_y = ny
                            min_x = nx
                        elif min_y == ny:
                            if min_x > nx:
                                min_y = ny
                                min_x = nx

                    # heapq.heappush(q, (dist+1, ny, nx))
                    # eat_fish(ny, nx, dist+1)
                    # return True
                else: # 해당 경로로 이동도 불가능한 경우 (더 큰 크기의 물고기이기 때문)
                    continue
    if min_dist == N ** 2: ## 최단 거리가 N**2이다.
        return False
    else:
        eat_fish(min_y, min_x, min_dist)
        return True

time = 0

while True:
    eaten = shortest_distance()
    if not eaten:
        break
print(time)




