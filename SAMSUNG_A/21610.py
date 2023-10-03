""" 21610 - 마법사 상어와 비바라기
<문제 설명>
1. 구름이 이동한 후 해당 칸의 물 += 1
2. 구름이 모두 사라짐
3. 물이 증가한 칸, 즉 구름이 있던 칸에서 대각선 방향으로 거리가 1인 칸에 **물이 있는 바구니의 수** 만큼 증가
4. 마지막으로 물의 양이 2이상인 칸이면서 구름이 있지 않던 칸에서의 물의 양이 -= 2

<조건>
- 구름의 이동은 경계를 넘어서도 가능
- 구름의 물 복사는 경계를 넘을 수 없음.
- y == N, N-1 이고 x == 1, 2인 4개의 칸에 구름이 생김


<출력>
- M번의 이동이 모두 끝난 후 바구니에 들어있는 물의 합

<풀이 방법>
- 느낌상으로는 바구니에 물의 양이 2이상인 칸들을 저장해야 할 수도 있을 것 같다.
    - 따라서 연결 리스트를 사용해서 바구니의 물의 양을 기준으로 저장을 해야 할 수도 있을 것이다.

"""

N, M = map(int, input().split(' '))
board = []
for n in range(N):
    arr = list(map(int, input().split(' ')))
    board.append(arr)

DX, DY = [-1, -1, 0, 1, 1, 1, 0, -1], [0, -1, -1, -1, 0, 1, 1, 1]
visited = [[False for _ in range(N)] for _ in range(N)]
def init():
    visited = [[False for _ in range(N)] for _ in range(N)]
    return visited
def count_water_basket(x, y):
    """대각선 방향에 있는 물이 담긴 바구니의 수를 구한다."""
    global board
    cnt = 0
    for i in range(1, 8, 2):
        nx, ny = DX[i] + x, DY[i] + y
        if (0 <= nx < N and 0 <= ny < N) and board[ny][nx] != 0:
            cnt += 1
    return cnt

def change_point(x, y):
    x = x % N
    y = y  % N
    return x, y

def move_cloud(d, s, clouds):
    """이동 방향과 크기에 맞게 구름을 이동 시킨다. 이 때 방향은 원래 입력에서 -1을 한 값이다."""

    dx, dy = DX[d], DY[d]
    n = len(clouds)
    # clouds = deque([(N-1, 0), (N-1, 1), (N-2, 0), (N-2, 1)])

    for i in range(n):
        y, x = clouds.popleft()
        x,y = change_point(s * dx + x, s * dy + y)
        visited[y][x] = True
        clouds.append((y, x))

    # print(f"CLOUDS: {clouds}")
    return clouds

def update_cloud_rain(clouds):
    """구름에서 비가 내려서 구름이 있는 칸의 바구니에 저장된 물의 양 += 1"""
    for cloud in clouds:
        y, x = cloud
        board[y][x] += 1
def spread_water(clouds):
    """구름이 있었던 칸이 결국 물이 증가한 칸이고, 여기에 대각선 방향으로 거리가 1인 칸에 물이 있는 바구니의 수만큼 물이 증가"""
    for cloud in clouds:
        y, x = cloud
        water_count = count_water_basket(x, y)
        board[y][x] += water_count

def final_remove_water(clouds):
    new_clouds = deque([])

    for x in range(N):
        for y in range(N):
            # if (y, x) not in clouds and board[y][x] >= 2:
            if visited[y][x] == False and board[y][x] >= 2:
                board[y][x] -= 2
                new_clouds.append((y, x))
    return new_clouds

from collections import deque
clouds = deque([(N-1, 0), (N-1, 1), (N-2, 0), (N-2, 1)])
for m in range(M):
    visited = init()
    d, s = map(int, input().split(' ')) # 구름의 이동 방향, 이동 칸의 수
    clouds = move_cloud(d-1, s, clouds)
    update_cloud_rain(clouds)
    # print(board)
    spread_water(clouds)
    # print(board)
    clouds = final_remove_water(clouds)
    # print(board)
    # print("===")
print(sum([sum(a) for a in board]))


