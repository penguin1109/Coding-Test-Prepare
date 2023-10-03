import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

"""
STEP 1 : 머리사람을 시작으로 1칸씩 각 팀의 구성원들이 움직인다. (move)
STEP 2 : 공이 현재 라운드 번호에 맞는 방향으로 던져지고, 공을 제일 먼저 맞은 사람이 머리사람으로부터 n번째이면 n**2의 점수를 얻음 (throw_ball)
STEP 3 : 공을 먼저 맞은 사람이 포함된 군집은 머리 <=> 꼬리 (reverse)

"""
## 출력 : 각 팀이 획득한 점수의 총합 ##

N, M, K = map(int, readl().strip().split(' ')) # 격자의 크기, 팀의 개수, 라운드의 수

board = [list(map(int, readl().split(' '))) for _ in range(N)]

move_indices = [[] for _ in range(M+1)] # 각 군집들의 이동 경로 index를 저장하는 배열 # 
tail = [0 for _ in range(M+1)]          # 각 군집의 꼬리 사람의 move_indices에서의 번호를 저장하는 배열 #

visited = [[False for _ in range(N)] for _ in range(N)] 
team_split = [[0 for _ in range(N)] for _ in range(N)] # 각 팀별 이동 경로에 맞춰서 해당 팀의 번호를 저장하는 배열 #

total_score = 0                       # 정답 저장 변수 # 
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1] # 이동 방향에 별도의 우선순위는 없음

def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

def dfs(x, y, idx):
    """군집화를 해서 이동 경로를 저장하기 위해서 사용"""
    global visited, team_split
    visited[y][x] = True
    team_split[y][x] = idx # 팀 번호 저장
    
    for dx, dy in zip(DX, DY): 
        nx, ny = x + dx, y + dy
        if in_range(nx, ny) == False: # 격자안에 있지 않은 경우에는 제외 #
            continue
        if visited[ny][nx] == True:   # 이미 방문한 칸인 경우에는 제외 #
            continue
        if board[ny][nx] == 0: # 빈칸인 경우에는 입력을 하지 않음 # 
            continue 
        if len(move_indices[idx]) == 1 and board[ny][nx] != 2: # 처음 탐색이면 2가 있는 방향으로 이동 # 
            continue
        move_indices[idx].append((nx, ny))
        if board[ny][nx] == 3: # 꼬리 사람인 경우에
            tail[idx] = len(move_indices[idx])
        dfs(nx, ny, idx)
        
            
def init():
    cnt = 1
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1: # 머리 사람
                move_indices[cnt].append((j, i)) # (x, y) 순서로 입력
                cnt += 1 # 군집의 개수 업데이트 
    for i in range(1, M+1):
        x, y = move_indices[i][0]
        dfs(x, y, i)
        
######################### STEP1 #########################
def move():
    global board
    for i in range(1, M+1):
        temp_tail = move_indices[i][-1]
        for j in range(len(move_indices[i])-1, 0, -1):
            move_indices[i][j] = move_indices[i][j-1]
        move_indices[i][0] = temp_tail # 먼저 이동을 하기 위해서 move_indices 배열을 업데이트
    
    # 업데이트된 move_indices 배열에 맞춰서 board 업데이트 #
    for i in range(1, M+1):
        for j, (x, y) in enumerate(move_indices[i]):
            if j == 0:
                board[y][x] = 1 # 머리 사람
            elif j < tail[i] - 1:
                board[y][x] = 2 # 중간 사람
            elif j == tail[i]-1:
                board[y][x] = 3 # 꼬리 사람
            else:
                board[y][x] = 4 # 공백
                
        
######################### STEP2 #########################
def throw_ball():
    global k
    
    def get_score(x, y):
        global total_score
        idx = team_split[y][x]
        cnt = move_indices[idx].index((x, y))
        total_score += (cnt+1)**2
        
    # 현재 round의 번호는 k이고, 이거에 맞춰서 공이 던져지게 된다.
    """
    1~N : 오른쪽으로 위에서부터 순서대로 
    N+1~2N : 위로 왼쪽부터 순서대로
    """
    turn = (k+1) % (4*N)
    turn += 1
    if turn <= N: # 오른쪽으로 공 던짐
        for i in range(N):
            if 1 <= board[turn-1][i] <= 3: # 꼬리 사람, 머리 사람, 나머지 사람인 경우에 제일 먼저 공에 맞음
                get_score(turn, i)
                return team_split[turn][i]
    elif N+1 <= turn <= 2*N: # 위로 공 던짐
        turn -= N
        for i in range(N):
            if 1 <= board[N-i-1][turn-1] <= 3:
                get_score(N-i-1, turn)
                return team_split[N-i][turn]
            
    elif 2*N+1 <= turn <= 3*N: # 왼쪽으로 공 던짐
        turn -= (2*N)
        for i in range(N):
            if 1 <= board[N-turn-1][N-1-i] <= 3:
                get_score(N-turn, N-1-i)
                return team_split[N-turn][N-i-1]
    else: ## 아래로 공 던짐
        turn -= (3*N)
        for i in range(N):
            if 1 <= board[N-1-turn][N-1-i] <= 3:
                get_score(N-1-turn, N-1-i)
                return team_split[i][N-1-turn]
    return 0
    
######################### STEP3 #########################
def reverse(team_idx):
    global move_indices
    if team_idx == 0: # 공을 맞은 군집이 없으면
        return
    new = []
    for j in range(tail[team_idx]-1, -1, -1):
        new.append(move_indices[team_idx][j])
    for j in range(len(move_indices[team_idx])-1, tail[team_idx]-1, -1):
        new.append(move_indices[team_idx][j])
    
    move_indices[team_idx] = new[:]
    
    for j, (x, y) in enumerate(move_indices[team_idx]):
        if j == 0:
            board[y][x] = 1
        elif j < tail[team_idx]-1:
            board[y][x] = 2
        elif j == tail[team_idx]-1:
            board[y][x] = 3
        else:
            board[y][x] = 4
######################### MAIN ##########################
init()
for k in range(K):
    move()
    team_idx = throw_ball()
    reverse(team_idx)

print(total_score)