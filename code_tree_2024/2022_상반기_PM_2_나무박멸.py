import sys, copy
input = sys.stdin.readline

N, M, K, C = map(int, input().strip().split(' ')) # 격자의 크기, 박멸 진행 햇수, 제초제 확산 범위, 제초제가 남은 햇수 #
'''[출력] M년동안 박명한 총 나무의 그루 수를 구하여라'''

BOARD = [list(map(int, input().strip().split(' '))) for _ in range(N)]
KILL = [[0 for _ in range(N)] for _ in range(N)] # 제초제 #

DX, DY = [0, 1, 1, 1, 0, -1, -1, -1], [-1, -1, 0, 1, 1, 1, 0, -1] # 홀수: 4방 짝수: 대각선 #

answer = 0

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def growth_and_spread():
    global BOARD, KILL
    SPREAD = [[[] for _ in range(N)] for _ in range(N)]
    # new_board = copy.deepcopy(BOARD)
    for y in range(N):
        for x in range(N):
            if BOARD[y][x] <= 0:
                continue
            for di in range(0, 8, 2):
                nx, ny = x + DX[di], y + DY[di]
                if in_range(nx, ny):
                    if BOARD[ny][nx] > 0:
                        BOARD[y][x] += 1
                    elif BOARD[ny][nx] == 0 and KILL[ny][nx] == 0:
                        SPREAD[y][x].append((nx, ny))
    # debug(BOARD)
    new_board = copy.deepcopy(BOARD)
    for y in range(N):
        for x in range(N):
            to_spread = len(SPREAD[y][x])
            for (xx, yy) in SPREAD[y][x]:
                new_board[yy][xx] += BOARD[y][x] // to_spread
    BOARD = new_board
    

def dfs(x, y):
    new_board = [[-1 for _ in range(N)] for _ in range(N)] # copy.deepcopy(BOARD)
    killed = BOARD[y][x]
    new_kill = [[0 for _ in range(N)] for _ in range(N)] # copy.deepcopy(KILL)
    new_kill[y][x] = C+1
    new_board[y][x] = 0
    
    for di in range(1, 8, 2):
        xx, yy = x, y
        for k in range(K):
            nx, ny = xx + DX[di], yy + DY[di]
            if in_range(nx, ny): # and BOARD[ny][nx] >= 0:
                new_kill[ny][nx] = C+1
                if BOARD[ny][nx] > 0:
                    # new_kill[ny][nx] = C+1
                    killed += BOARD[ny][nx]
                    new_board[ny][nx] = 0
                else:
                    break
            else:
                break
        
            xx, yy = nx, ny
            
    return killed,new_board,new_kill

def kill():
    global KILL, BOARD, answer
    MAX_KILL = -1
    NEW_BOARD = [[-1 for _ in range(N)] for _ in range(N)] # copy.deepcopy(BOARD)
    NEW_KILL = [[0 for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            if BOARD[y][x] < 0:
                continue
            elif BOARD[y][x] == 0:
                if MAX_KILL < 0:
                    MAX_KILL = 0
                    NEW_KILL[y][x] = C+1
            else:
                killed, new_board, new_kill = dfs(x, y)
                if killed > MAX_KILL:
                    MAX_KILL = killed
                    NEW_KILL = new_kill
                    NEW_BOARD = new_board
          
    # BOARD = NEW_BOARD
    # # KILL[ky][kx] = C+1
    # KILL = NEW_KILL
    answer += MAX_KILL
    for y in range(N):
        for x in range(N):
            if NEW_KILL[y][x] == C+1:
                KILL[y][x] = C+1
            if KILL[y][x] > 0:
                KILL[y][x] -= 1
            if NEW_BOARD[y][x] == 0:
                BOARD[y][x] = 0


def simulate():
    growth_and_spread()
    kill()

def debug(board):
    print('*'* 30)
    for y in range(N):
        print(' '.join([str(a) for a in board[y]]))
    print('*' * 30)
    
for _ in range(M):
    simulate()
    

print(answer)
                
            