import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

class Shark:
    def __init__(self, s, d, z):
        self.speed = s
        self.dir = d
        self.size = z

R, C, M = map(int, readl().strip().split(' ')) # 세로, 가로, 상어의 수 #
board = [[[] for _ in range(C)] for _ in range(R)]
# [출력] 낚시왕이 잡은 상어의 크기의 합 #

for m in range(M):
    r, c, s, d, z = map(int, readl().strip().split(' ')) # y, x, 속력, 이동방향, 크기 #
    d -= 1
    new_shark = Shark(s, d, z)
    board[r-1][c-1].append(new_shark)

answer=  0
######## STEP 1 : 낚시왕이 이동한 다음에 땅이랑 제일 가까운 상어를 잡음 #########
def catch_shark(col):
    global board, answer
    for y in range(R):
        if len(board[y][col]) != 0:
            answer += board[y][col][0].size
            board[y][col] = []
            return

######## STEP 2 : 상어가 이동 함 ######

"""
- 상어가 이동을 0->1->2->3->4->5->4->3->2->1->0 이런 식이기 때문에 한 변의 길이가 6이면 한번의 cycle에서의 이동 거리는 6*2-2 = 10이다.
"""
def move_shark():
    global board
    DX, DY = [0, 0, 1, -1], [-1, 1, 0, 0] # 상-하-우-좌 #
    new_board = [[[] for _ in range(C)] for _ in range(R)]
    for y in range(R):
        for x in range(C):
            if len(board[y][x]) != 0:
                sx, sy = x, y
                shark = board[y][x][0] # 하나만 있으니까 첫번째만 다루면 된다. #
                speed = shark.speed;dir = shark.dir
                if dir == 0 or dir == 1:
                    # speed %= (R*2) if speed >= (R*2) else speed
                    speed = speed % (R*2-2)
                    for s in range(speed):
                        nx, ny = sx + DX[dir], sy + DY[dir]
                        if ny == -1 or ny == R:
                            dir = 1 if dir == 0 else 0
                            # nx, ny = sx, sy
                            nx, ny = sx + DX[dir], sy + DY[dir]
                        sx, sy = nx, ny
                        shark.dir = dir
                else:
                    # speed %= (C*2) if speed >= (C*2) else speed
                    speed = speed % (C*2-2)
                    for s in range(speed):
                        nx, ny = sx + DX[dir], sy + DY[dir]
                        if nx == -1 or nx == C:
                            dir = 3 if dir == 2 else 2
                            # nx, ny = sx, sy
                            nx, ny = sx + DX[dir], sy + DY[dir]
                        sx, sy = nx, ny
                        shark.dir = dir
                if new_board[sy][sx] == []:
                    new_board[sy][sx] = [shark]
                else:
                    if new_board[sy][sx][0].size < shark.size:
                        new_board[sy][sx] = [shark]
    return new_board

def print_board():
    global board
    for y in range(R):
        temp = []
        for x in range(C):
            if len(board[y][x]) > 0:
                temp.append((board[y][x][0].size, board[y][x][0].dir))
            else:
                temp.append((0,0))
        temp = [str(i) for i in temp]
        print(' '.join(temp))

if M == 0:
    print(0)
else:
    # print_board()
    # print('*' * 40)
    for col in range(C):
        catch_shark(col)
        # print_board()
        # print('*'* 20)
        board = move_shark()
        # print_board()
        # print('*' * 40)
    print(answer)