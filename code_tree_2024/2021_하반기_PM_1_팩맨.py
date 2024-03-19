import sys
input = sys.stdin.readline
import heapq
import copy

DX, DY = [0, -1, -1, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1, 0, -1] # 증가할수록 반시계 45도씩 회전 #
'''[출력] t개의 턴이 지난 후 살아남은 몬스터의 총 마리 수'''

M, T = map(int, input().strip().split(' ')) # 몬스터 마리수, 턴의 수 #
R, C = map(int, input().strip().split(' ')) # 초기 위치 (Y, X) #
R -= 1;C -= 1
ALIVE = 1
EGG = 0
DEAD = -1
MAXEAT = -1
TRACK = [[(-1, -1) for _ in range(4)] for _ in range(4)]
CORPUS = [[False for _ in range(4)] for _ in range(4)] # 죽은 몬스터 트래킹 #
BOARD = [[[] for _ in range(4)] for _ in range(4)]

def in_range(x, y):
    return 0 <= x < 4 and 0 <= y < 4

## STEP 1 ##
def copy_monster():
    global BOARD
    for y in range(4):
        for x in range(4):
            arr = []
            for (dir, status) in BOARD[y][x]:
                if status == ALIVE:
                    arr.append((dir, EGG))
                    arr.append((dir, ALIVE))
                else:
                    arr.append((dir, status))
            BOARD[y][x] = arr

## STEP 2 ##
def get_dir(dir, x, y):
    for i in range(8):
        d = (dir+i) % 8
        nx, ny = x + DX[d], y + DY[d]
        if in_range(nx, ny) and CORPUS[ny][nx] == False:
            if (R == ny and C == nx):
                continue
            else:
                return d, nx, ny
    return dir, x, y
    
        
def move_monster():
    global BOARD
    new_board = [[[] for _ in range(4)] for _ in range(4)]
    
    for y in range(4):
        for x in range(4):
            for (dir, status) in BOARD[y][x]:
                if status == ALIVE:
                    new_dir, nx, ny = get_dir(dir, x, y)
                    new_board[ny][nx].append((new_dir, status))
                    # print(f"{x},{y} -> {nx},{ny}")
                else:
                    new_board[y][x].append((dir, status))
    
    BOARD = new_board
    
## STEP 3 ##
def dfs(x, y, cnt, eaten, track):
    global MAXEAT, TRACK, R, C
    # print(track)
    if cnt == 3:
        if MAXEAT < eaten:
            MAXEAT = eaten
            TRACK = copy.deepcopy(track) 
            R, C = y, x
        # print(TRACK)
        return
    for di in range(0, 8, 2):
        nx, ny = x + DX[di], y + DY[di]
        if in_range(nx, ny):
            prev = track[ny][nx]
            if prev == (-1, -1):
                temp = 0
                track[ny][nx] = (y, x)
                for (d, stat) in BOARD[ny][nx]:
                    if stat == ALIVE:
                        temp += 1
                dfs(nx, ny, cnt+1, eaten+temp, track)
                track[ny][nx] = prev 
            else:
                '''여기서 과거 방문한 위치를 다시 방문하면 안된다는 조건이 없기 때문에 그냥 else 문으로 처리'''
                track[ny][nx] = (y, x)
                dfs(nx, ny, cnt+1, eaten, track)
                track[ny][nx] = prev
    
        
def move_packman():
    global R, C, BOARD, CORPUS
    global MAXEAT, TRACK
    # from collections import deque
    # q = deque([(0, R, C, 0)])
    
    visited = [[False for _ in range(4)] for _ in range(4)]
    visited[R][C] = True
    track = [[(-1, -1) for _ in range(4)] for _ in range(4)]
    track[R][C] = (R, C)
    MAXEAT = -1
    '''MAXEAT값이 0이면 잡은 몬스터 역시 0인 경우에 팩멘의 위치가 하나도 업데이트가 안될 수 도 있다.'''
    
    dfs(C, R, 0, 0, track)
    
    # print(TRACK)
    # print(f"Max Eaten : {MAXEAT} (x, y) : {C},{R}")
    cur_x, cur_y = C, R
    for _ in range(3):
        # print(cur_x, cur_y)
        for mi, (dir, status) in enumerate(BOARD[cur_y][cur_x]):
            if status == ALIVE:
                BOARD[cur_y][cur_x][mi] = (dir, DEAD)
                CORPUS[cur_y][cur_x] = True
        cur_y, cur_x = TRACK[cur_y][cur_x]

            
    
## STEP 4 ##
def clean():
    '''for loop 2번씩 돌면서 소멸 & 복제 & 부화'''
    global BOARD, CORPUS
    alive = 0
    
    new_board = [[[] for _ in range(4)] for _ in range(4)]
    for y in range(4):
        for x in range(4):
            corpus = 0
            for (dir, status) in BOARD[y][x]:
                if status == -3:
                    continue
                elif status <= DEAD:
                    new_board[y][x].append((dir, status-1))
                    corpus += 1
                elif status == ALIVE:
                    new_board[y][x].append((dir, status))
                    alive += 1
                elif status == EGG:
                    new_board[y][x].append((dir, ALIVE))
                    alive += 1
                    
            if corpus > 0:
                CORPUS[y][x] = True
            else:
                CORPUS[y][x] = False
                
    BOARD = new_board
    return alive

def simulate():
    copy_monster()
    # print(BOARD)
    # print(CORPUS)
    move_monster()
    # print(BOARD)
    move_packman()
    alive = clean()
    # print(BOARD)
    return alive

for m in range(M):
    r, c, d = map(int, input().strip().split(' '))
    BOARD[r-1][c-1].append((d-1, ALIVE))


for t in range(T):
    alive = simulate()
    
print(alive)
    
