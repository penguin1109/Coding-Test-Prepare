""" 포탑 부수기
- NxM의 크기의 격자가 존재
- 각 포탑에 공격력이 존재하고, 늘거나 줄수 있으며 공격력이 0이하면 부서지고 공격 불가능
- 하나의 턴에서 4가지 action을 K번 반복한다.
1. 공격자 선정
    - 공격력이 0이 아니면서 가장 낮은 포탑 == 제일 약한 포탑 
    - 제일 최근에 공격했으면 동시에 제일 약한 포탑
    - 행과 열의 합이 제일 큰 포탑 (제일 우측 하단)
    - 열의 값이 제일 큰 포탑 (제일 오른쪽)
    - 제일 공격력이 약하면 N+M의 공격력을 추가로 부여

2. 공격자의 공격
    - 위에서 선정한 공격자가 업데이트된 공격력을 바탕으로 자신을 제외한 제일 강한 포탑 공격 ==> 공격할 포탑은 직접 순회하면서 찾아야 할 듯
    - 자신 제외 제일 공격력이 높고
    - 행과 열의 합이 제일 작고 (제일 좌측 상단)
    - 열의 값이 제일 작은 포탑 (제일 왼쪽)
    - 공격을 할 때는 레이저 공격을 먼저 하고 포탄 공격을 한다.
    2-1. 레이저 공격
        - DX, DY 4개의 방향으로 이동 가능
        - 부서진 포탑의 위치로는 갈수 없음 (== 공격력이 0이하인 위치로는 이동 불가능)
        - 격자를 지나서 반대편으로 이동 가능
        - 무조건 공격자 위치에서 공격 대상까지 최단 경로로 이동
        - 우->하->좌->상의 순서로 이동 가능
        - 이동 경로에 있는 포탑은 공격자의 공격력의 절반이 빠짐.
        - 공격 대상자는 공격자의 공격력만큼 빠짐.
    
    2-2. 포탄 공격
        - 공격 대상자는 공격자의 공격력만큼 빠짐
        - 공격 대상자 주위 8방도 피해를 공격자 공격력의 절반만큼 받는다.
        - 8방으로 영향 받는게 반대편에도 동일하게 적용이 된다.

3. 포탑 부서짐
    - 공격력이 0 이하가 되었으면 부서져야 함

4. 포탑 정비
    - 살아남은 포탑 중에서 공격 받지 않았던 포탑과 공격 대상자가 아니었던 포탑은 공격력 +1 

[출력] 전체 과정이 종료된 이후에 남아있는 포탑 중에서 가장 강한 포탑의 공격력을 출력하여라.
"""

class Tower:
    def __init__(self, x, y, r, p):
        self.x = x
        self.y = y
        self.r = r
        self.p = p


DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # 우-하-좌-상
N, M, K = map(int, input().strip().split(' '))
turns = [[0] * M for _ in range(N)]
is_active = [[False for _ in range(M)] for _ in range(N)] ## 반드시 업데이트가 필요한건지 아닌지 트래킹하는 배열을 추가해 주자
visit = [[False for _ in range(M)] for _ in range(N)]
towers = []
turn = 0

board = [list(map(int, input().strip().split(' '))) for _ in range(N)]

def _init_towers():
    ## 다시 towers 배열을 업데이트 해준다. (board 정보를 바탕으로 => 따라서 공격할 때 board 배열만 갱신을 해 주면 된다.)
    global board, towers, turn, is_active
    towers = []
    turn += 1
    for y, arr in enumerate(board):
        for x, info in enumerate(arr):
            if info > 0:
                new_tower = Tower(x, y, turns[y][x], info)
                towers.append(new_tower)  

            is_active[y][x] = False
    

def move_point(x, y):
    nx, ny = x, y
    if x == M:
        nx = 0
    if x == -1:
        nx = M-1
    if y == N:
        ny = 0
    if y == -1:
        ny = N-1
    
    return nx, ny

def update():
    global board

    for y in range(N):
        for x in range(M):
            if board[y][x] > 0:
                if is_active[y][x] == False:
                    board[y][x] += 1 ## 공격력이 1씩 올라감 (공격과 무관했던 포탑들)
        

def bomb_attack(x, y, s, ax, ay):
    global board
    DX8, DY8 = [-1, -1, -1, 1, 1, 1, 0, 0], [0, -1, 1, -1, 1, 0, -1, 1]
    turns[y][x] = turn
    is_active[ay][ax] = True

    for dx, dy in zip(DX8, DY8):
        nx, ny = dx + ax, dy + ay
        nx, ny = move_point(nx, ny)

        if nx == x and ny == y:
            continue

        if board[ny][nx] > 0:
            is_active[ny][nx] = True
            board[ny][nx] -= s//2 # 경로에 있는 사람 공격력 업데이트 

    board[ay][ax] -= s # 공격 받은 사람 공격력 업데이트
    is_active[y][x] = True


def attack(x, y, s, ax, ay):
    # 공격자 좌표, 공격 당하는 좌표
    global DX, DY, board
    attacker = [x,y]
    attacked = [ax, ay]
    from collections import deque
    q = deque([[x, y]])
    track = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    visited = [[False for _ in range(M)] for _ in range(N)]

    visited[y][x] = True
    affected = []
    arrived = False

    while q:
        x, y = q.popleft()
        if x == ax and y == ay:
            arrived=True
            break
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            nx, ny = move_point(nx, ny)

            if board[ny][nx] > 0 and visited[ny][nx] == False: ## 이동하려면 공격력이 0 초과인 자리여야 함
                track[ny][nx] = [x, y] ## 이전에 방문한 곳
                q.append([nx, ny])
                visited[ny][nx] = True
                
        
    if arrived == False:
        ## 최단 경로를 구할 수 없다면 포탄 공격을 함 ##
        ax, ay = attacked
        Ax, Ay = attacker
        bomb_attack(Ax, Ay, s, ax, ay)

    else:
        ## 최단 경로를 구했으니 레이저 공격을 함 ##
        ax, ay = attacked
        Ax, Ay = attacker
        prev = track[ay][ax]

        turns[Ay][Ax] =  turn
        cx, cy = prev
        is_active[Ay][Ax] = True
        
        while not (cx == Ax and cy == Ay):
            board[cy][cx] -= s//2
            is_active[cy][cx] = True
            next_cx, next_cy = track[cy][cx]
            cx, cy = next_cx, next_cy
            

        board[ay][ax] -= s # 원래 공격 대상인 포탑의 공격력을 줄여줌
        is_active[ay][ax] = True

    # (4) 공격 후에 바로 포탑 정비를 함
    update()



def single_turn():
    global towers, DX, DY
    # (1) 공격자 선정
    # attacker = heapq.heappop(towers)
    towers.sort(key=lambda x : (x.p, -x.r, -(x.x + x.y), -x.x))

    attacker = towers[0]
    attacker_x = attacker.x 
    attacker_y = attacker.y
    attacker_s = attacker.p + M + N # 공격자의 공격력
    board[attacker_y][attacker_x] = attacker_s # 공격쟈의 공격력을 핸디캡 만큼 업데이트 
    attacker.p = attacker_s
    towers[0] = attacker
    
    # (2) 공격 대상자 선정
    attacked = towers[-1]
    attacked_x = attacked.x
    attacked_y = attacked.y
    # (3) 공격하기
    attack(attacker_x, attacker_y, attacker_s, attacked_x, attacked_y)
    

    
_init_towers()
for k in range(K):
    if len(towers) <= 1:
        break
    single_turn()
    _init_towers()

    if len(towers) <= 1:
        break

answer = max([max(a) for a in board])
print(answer)