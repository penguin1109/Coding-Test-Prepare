""" BOJ 2673 - 빙산
- 빙산이 분리되는 최초의 시간

1. board에서 총 빙산의 덩어리 수를 판단하는 함수 (check 함수)
2. board에 있는 빙산의 높이를 줄여주는 함수 (갱신 함수)
    - 중요한건 여기서 <동시에> 높이를 줄여주어야 한다는 것이다.

**python3으로도 시간초과 없이 성공할 수 있도록 하려면..?
-
"""
import copy
import sys
from collections import deque
input = sys.stdin.readline

N, M = map(int, input().split(' '))
board = []
ice = []
for n in range(N):
    arr = list(map(int, input().split(' ')))
    for m in range(M):
        if arr[m] != 0:
            ice.append((n, m))

    board.append(arr)

DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
def in_range(a, b):
    return (0 <= a < N and 0 <= b < M)
def update(board, ice):
    new_board = board.copy()
    new_ice = []
    for ice_pt in ice:
        n, m = ice_pt
        cnt = 0
        for dx, dy in zip(DX, DY):
            nx, ny = n + dx, m + dy
            if in_range(nx, ny) and board[nx][ny] == 0:
                cnt += 1
        new_board[n][m] = max(0, board[n][m] - cnt)
        if new_board[n][m] != 0:
            new_ice.append((n, m))
    return new_board, new_ice

def bfs(board, visited, a, b):
    q = deque([])
    q.append((a, b))
    idx = visited[a][b]
    while q:
        ta, tb = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = dx + ta, dy + tb
            if in_range(nx, ny) and board[nx][ny] != 0 and visited[nx][ny] == -1:
                visited[nx][ny] = idx
                q.append((nx, ny))


def check(board, ice):
    visited = [[-1 for _ in range(M)] for _ in range(N)]
    island_cnt = -1
    for single_ice in ice:
        n, m = single_ice
        if board[n][m] != 0 and visited[n][m] == -1:
            island_cnt += 1
            if island_cnt > 0:
                return True
            visited[n][m] = island_cnt
            bfs(board, visited, n, m)

    if island_cnt > 0:
        return True

    return False


time = 1
while True:
    board, ice = update(board, ice)
    # print(board, ice)
    if check(board, ice):
        print(time)
        break
    else:
        if len(ice) == 0:
            print(0)
            break
    time += 1
