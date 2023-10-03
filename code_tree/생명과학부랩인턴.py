"""
[출력] 모든 열을 검사 했을 때 채취한 곰팡이의 크기의 총합
"""

class Virus:
    def __init__(self, s, d, b):
        self.s = s # 1초 동안 곰팡이가 움직이는 거리
        self.d = d-1 # 이동 방향
        self.b = b # 곰팡이의 크기

N, M, K = map(int, input().strip().split(' ')) # 세로, 가로, 곰팡이의 수
board = [[[] for _ in range(M)] for _ in range(N)]
for k in range(K):
    x, y, s, d, b = map(int, input().strip().split(' '))
    new_virus = Virus(s, d, b)
    board[x-1][y-1].append(new_virus)

DX, DY = [0, 0, 1, -1], [-1, 1, 0, 0]
answer = 0
dir_dict = {0 : 1, 1 : 0, 2 : 3, 3 : 2}

def move_virus(virus, x, y):
    global DX, DY, dir_dict
    org_x, org_y = x, y
    move_dist, move_dir = virus.s, virus.d
    org_dir = virus.d
    nx, ny = x, y

    for d in range(move_dist):
        nx, ny = x + DX[move_dir], y + DY[move_dir]

        if nx == M or nx == -1:
            move_dir = dir_dict[move_dir]
            nx = x + DX[move_dir]
        if ny == N or ny == -1:
            move_dir = dir_dict[move_dir]
            ny = y + DY[move_dir]
        x, y = nx, ny
        virus.d = move_dir

    # print(f"X : {org_x} -> {nx} Y : {org_y} -> {ny} Dir : {org_dir} -> {virus.d}")

    return virus, x, y
       
def run(m):
    global answer, board
    ## STEP 1 : 해당 열에서 제일 먼저 발견하는 곰팡이 채취 ##
    for y in range(N):
        if len(board[y][m]) == 1:
            virus = board[y][m][0]
            answer += virus.b
            board[y][m] = []
            break

    
    ## STEP 2 : 곰팡이가 이동을 시작함 ##
    new_board = [[[] for _ in range(M)] for _ in range(N)] # 이동 후의 바이러스 board
    for y in range(N):
        for x in range(M):
            if len(board[y][x]) == 1:
                temp_virus = board[y][x][0] # 한 칸에 하나의 바이러스만 있음
                virus, nx, ny = move_virus(temp_virus, x, y)
                if len(new_board[ny][nx]) == 1:
                    comp = new_board[ny][nx][0]
                    if comp.b < virus.b:
                        new_board[ny][nx] = [virus]
                else:
                    new_board[ny][nx].append(virus)

    board = new_board


    
for m in range(M):
    run(m)

print(answer)