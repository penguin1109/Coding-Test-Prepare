import sys
import copy
input = sys.stdin.readline
'''[출력] M년이 지난 후 남아있는 리브로수 높이들의 총 '''
N, M = map(int, input().strip().split(' ')) # 격자의 크기, 총 키우는 햇수 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 서로 다른 리브로수의 높이 #
NEU = [(0, N-1), (0, N-2), (1, N-1), (1, N-2)] # 특수 영양제가 있는 위치 #
DX, DY = [1, 1, 0, -1, -1, -1, 0, 1], [0, -1, -1, -1, 0, 1, 1, 1] ## 대각선 : (1, 3, 5, 7) ## 

def get_new_xy(x, y):
    if x >= N:x = 0
    elif x < 0:x = N-1
    if y >= N:y = 0
    elif y < 0:y = N-1
    return x, y

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def simulate(dir, pix):
    global NEU, board
    for i, (x, y) in enumerate(NEU):
        '''이렇게 그냥 이동 크기를 곱해서 새로운 (x, y) 좌표를 구하는게 맞는지 모르겠음'''
        for p in range(pix):
            nx, ny = x + DX[dir]*pix, y + DY[dir]*pix
            nx, ny = get_new_xy(nx, ny)
            x, y = nx, ny
        NEU[i]= (nx, ny)
        board[ny][nx] += 1 # 특수 영양제를 넣은 땅의 리브로수의 높이가 1만큼 증가 #
    new_board = copy.deepcopy(board)
    visited = [[False for _ in range(N)] for _ in range(N)]

    for i, (x, y) in enumerate(NEU):
        for di in range(1, 8, 2):
            nx, ny = x + DX[di], y + DY[di]
            if in_range(nx, ny) == True and board[ny][nx] >= 1:
                new_board[y][x] += 1
                visited[y][x] = True
    NEU = []
    for y in range(N):
        for x in range(N):
            if new_board[y][x] >= 2 and visited[y][x] == False:
                new_board[y][x] -= 2
                NEU.append((x, y))
    board = new_board              
        

for m in range(M):
    d, p = map(int, input().strip().split(' ')) # 이동 방향, 이동 칸 수 #
    d -= 1
    simulate(d, p)

answer = sum([sum(arr) for arr in board])
print(answer)