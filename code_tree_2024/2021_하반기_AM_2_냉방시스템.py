import sys
input = sys.stdin.readline

N, M, K = map(int, input().strip().split(' ')) # 격자 크기, 벽의 개수, 원하는 시원함 정도 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 고정된 에어컨의 위치 #
'''[출력] 모든 사무실의 시원함 정도가 K이상이 되기 위해 걸리는 최소 시간 (100분 넘으면 -1)'''
WIND = [[0 for _ in range(N)] for _ in range(N)]
MOVE = [[[True for _ in range(4)] for _ in range(N)] for _ in range(N)]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

# DX, DY = [0, -1, 0, 1], [-1, 0, 1, 0] # 위 왼 아래 오 #
DX, DY = [-1, 0, 1, 0], [0, -1, 0, 1] # 왼 위 오 아래 #
for m in range(M):
    y, x, s = map(int, input().strip().split(' '))
    s = abs(s-1)
    y -= 1;x-=1
    MOVE[y][x][s] = False
    nx, ny = x + DX[s], y + DY[s]
    if in_range(nx, ny):
        MOVE[ny][nx][s+2] = False

def check():
    global board, WIND
    for y in range(N):
        for x in range(N):
            if board[y][x] == 1 and WIND[y][x] < K:
                return False
    return True

def blow_wind(dirs, x, y):
    from collections import deque
    global WIND, MOVE
    q = deque([(x, y, 5)])
    blown = [[0 for _ in range(N)] for _ in range(N)]
    visited = [[False for _ in range(N)] for _ in range(N)]
    if in_range(x, y) == False:
        return
    visited[y][x] = True
    WIND[y][x] += 5
    blown[y][x] = 5
    while q:
        xx, yy, wind = q.popleft()
        # print((xx, yy, wind))
        if wind == 1:
            continue
        for dir in dirs:
            nx, ny = xx, yy
            valid = True
            for idx in dir:
                if MOVE[ny][nx][idx] == True:
                    nx, ny = nx + DX[idx], ny + DY[idx]
                else:
                    valid = False
                    break
                if in_range(nx, ny) == False:
                    valid = False;break
            if valid and visited[ny][nx] == False:
                q.append((nx, ny, wind-1))
                WIND[ny][nx] += (wind-1)
                visited[ny][nx] = True
                blown[ny][nx] += (wind-1)
    # debug(blown)
                
def mix_wind():
    global WIND
    changes = [[0 for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):                
            for di, (dx, dy) in enumerate(zip(DX, DY)):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) and MOVE[y][x][di] == True:
                    if WIND[y][x] > WIND[ny][nx]:
                        diff = WIND[y][x] - WIND[ny][nx]
                        changes[y][x] -= int(diff / 4)
                        changes[ny][nx] += int(diff / 4)
    for y in range(N):
        for x in range(N):
            WIND[y][x] += changes[y][x]

def decrease_wind():
    global WIND
    for x in range(N):
        for y in [0, N-1]:
            WIND[y][x] = max(0, WIND[y][x]-1)
    for y in range(1, N-1):
        for x in [0, N-1]:
            WIND[y][x] = max(0, WIND[y][x] -1)
        
def simulate():
    global WIND
    ## (1) ##
    for y in range(N):
        for x in range(N):
            if board[y][x] == 2: # 왼쪽 방향 => (왼) (위 왼) (아래 왼) # => (0) (1 0) (3 0) 
                blow_wind([[0], [1,0], [3,0]], x+DX[0], y+DY[0])
            elif board[y][x] == 3: # 위쪽 방향 -> (위) (왼 위) (오 위) # => (1) (0 1) (2 1)
                blow_wind([[1], [0,1],[2,1]], x+DX[1], y+DY[1])
            elif board[y][x] == 4: # 오른 방향 => (오) (위 오) (아래 오) # => (2) (1 2) (3 2)
                blow_wind([[2],[1,2],[3,2]], x+DX[2], y+DY[2])
            elif board[y][x] == 5: # 아래 방향 => (아래) (왼 아래) (오 아래) # => (3) (0 3) (2 3)
                blow_wind([[3], [0,3], [2,3]], x+DX[3], y+DY[3])
    # print("after blow..")
    # debug(WIND)
    ## (2) ##
    mix_wind()
    
    ## (3) ##
    decrease_wind()
    
def debug(board):
    print('*'*30)
    for y in range(N):
        print(' '.join([str(s) for s in board[y]]))
    print('*'*30)
answer = -1
for time in range(1, 101):                
    simulate()
    success = check()
    # debug(WIND)
    if success:
        print(time)
        exit(0)
    # debug(WIND)
    # exit(0)
print(answer)