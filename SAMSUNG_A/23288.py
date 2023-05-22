""" 주사위 굴리기 2
<문제 조건>
- NxM인 크기의 지도
- 지도의 오른쪽은 동쪽, 위쪽은 북쪽

<주사위 이동>
1. 동쪽으로 한 칸 굴러감 (이동방향에 칸이 없으면 반대로 한 칸 굴러감)
2. 주사위가 도착한 칸에 해당하는 숫자만큼의 점수 획득
3. 주사위 아랫면의 정수 A와 (x, y)의 정수 B를 비교해 이동 방향 결정
    - A > B: 90도로 시계 방향 회전
    - A = B: 변화 없음
    - A < B: 90도로 반시계 방향 회전
** 점수 획득 방법: 동서남북으로 연속해서 이동할 때 (x,y)좌표의 값이 나오는 개수에 (x,y) 좌표의 값을 곱한다.

"""
import sys
from collections import deque
input = sys.stdin.readline

N, M, K = map(int, input().split(' ')) # 세로, 가로, 이동 횟수

board = []
for n in range(N):
    arr = list(map(int, input().split(' '))) # 지도에 쓰여 있는 수
    board.append(arr)

vertical = deque([2, 1, 5, 6])
horizontal = deque([4, 1, 3])

dice_x, dice_y = 0, 0 # 처음에 주사위는 외쪽 위에 위치해 있다.
dice_dir = 0
# DX, DY = [0, 0, 1, -1], [-1, 1, 0, 0] # 동-서-남-북
# 동-남-서-북
DX, DY = [0, 1, 0, -1], [1, 0, -1, 0]
def roll_dice():
    global dice_x, dice_y, dice_dir, horizontal, vertical
    nx, ny = dice_x + DX[dice_dir], dice_y + DY[dice_dir]
    if (0 <= nx < N and  0 <= ny < M):
        dice_x, dice_y = nx, ny
    else:
        if dice_dir == 0 or dice_dir == 1:
            dice_dir += 2
        else:
            dice_dir -= 2
        nx, ny = dice_x + DX[dice_dir], dice_y + DY[dice_dir]
        if (0 <= nx < N and 0 <= ny < M):
            dice_x, dice_y = nx, ny

    if dice_dir == 0: # 동쪽으로 굴려야 하는 경우
        bottom = vertical.pop()
        move = horizontal.pop()
        vertical.append(move)
        horizontal.appendleft(bottom)
        vertical[1] = horizontal[1]
    elif dice_dir == 2: # 서쪽으로 굴려야 하는 경우
        move = horizontal.popleft()
        bottom = vertical.pop()
        vertical.append(move)
        horizontal.append(bottom)
        vertical[1] = horizontal[1]
    elif dice_dir == 3: # 북쪽으로 굴려야 하는 경우
        move = vertical.popleft()
        vertical.append(move)
        horizontal[1] = vertical[1]
    else: # 남쪽으로 굴려야 하는 경우
        move = vertical.pop()
        vertical.appendleft(move)
        horizontal[1] = vertical[1]

score = 1
def dfs(x, y, cnt, visited):
    global score
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy

        if (0 <= nx < N and 0 <= ny < M) and board[x][y] == board[nx][ny] and visited[nx][ny] == False:
            visited[nx][ny] = True
            dfs(nx, ny, cnt + 1, visited)
            visited[nx][ny] = False
    return cnt


def calculate_score():
    # score = 1
    # 주사위가 도착한 칸에 대해서 점수 계산

    score = 1
    q = deque([[dice_x, dice_y, 0]])
    visited = [[False for _ in range(M)] for _ in range(N)]
    visited[dice_x][dice_y] = True

    while q:
        x, y, dist = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if (0 <= nx < N and 0 <= ny < M) and (visited[nx][ny] == False) and board[nx][ny] == board[dice_x][dice_y]:
                q.append([nx, ny, dist+1])
                score += 1
                visited[nx][ny] = True


    # print(f"SCORE : {score}")

    return score * board[dice_x][dice_y]

def change_dir():
    global dice_dir
    B = board[dice_x][dice_y]
    A = vertical[-1]
    # print(f"A: {A} B: {B}")
    if (A > B): # 시계방향으로 변경
        dice_dir = (dice_dir + 1) % 4
    elif (A < B): # 반시계방향으로 변경
        dice_dir = (dice_dir + 3)  % 4
    ## 같을 때는 변화가 없음.

answer= 0
for trial in range(K):
    score = 1
    roll_dice()
    change_dir()
    answer += calculate_score()
#     change_dir()

    # print(horizontal, vertical)
    # print(dice_x, dice_y)
    # print(dice_dir)
print(answer)











