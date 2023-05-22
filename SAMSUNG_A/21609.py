""" 상어 중학교
<문제 설명>
- NxN 크기의 격자에서 게임을 하고, 초기의 격자의 모든 칸에는 블록이 하나씩 들어 있다.
- 검은색, 무지개, 일반 블록
- 검(-1) 무지개(0) 일반(1~M)
- 인접한 칸 == 사방에 존재하는 칸(동서남북)

<블록 그룹의 특징>
- 연결된 블록의 집합 => 이 조건을 볼때 bfs를 사용해서 서로 이어질 수 있는 모든 경우를 찾아 주어야 한다.
- 일반 블록이 적어도 하나 있으며, 색이 모두 같아야 함
- 검(-1)은 없어야 함
- 무지개(0)은 상관 없음
- 2이상의 개수의 블록이 존재해야 함
- 기준 블록 = 0이 아닌 블록 중에서 행의 번호가 가장 작은 블록, 중에서 열이 가장 작은 블록

<오토 플레이 기능>
1. 크기가 가장 큰 블록 그룹을 찾는다.
    - 0의 개수가 가장 적은 블록
    - 기준 블록의 행이 가장 큰 것
    - 기준 블록의 열이 가장 큰 것
2. 1에서 찾은 블록 그룹의 모든 블록을 제거하고 블록 그룹에 속한 블록의 수가 B일 때 B^2점 획득
3. 격자에 중력이 작용
4. 격자가 90도 반시계 방향 회전
5. 다시 격자에 중력이 작용
    - 중력이 작용하면 검은색 블록을 제외한 모든 블록이 행의 번호가 큰 칸으로 이동한다.

<출력>
- 블록 그룹이 존재하는 동안 오토 플레이는 계속 반복되어야 한다.
- 오토 플레이가 모두 끝났을 때 획득한 점수의 합
"""

import sys
from collections import deque
import heapq

input = sys.stdin.readline

N, M = map(int, input().split(' ')) # 격자 한 변의 크기, 색상의 개수
board = []
for n in range(N):
    arr = list(map(int, input().split(' '))) # 격자의 칸에 들어있는 블록의 정보
    board.append(arr)

DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
visited = [[-1 for _ in range(N)] for _ in range(N)]
group_info = {}

score = 0
def bfs(x, y, n):
    global visited
    rainbow_block = 0 # 무지개 블록 개수 tracking
    blocks = [] # 블록 그룹의 기준 블록을 찾아야 함
    q = deque([[x, y]])
    temp_visited = visited.copy()
    cx, cy = x, y
    temp_visited[x][y] = n
    while q:
        a, b = q.popleft()
        heapq.heappush(blocks, [a, b])
        for dx, dy in zip(DX, DY):
            nx, ny = a + dx, b + dy
            if (0 <= nx < N and 0 <= ny < N):
                if board[nx][ny] == 0 and temp_visited[nx][ny] != n: # 무지개면 상관이 없음

            # if (0 <= nx < N and 0 <= ny < N) and temp_visited[nx][ny] == -1:
                # if board[nx][ny] == 0:
                    rainbow_block += 1
                    temp_visited[nx][ny] = n
                    q.append([nx, ny])
                elif temp_visited[nx][ny] == -1 and board[nx][ny] > 0 and board[nx][ny] == board[x][y]:
                    temp_visited[nx][ny] = n
                    # heapq.heappush(blocks, [nx, ny])
                    if cx > nx:
                        cx, cy = nx, ny
                    elif cx == nx:
                        if cy > ny:
                            cx, cy = nx, ny
                    q.append([nx, ny])

    if len(blocks) >= 2: # 2개 이상의 블록이 존재하는 경우
        visited = temp_visited
        group_info[n] = blocks
        # cx, cy = blocks[0]
        return True, cx, cy, rainbow_block, len(blocks)
    else:
        return False, -1, -1, -1, -1



def make_block_groups():
    global score
    group_count = 0
    block_groups = [] # 크기가 가장 큰 블록 그룹을 찾기 위해서
    for x in range(N):
        for y in range(N):
            # 검은색 블록은 있으면 안되고 아직은
            if visited[x][y] == -1 and board[x][y] != -1 and board[x][y] != -2 and board[x][y] != 0:
                valid_group, cx, cy, rainbow, size = bfs(x, y, group_count)
                if valid_group:
                    heapq.heappush(block_groups, [-size, -rainbow, -cx, -cy, group_count])
                    group_count += 1

    if len(block_groups) == 0:
        return -1

    largest_block = heapq.heappop(block_groups)
    nums = len(group_info[largest_block[-1]])
    score += nums * nums # 점수 획득
    return largest_block[-1] # 가장 큰 블록 그룹의 번호를 보내줌
def remove_largest(group_n):
    for x, y in group_info[group_n]:
        board[x][y] = -2 # 제거된 블록은 -2라고 나타내기로 한다.
def apply_gravity():
    global board
    for x in range(N-1, -1, -1):
        for y in range(N):
            if board[x][y] >= 0:
                move = False
                for ptr in range(x+1, N):
                    if board[ptr][y] != -2:
                        ptr -= 1
                        break
                    move = True

                if move:
                    board[ptr][y] = board[x][y]
                    board[x][y] = -2

def rotate_counter():
    global board
    # 격자가 90도 반시계 방향으로 회전하도록 한다.
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    for n in range(N):
        arr = board[n] # n번째 행
        for idx, a in enumerate(arr[::-1]):
            new_board[idx][n] = a

    board = new_board

def init():
    global visited, group_info
    visited = [[-1 for _ in range(N)] for _ in range(N)]
    group_info = {}

while True:
    init()
    largest_group = make_block_groups()
    if largest_group == -1: # 더이상 만들 수 있는 블록 그룹이 존재하지 않는 경우
        break
    remove_largest(largest_group)
    # print(board)
    apply_gravity()
    # print(board)
    rotate_counter()
    # print(board)
    apply_gravity()
    # print(board)
print(score)




