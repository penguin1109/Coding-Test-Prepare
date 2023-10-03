import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, M, K = map(int, readl().strip().split(' ')) # 세로 길이, 가로 길이, 턴의 횟수

board = [] # 포탑들의 공격력을 저장하는 배열 #
towers = [] # 포탑 각각의 정보를 저장해서 attacker, target 선정에서 편한 정렬을 위해서 #
is_active = [[False for _ in range(M)] for _ in range(N)] # 포탑이 공격에 반영을 하였는지 트래킹하기 위한 배열 #
turn = 0 # 몇번째 turn을 진행중인지 트래킹하기 위한 변수 #
turns = [[0 for _ in range(M)] for _ in range(N)] # 제일 최근에 공격을 한 turn -> towers 배열 업데이트를 위해서 필요 #

for y in range(N):
    arr = list(map(int, readl().strip().split(' '))) # 격자의 정보 # 
    board.append(arr)
    for x, power in enumerate(arr):
        if power > 0:
            towers.append([power, 0, x+y, y, x]) # 나중에 정렬하기 쉽도록 -> (공격력, 제일 최근에 한 공격의 turn, 열+행, 열, 행)

############### UTILS #################
def in_range(x, y):
    return (0 <= x < M and 0 <= y < N)

def change_pos(x, y):
    if x == M:x = 0
    if x == -1:x = M-1
    if y == N:y=0
    if y == -1:y=N-1
    return x,y
    
towers = []
############### STEP0: 포탑 배열 towers 초기화 #############
def __init__():
    global board, towers, turn, is_active
    towers = []
    turn += 1
    for y, arr in enumerate(board):
        for x, power in enumerate(arr):
            if power > 0:
                towers.append([power, turns[y][x], x+y, y, x])
            is_active[y][x] = False
            
############### STEP2: 공격 ##############
"""
(1) 레이저 공격을 먼저 
    - 부서진 포탑이 있는 위치 == board[y][x] <= 0인 위치는 지날 수 없음
    - 가장자리에 도달하면 돌아서 반대 방향으로 가서 이동 가능함
    - 우하좌상의 우선순위로 이동 가능
    - 최단 경로 문제이기 때문에 당연히(?) BFS로 해결해야 하는 문제이다.

(3) 레이저 공격이 안되면 포탄 공격
    - 공격자를 중심으로 주위 8개의 방향에 있는 포탑이 피해를 입음
    - 던져지는 포탄의 좌표도 반대편으로 돌아서 이동 가
"""
def laser_attack(ax, ay, tx, ty, power):
    """
    @params (ax, ay): 공격자의 좌표
    @params (tx, ty): 공격 당하는 포탑의 좌표
    @params power: 공격자의 공격력
    """
    from collections import deque
    
    global board, turn, is_active
    
    DX, DY = [1, 0, -1, 0], [0, 1, 0, -1]
    visited = [[False for _ in range(M)] for _ in range(N)]
    track = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    visited[ay][ax] = True
    q = deque([[ax, ay]])
    arrived = False
    while q:
        x, y = q.popleft()
        if x == tx and y == ty:
            arrived = True
            break
        for dx, dy in zip(DX, DY):
            nx, ny = change_pos(x + dx, y + dy)
            if board[ny][nx] > 0 and visited[ny][nx] == False:
                visited[ny][nx] = True
                q.append([nx, ny])
                track[ny][nx] = [x, y] # 최단 경로의 방문 기록을 트래킹해야 하기 때문에 이전에 방문했던 좌표의 정보를 기록해 놓는다.#
    if arrived == False:
        bomb_attack(ax, ay, tx, ty, power)
    else:
        prev = track[ty][tx]
        turns[ay][ax] = turn # 현재 공격을 하였으니 공격자의 turns 배열 업데이트 #
        cx, cy = prev
        
        while not (cx == ax and cy == ay):
            board[cy][cx] -= power // 2
            is_active[cy][cx] = True
            cx, cy = track[cy][cx]
        
        board[ty][tx] -= power
        is_active[ty][tx] = True
        is_active[ay][ax] = True
    
    update()

def bomb_attack(ax, ay, tx, ty, power):
    global board, is_active
    
    DX, DY = [-1, -1, -1, 1, 1, 1, 0, 0], [-1, 1, 0, -1, 1, 0, -1, 1] # 8개의 방향이 존재 #
    turns[ay][ax] = turn
    
    for dx, dy in zip(DX, DY):
        nx, ny = change_pos(tx + dx, ty + dy)
        
        if nx == ax and ny == ay:
            continue
    
        if board[ny][nx] > 0:
            is_active[ny][nx] = True
            board[ny][nx] -= power // 2
    
    board[ty][tx] -= power
    is_active[ty][tx] = True
    is_active[ay][ax] = True
            
            
    
    
    
    
    
################ STEP5: 공격에 무관했던 포탑들 업데이트 ##############
def update():
    global board
    
    for y in range(N):
        for x in range(M):
            if board[y][x] > 0 and is_active[y][x] == False: # 공격력이 있는 포탑임과 동시에 이번 공격에는 무관한 경우 #
                board[y][x] += 1 # 공격력 1 증가 # 
            
def simulate():
    global towers
    ## (1) 제일 약한 포탑을 공격자로 선정 ##
    towers = sorted(towers, key = lambda x : (x[0], -x[1], -x[2], -x[4]))
    weak = towers[0]
    attacker_x = weak[4]
    attacker_y = weak[3]
    attacker_s = weak[0] + M + N
    board[attacker_y][attacker_x] = attacker_s
    towers[0] = [attacker_s, weak[1], attacker_x + attacker_y, attacker_y, attacker_x]
    
    ## (2) 자신 제외 제일 강한 포탑을 공격자로 선정 ##
    strong = towers[-1]
    target_x = strong[4]
    target_y = strong[3]
    
    ## (3) 공격 시작 ##
    laser_attack(attacker_x, attacker_y, target_x, target_y, attacker_s)
    

############### MAIN ##################
__init__()

for k in range(K):
    if len(towers) <= 1:
        break
    simulate()
    __init__()
    if len(towers) <= 1:
        break

answer = max([max(a) for a in board])
print(answer)



