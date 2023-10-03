""" 마법사 상어와 블리자드
- 마법사 상어는 전체 격자의 중간에 위치해 있다.
- 실선은 벽이고, 점선은 벽이 아님. 
- NxN의 크기의 격자 사용
- 같은 번호를 가진 구슬이 번호가 연속하는 칸에 있으면 연속하는 구슬임
- 구슬 파괴 -> 빈칸

STEP 1 : 상어가 블리자드 마법 시전
- d방향으로 거리 s이하인 모든 칸에 얼음을 던져 그 칸의 구슬을 파괴하고, 파괴되면 빈칸이 된다. (벽은 가만히)

STEP 2 : 구슬 이동
- 현재 칸보다 번호가 하나 작은, 빈 칸일 떄 이동이 가능하고, 이동할데가 없을 떄까지 이동.
    - 칸의 번호는 방향이 작은 순서대로 이동한다.
    
STEP 3 : 구슬 폭발 & 이동
- 4개 이상의 연속하는 구슬이 있으면 폭발을 하고 빈자리가 생기면 구슬 이동
- 폭발하는 구슬이 없을 떄까지 반복

STEP 4 : 구슬 변화
- 연속하는 구슬 == 하나의 그룹
    - A = 그룹에 있는 구슬의 개수, B = 그룹을 이루는 구슬의 번호
- 모든 그룹이 순서대로 A, B로 각 2칸씩 차지한다.

[출력] 1x(폭발한 1번 구슬) + 2x(폭발한 2번 구슬) + 3x(폭발한 3번 구슬)
"""
from collections import deque

N, M = map(int, input().strip().split(' ')) # 격자의 크기, 수행한 마법의 개수
board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
shark_x, shark_y = N//2, N//2
DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] # 위, 아래, 왼, 오 
MAPIDX = deque() # 초기에 작성한 기본 이동을 위한 지도 queue
score = [0 for _ in range(3)] # 출력해야 하는 구슬의 폭발 status를 저장하기 위한 배열

def init_map():
    global MAPIDX
    x, y = shark_x, shark_y
    mv = 0
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]
    while True:
        for i in range(4):
            if i%2 == 0:
                mv += 1
            for _ in range(mv):
                x += dx[i];y += dy[i]
                MAPIDX.append([x, y])
                if x == 0 and y == 0: # 좌측 상단에 도달해서 더이상의 이동을 멈춰야 할 때
                    return 
                
def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

def shark_magic(D, S):
    """ STEP 1 : 상어의 블리자드 마법 시전
    """
    global board
    x, y = N//2, N//2
    for s in range(S):
        # nx, ny = shark_x + DX[D], shark_y + DY[D]
        x += DX[D]
        y += DY[D]
        if in_range(x, y):
            board[y][x] = 0
        else:
            break
    fill_blank()
    while explode():
        fill_blank()
    group()
        
def fill_blank():
    """ STEP 2, 3에 모두 사용이 되는, 빈칸이 없을 때까지 구슬이 이동하도록 하는 function
    """
    blankIdx = deque()
    for x, y in MAPIDX: # 상어의 위치 (격자의 중심)에서부터의 index 사용
        if board[y][x] == 0:
            blankIdx.append((x, y))
        elif board[y][x] > 0 and blankIdx: # 비어 있는 칸이 있는데 지금 구슬이 존재하면
            bx, by = blankIdx.popleft() # 제일 예전에 넣었던 index 사용
            board[by][bx] = board[y][x]
            board[y][x] = 0 # 원래 구슬이 있던 위치는 비어질 것이기 때문에 blankIdx에 또 넣어줌
            blankIdx.append((x, y))

def explode():
    """ STEP 3에서 4개의 연속하는 구슬이 폭발함
    """
    global score
    visited = deque()
    cnt = 0
    ball_num = -1
    did_explode = False
    for x, y in MAPIDX:
        if ball_num == board[y][x]:
            visited.append((x,y))
            cnt += 1
        else: ## 같은 그룹이 아님
            if cnt >= 4: # 폭발 가능
                score[ball_num-1] += cnt
                did_explode = True
                
                while visited:
                    nx, ny = visited.popleft()
                    board[ny][nx] = 0
            visited = deque()
            ball_num = board[y][x] # 현재 트래킹하는 그룹의 구슬 번호
            cnt = 1 # 현재 그룹의 구슬 개수는 1개로 바뀜 
            visited.append((x, y)) # 방문한 index 배열 업데이트
    return did_explode

def group():
    """ STEP 4 : 구슬을 같은 번호로 grouping 한 다음에 A, B로 바꿔서 board 갱신
    """
    cnt = 1
    tmpx, tmpy = MAPIDX[0]
    num = board[tmpy][tmpx] # 구슬의 번호
    nums = []
    
    for i in range(1, len(MAPIDX)): # 시작 위치 이후부터
        x, y = MAPIDX[i]
        if num == board[y][x]:
            cnt += 1
        else: # 그룹 분리
            nums.append(cnt);nums.append(num) # A, B 순서대로 입력
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
    
init_map()  
    
for m in range(M):
    d, s = map(int, input().strip().split(' ')) # 마법의 방향, 마법의 거리
    d -= 1
    shark_magic(D=d, S=s)

answer = 0

for idx, s in enumerate(score):
    answer += (idx+1) * s
print(answer)

