import sys
input = sys.stdin.readline
'''
- 턴이 한번 진행될 때 한 칸씩 이동
- 독점 계약은 k만큼의 턴 동안 유효 (k번 이후 주인 없는 칸이 됨)
- 각 플레이어는 방향 별 우선 순위가 존재. (우선은 독점 계약이 없는 칸으로, 그런게 없으면 자신이 독점 계약한 땅으로 이동)
- 모든 플레이어 이동 후 여러 플레이어가 있으면 제일 작은 번호를 갖는 플레이어만 살아남음.
- 위의 조건들로부터 추론해 볼 때 각각의 땅은 한명씩만 계약이 가능하다.

**중요: 모든 플레이어는 동시에 이동함**

[출력] 1번 플레이어만 살아남기까지 걸린 턴의 수
'''
DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] # 상하좌우 #
DIR_DICT = {
    0 : [0,1,2,3], 1 : [1,0,3,2], 2 : [2,3,1,0], 3 : [3,2,0,1]
}
EMPTY = (401, 401) # N <= 20인데 K <= N^2이기 떄문이다. #
EMPTY_NUM = 401
spent_time = 0
N, M, K = map(int, input().strip().split(' '))
board = [list(map(int, input().strip().split(' '))) for _ in range(N)]

next_dir = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(M+1)] # 우선순위에 맞춰서 view_dir이 0~3까지일때 각각의 다음 이동 방향을 저장 #
players = [[EMPTY for _ in range(N)] for _ in range(N)]
next_players = [[EMPTY for _ in range(N)] for _ in range(N)]
land = [[EMPTY for _ in range(N)] for _ in range(N)]

## get inputs ##
input_dirs = list(map(int, input().strip().split(' ')))
for di, move_dir in enumerate(input_dirs):
    for y in range(N):
        for x in range(N):
            if board[y][x] == di+1:
                players[y][x] = (di+1, move_dir-1)
                land[y][x] = (di+1, K)
                
for n in range(1, M+1):
    for cur_dir in range(4):
        dirs = list(map(int, input().strip().split(' ')))
        for di, dir in enumerate(dirs):
            next_dir[n][cur_dir][di] = dir-1
            
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def can_go(x, y, num):
    if in_range(x, y) == False:
        return False
    org_num, _ = land[y][x]
    return org_num == num

def next_pos(x, y, cur_dir):
    num, _ = players[y][x]
    ## (1) 독점 계약 안된 칸 찾기 ##
    for move_dir in next_dir[num][cur_dir]:
        nx, ny = x + DX[move_dir], y + DY[move_dir]
        if can_go(nx, ny, EMPTY_NUM):
            return (nx, ny, move_dir)
    ## (2) 독점 계약 안된게 없으면 본인이 계약한 칸 찾기 ##
    for move_dir in next_dir[num][cur_dir]:
        nx, ny = x + DX[move_dir], y + DY[move_dir]
        if can_go(nx, ny, num):
            return (nx, ny, move_dir)

def remove_small(x, y, new):
    global next_players
    if next_players[y][x][0] > new[0]:
        next_players[y][x] = new

def move(x, y):
    num, dir = players[y][x]
    nx, ny, new_dir = next_pos(x, y, dir)
    remove_small(nx, ny, (num, new_dir))

def remove_single_contract(x, y):
    global land
    num, left_time = land[y][x]
    if left_time == 1:
        land[y][x] = EMPTY
    else:
        land[y][x] = (num, left_time - 1)

def add_single_contract(x, y):
    global land
    num, _ = players[y][x]
    land[y][x] = (num, K)

def run():
    global next_players, players
    for y in range(N):
        for x in range(N):
            next_players[y][x] = EMPTY
    
    for y in range(N):
        for x in range(N):
            if players[y][x] != EMPTY:
                move(x, y)
    
    for y in range(N):
        for x in range(N):
            players[y][x] = next_players[y][x]
    
    for y in range(N):
        for x in range(N):
            if land[y][x] != EMPTY:
                remove_single_contract(x, y)
    
    for y in range(N):
        for x in range(N):
            if players[y][x] != EMPTY:
                add_single_contract(x, y)

def stop():
    global spent_time
    if spent_time >= 1000:
        return True
    for y in range(N):
        for x in range(N):
            if players[y][x] != EMPTY:
                num, _ = players[y][x]
                if num != 1:
                    return False
    return True


while not stop():
    run()
    spent_time += 1
if spent_time >= 1000:
    spent_time = -1
print(spent_time)
    