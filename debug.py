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
import heapq

DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # 우-하-좌-상
N, M, K = map(int, input().strip().split(' '))
towers = []
turn = 1
# board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
board = []
for y in range(N):
    arr = list(map(int, input().strip().split(' ')))
    temp = []
    for a in arr:
        temp.append([a, 1])
    board.append(temp)

def _init_towers():
    ## 다시 towers 배열을 업데이트 해준다. (board 정보를 바탕으로 => 따라서 공격할 때 board 배열만 갱신을 해 주면 된다.)
    global board, towers, turn
    towers = []
    turn += 1
    for y, arr in enumerate(board):
        for x, info in enumerate(arr):
            if info[0] > 0:
                heapq.heappush(towers, [info[0], -info[1], -(x+y), -x]) ## 공격력, 공격으로부터 지난 시간 (=현재 turn - 공격했을 때 turn), 열의 번호
    

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

def update(affected, attacker, attacked):
    global board, turn

    check = [[False for _ in range(M)] for _ in range(N)]
    check[attacker[1]][attacker[0]] = True
    board[attacker[1]][attacker[0]][1] = turn ## 공격자의 각성 시간만 갱신 해줌 
    check[attacked[1]][attacked[0]] = True
    # board[attacked[1]][attacked[0]][1] += 1

    for x, y in affected:
        check[y][x] = True
        # board[y][x][1] += 1

    for y in range(N):
        for x in range(M):
            if board[y][x][0] > 0:
                if check[y][x] == False:
                    check[y][x] = True
                    # board[y][x][1] += 1 ## 마지막 공격으로부터의 시간이 1이 더해짐
                    board[y][x][0] += 1 ## 공격력이 1씩 올라감 (공격과 무관했던 포탑들)
        

def bomb_attack(x, y, s, ax, ay):
    global board
    DX8, DY8 = [0, 0, -1, -1, -1, 1, 1, 1], [-1, 1, 0, -1, 1, 0, -1, 1]
    affected = []
    for dx, dy in zip(DX8, DY8):
        nx, ny = dx + ax, dy + ay
        nx, ny = move_point(nx, ny)
        if nx == x and ny == y:
            continue
        if board[ny][nx][0] > 0:
            board[ny][nx][0] -= s//2 # 경로에 있는 사람 공격력 업데이트 
        affected.append([nx, ny])
    board[ay][ax][0] -= s # 공격 받은 사람 공격력 업데이트

    return affected


def attack(x, y, s, ax, ay):
    # 공격자 좌표, 공격 당하는 좌표
    global DX, DY, board
    attacker = [x,y]
    attacked = [ax, ay]
    from collections import deque
    q = deque([[x, y]])
    track = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    track[y][x] = [0, 0]
    order = []
    # print(f"X: {x} Y: {y}")
    # print(f"AX: {ax} AY : {ay}")
    affected = []
    arrived = False

    while q:
        x, y = q.popleft()
        now_stop = False
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            nx, ny = move_point(nx, ny)
            # print(f"X : {nx} Y : {ny} S : {board[ny][nx]}")
            if board[ny][nx][0] > 0 and track[ny][nx] == [-1, -1]: ## 이동하려면 공격력이 0 초과인 자리여야 함
                track[ny][nx] = [x, y] ## 이전에 방문한 곳
                q.append([nx, ny])
                order.append([nx, ny])
                if (ny == ay and nx == ax):
                    # print("Arrived")
                    arrived = True
                    now_stop = True
                    break
            if now_stop:
                break
        if now_stop:
            break
        
    # print(f"Order : {order}")
    if arrived == False:
        # print("Bomb Attack")
        ## 최단 경로를 구할 수 없다면 포탄 공격을 함 ##
        ax, ay = attacked
        Ax, Ay = attacker
        affected = bomb_attack(Ax, Ay, s, ax, ay)

    # if affected == []:
    
    else:
        # print("Laser Attack")
        ax, ay = attacked
        Ax, Ay = attacker
        prev = track[ay][ax]

        board[Ay][Ax][1] = turn # 공격자가 이번에 공격을 하였음을 업데이트 
        # print(order)
        for i in range(len(order)-1, -1, -1):
            x, y = order[i]
            if x == ax and y == ay:
                continue
            if x == Ax and y == Ay: ## 시작했던 점에 도달하면 멈추기
                break
            if prev[0] == x and prev[1] == y:
                affected.append([x, y])
                board[y][x][0] -= s//2 # 공격 당하는 포탑의 공격력을 줄여줌
                prev = track[y][x]

                
        board[ay][ax][0] -= s # 원래 공격 대상인 포탑의 공격력을 줄여줌
        
    # print(f"Affected : {affected}")
    # (4) 공격 후에 바로 포탑 정비를 함
    update(affected, attacker=attacker, attacked=attacked)



    
    
    

def single_turn():
    global towers, DX, DY
    # (1) 공격자 선정
    attacker = heapq.heappop(towers)
    attacker_x = attacker[3]*-1
    attacker_y = (-1 * attacker[2]) - attacker_x
    attacker_s = attacker[0] + M + N # 공격자의 공격력
    board[attacker_y][attacker_x][0] = attacker_s # 공격쟈의 공격력을 핸디캡 만큼 업데이트 
    
    # print(f"Attacker: {attacker} Strength: {attacker_s}")
    # (2) 공격 대상자 선정
    q = []
    for t in towers:
        if t[0] > 0:
            heapq.heappush(q, [-t[0], -t[1], -t[2], -t[3]])
    attacked = heapq.heappop(q)
    attacked_x = attacked[3]
    attacked_y = attacked[2] - attacked_x
    # print(f"Attacked: {attacked}")
    # (3) 공격하기
    attack(attacker_x, attacker_y, attacker_s, attacked_x, attacked_y)
    

    

_init_towers()
for k in range(K):
    # single_turn()
    _init_towers()
    # print(board)
    if len(towers) <= 1:
        break
    single_turn()

answer = max(max([max(a) for a in board]))
print(answer)