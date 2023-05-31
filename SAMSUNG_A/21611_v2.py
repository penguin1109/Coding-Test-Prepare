import sys
input = sys.stdin.readline
from collections import deque

N, M = map(int, input().split(' '))
DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] ## 위, 아래, 왼, 오
board = [list(map(int, input().split(' ')))  for _ in range(N)]
MAPIDX = deque() ## 이건 바뀌지 않고 계속 동일하게 유지되는 초기 기본 이동 지도이다.
score = [0 for _ in range(3)]
""" (1) 초기 작업 - Map Index Initialize
- 2D의 격자에서 중심 좌표에 있는 상어를 기준으로 회오리 모양으로 회전을 하는데, 각 번호를 순서대로 격자의 좌표를 저장해 주어서 1D 배열에 정보를 저장한다.

"""
def init_map_index():
    x, y = N // 2, N//2
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]
    mv = 0
    while True:
        for i in range(4):
            if i % 2 == 0:
                mv += 1
            for j in range(mv):
                x += dx[i]
                y += dy[i]
                MAPIDX.append([x,y])
                if x == 0 and y == 0:
                    return
def check_range(x, y):
    return 0 <= x < N and 0 <= y < N

def magic(d, s):
    x, y = N//2, N//2
    ## (1) 지정해준 방향으로 지정해준 거리만큼 이동한다.
    for i in range(s):
        x += DX[d]
        y += DY[d]
        if check_range(x, y) == False:
            break
        board[y][x] = 0

    ## (2) 빈칸이 없도록 이동한다.
    fill_blank()
    ## (3) 더이상 폭발할 <연결된 구슬>이 없을 때까지 이동을 한다.
    while explode():
        fill_blank()
    ## (4) 연결된 구슬로부터 A, B를 구해서 배열을 다시 채워 준다.
    group()

def fill_blank():
    blankIdx = deque()
    for x, y in MAPIDX: ## 격자의 중심으로부터 가장 먼저 이동하면 나오는 위치부터 작은 번호 순서대로
        if board[y][x] == 0: # 비어 있으면
            blankIdx.append((x, y)) # 비어있는 좌표에 입력
        elif board[y][x] > 0 and blankIdx: # 비어 있는 칸이 있고 현재 칸에는 구슬이 있으면
            nx, ny = blankIdx.popleft()
            board[ny][nx] = board[y][x]
            board[y][x] = 0 # 원래 구슬이 있던 위치는 비게 된다.
            blankIdx.append((x, y))

def explode():
    global score
    visited = deque()
    cnt = 0
    ball_num = -1 ## 내가 원래 구현 했을 때 None으로 지정해 놓은 것과 동일하다.
    did_explode = False
    for x, y in MAPIDX: ## 확실히 순서대로 인덱스 좌표 값을 저장해 놓으니까 구슬을 이동시키기 편함
        if ball_num == board[y][x]: ## 같은 색의 group을 이룰 수 있는 경우
            visited.append((x, y))
            cnt += 1
        else: ## 이제 group이 분리 되는 경우
            if cnt >= 4:
                score[ball_num-1] += cnt
                did_explode = True ## 폭발 하였으면 계속 이동을 해야 한다 (빈칸이 생기니까)

                while visited: ## 어쨌든 visited 배열은 비워야 하기 때문에
                    nx, ny = visited.popleft() ## FIFO으로 입력한 빈칸의 좌표부터 뽑아서 사용한다.
                    # if cnt >= 4: ## 4개 이상의 연결 된 같은 구슬 번호가 group을 이루었다면 폭발
                    board[ny][nx] = 0
            visited = deque()
            ball_num = board[y][x] ## 새로운 구슬 번호로 업데이트
            cnt = 1 ##  현재 그룹의 구슬 수 1개로 업데이트
            visited.append((x, y)) ## visited 배열 업데이트
    return did_explode

def group():
    cnt = 1
    tmpx, tmpy = MAPIDX[0]
    num = board[tmpy][tmpx]
    nums = []
    for i in range(1, len(MAPIDX)):
        x, y = MAPIDX[i][0], MAPIDX[i][1]
        if num == board[y][x]:
            cnt += 1
        else:
            nums.append(cnt)
            nums.append(num)
            num = board[y][x]
            cnt = 1
    idx = 0
    for x, y in MAPIDX:
        if not nums:
            break
        board[y][x] = nums[idx]
        idx += 1
        if idx == len(nums):
            break

init_map_index()
for m in range(M):
    d, s = map(int, input().split(' '))
    d -= 1
    magic(d, s)
    # print(board)
# print(len(MAPIDX))
answer = 0
for idx, s in enumerate(score):
    answer += (idx+1) * s
print(answer)
