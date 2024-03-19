import sys
input = sys.stdin.readline
from collections import deque

N, M, K = map(int, input().strip().split(' ')) # 격자의 크기, 팀의 크기, 라운드의 수 #
'''[출력] K번의 라운드 동안 각 팀이 얻게 되는 점수의 총합'''

GROUPS = [[] for _ in range(M)]

BOARD = [list(map(int, input().strip().split(' '))) for _ in range(N)]
ROAD = [[-1 for _ in range(N)] for _ in range(N)]
CLOCK = [[0 for _ in range(N)] for _ in range(N)] # 시계방향으로 머리 사람을 따라 이동해야 할 때의 각 위치에서의 방향 #
COUNTER = [[0 for _ in range(N)] for _ in range(N)] # 반시계 방향으로 머리 사람을 따라 이동해야 할 때의 각 위치에서의 방향 #
TAIL = [0 for _ in range(M)] # 각 팀당 꼬리 사람의 index 번호를 넣어줌 #

visited = [[False for _ in range(N)] for _ in range(N)]


DX, DY = [1, 0, -1, 0], [0, -1, 0, 1]

answer = 0

def in_range(x, y):
    return 0 <= x < N and 0 <= y <N

class Group:
    def __init__(self, routes):
        self._make_route(routes)
    
    def _make_route(self, routes):
        from collections import defaultdict
        route_dict = defaultdict(list)
        for (x, y, role) in routes:
            route_dict[role].append((x, y))
        self.route_dict = route_dict

def dfs(x, y, idx):
    global GROUPS, visited
    visited[y][x] = True
    ROAD[y][x] = idx
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy
        if in_range(nx, ny) and visited[ny][nx] == False:
            if 1 <= BOARD[ny][nx] <= 4:
                if len(GROUPS[idx]) == 1 and BOARD[ny][nx] != 2:
                    continue
                if BOARD[ny][nx] == 3:
                    TAIL[idx] = len(GROUPS[idx])
                GROUPS[idx].append((nx, ny))
                dfs(nx, ny, idx)
    
    
def init_group():
    global visited
    visited = [[False for _ in range(N)] for _ in range(N)]
    group = 0
    
    for y in range(N):
        for x in range(N):
            if BOARD[y][x] == 1 and visited[y][x] == False:
                GROUPS[group].append((x, y))
                dfs(x, y, group)
                group += 1

def move():
    global GROUPS, BOARD
    for gi in range(M):
        new_head = GROUPS[gi][-1]
        for j in range(len(GROUPS[gi])-1, 0, -1):
            GROUPS[gi][j] = GROUPS[gi][j-1]
        GROUPS[gi][0] = new_head
    
    for i in range(M):
        for j, (x, y) in enumerate(GROUPS[i]):
            if j == 0:
                BOARD[y][x] = 1
            elif j < TAIL[i]:
                BOARD[y][x] = 2
            elif j == TAIL[i]:
                BOARD[y][x] = 3
            else:
                BOARD[y][x] = 4

def get_score(y, x):
    global answer
    
    group_idx = ROAD[y][x]
    people_idx = GROUPS[group_idx].index((x, y))
    # print(f"HIT group : {group_idx} ppl : {people_idx}")
    answer += (people_idx+1) * (people_idx+1)

def reverse(group_idx):
    global GROUPS
    if group_idx == -1:
        return
    new_groups = []
    for j in range(TAIL[group_idx], -1, -1):
        new_groups.append(GROUPS[group_idx][j])
    for j in range(len(GROUPS[group_idx])-1, TAIL[group_idx], -1):
        new_groups.append(GROUPS[group_idx][j])
    GROUPS[group_idx] = new_groups[:]
    
    ## update BOARD ##
    for j, (x, y) in enumerate(GROUPS[group_idx]):
        if j == 0:
            BOARD[y][x] = 1
        elif j == TAIL[group_idx]:
            BOARD[y][x] = 3
        elif j < TAIL[group_idx]:
            BOARD[y][x] = 2
        else:
            BOARD[y][x] = 4
    
def throw_ball(turn):
    t = (turn - 1) % (4 * N) + 1 # ROW (Y축 좌표) #
    if t <= N: # 왼 -> 오 #
        for i in range(N): # COL (X축 좌표) #
            if 1 <= BOARD[t-1][i] <= 3:
                get_score(t-1, i)
                return ROAD[t-1][i]
            
    elif t <= 2 * N: # COL #
        t -= N
        for i in range(N-1, -1, -1): # ROW #
            if 1 <= BOARD[i][t-1] <= 3:
                get_score(i, t-1)
                return ROAD[i][t-1]
    elif t <= 3 * N:
        t = 3*N-t+1
        for i in range(N-1, -1, -1): # COL #
            if 1 <= BOARD[t-1][i] <= 3:
                get_score(t-1, i)
                return ROAD[t-1][i]
    else:
        t = 4*N - t + 1
        for i in range(N): # COL #
            if 1 <= BOARD[i][t-1] <= 3:
                get_score(i, t-1)
                return ROAD[i][t-1]
    return -1

def debug(board):
    print('*'*30)
    for y in range(len(board)):
        print(' '.join([str(a) for a in board[y]]))            
    print('*'*30)

def simulate(turn):
    global answer
    move()
    group_idx = throw_ball(turn)
    # print(f"HIT GROUP : {group_idx}")
    reverse(group_idx)
    
init_group()
for i in range(1, K+1):
    simulate(i)
    # print(f"TAIL : {TAIL}")
    # debug(BOARD)
# debug(ROAD)
print(answer)



                            