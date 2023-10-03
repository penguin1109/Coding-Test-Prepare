""" 예술성
nxn 크기의 격자에 대해서 각 칸의 색을 1이상 10이하의 숫자로 표현한다.
<조건>
- 동일한 숫자가 상하좌우로 인접해 있으면 동일한 그룹으로 본다.
- 예술 점수: 모든 그룹 쌍의 조화로움의 합
    그룹 a와 b의 조화로움 점수 = (그룹 a에 속한 칸 수 + 그룹 b에 속한 칸 수) x 그룹 a를 이루는 숫자 x 그룹 b를 이루는 숫자 x 그룹 a와 b가 맞닿아 있는 변의 수
- 초기 예술 점수 = 그룹 쌍 간의 조화로움 값이 0보다 큰 조합의 조화로움의 모든 합
- 초기 예술 점수를 구하고 그림에 대해 회전을 한다.

<회전>
- 중앙을 기준으로 두 선을 그어 만들어지는 십자가 모양과 그 외의 부분으로 나눔.
1. 십자 모양: **반시계 90도**
2. 나머지 4개의 정사각형: **시계 90도**

<문제>
nxn 크기의 그림 정보가 주어졌을 때, (초기 예술 점수 + 1회전 이후 예술 점수 + 2회전 이후 예술 점수 + 3회전 이후 예술 점수) 를 구하여라
"""
from itertools import combinations

N = int(input().strip())
board = []

for n in range(N):
    board.append(list(map(int, input().strip().split(' '))))


def rotate_90(arr):
    n = len(arr)
    rot = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rot[j][n - 1 - i] = arr[i][j]
    return rot


def rotate():
    global board, N
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    size = (N - 1) // 2

    ## 정사각형 4개를 시계 방향 90도 회전한다.
    SX, SY = [0, 0, size + 1, size + 1], [0, size + 1, 0, size + 1]
    for sx, sy in zip(SX, SY):
        temp = [board[b][sy:sy+size] for b in range(sx, sx+size)]

        rotated = rotate_90(temp)
        for s in range(sx, sx+size):
            new_board[s][sy:sy+size] = rotated[s-sx]
        # new_board[sx:sx + size][sy:sy + size] = rotate_90(temp)
    ## 중앙의 십자가 모양을 반시계 방향 90도 회전한다.
    for i in range(N):
        temp = board[i][size]
        new_board[size][i] = temp
        temp = board[size][i]
        new_board[N - 1 - i][size] = temp

    return new_board

def check_range(x, y):
    return (0 <= x < N and 0 <= y < N)

def bfs(i, j, group, group_no):
    global board
    DX, DY = [-1, 0, 1, 0], [0, -1, 0, 1]
    q = [(i, j)]
    val = board[i][j]
    group[i][j] = group_no
    group_points = [[i, j]]
    while q:
        x, y = q.pop()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if check_range(nx, ny) and group[nx][ny] == 0 and val == board[nx][ny]:
                group[nx][ny] = group_no
                q.append([nx, ny])
                group_points.append([nx, ny])

    return group_points



def make_group():
    # 새롭게 회전 한 이후의 board를 바탕으로 그룹을 만들어 준다.
    global board
    GROUP = [[0 for _ in range(N)] for _ in range(N)]
    GROUP_POINTS = {}
    group_n = 1
    for i in range(N):
        for j in range(N):
            if GROUP[i][j] == 0:
                group_points = bfs(i, j, GROUP, group_n)
                GROUP_POINTS[group_n] = group_points
                group_n += 1
    return GROUP, group_n-1, GROUP_POINTS


def calc_art_score(group, group_points, a, b):
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    # 두 그룹이 맞닿아 있는 변의 수가 없다면 어차피 예술 점수가 0이다.
    a_n = len(group_points[a])
    b_n = len(group_points[b])
    a_v = board[group_points[a][0][0]][group_points[a][0][1]]
    b_v = board[group_points[b][0][0]][group_points[b][0][1]]
    side = 0
    # 이제 두 그룹이 맞닿아 있는 변의 수를 구해야 한다.
    b_pts = group_points[b]
    for pt in group_points[a]:
        ax, ay = pt
        for dx, dy in zip(DX, DY):
            nx, ny = dx + ax, dy + ay
            if check_range(nx, ny) and [nx, ny] in b_pts:
                # print(nx, ny, ax, ay)
                side += 1
    # print(a_n, b_n, a_v, b_v, side)
    return (a_n + b_n) * a_v * b_v * side




def all_art_scores():
    GROUP, group_n, GROUP_POINTS = make_group()
    # print(GROUP)
    hubos = list(combinations([int(i) for i in range(1, group_n+1)], 2))
    art_score = 0
    for hubo in hubos:
        score = calc_art_score(GROUP, GROUP_POINTS, hubo[0], hubo[1])
        if score>0:
            art_score += score
    # print(art_score)
    return art_score

answer = all_art_scores()
for i in range(3):
    board = rotate()
    # print(board)
    answer += all_art_scores()

print(answer)