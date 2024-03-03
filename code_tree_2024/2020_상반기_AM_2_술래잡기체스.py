import sys
import copy
input = sys.stdin.readline

'''
- 처음에 술래는 (0, 0)에 위치해 있으면서 거기 있는 도둑 말을 잡는다.
- 도둑말은 번호가 작은 순서대로 한 칸씩 이동하는데, 빈칸이나 다른 도둑말이 있는 칸으로 이동이 가능하다.
- 다른 도둑말이 있으면 그 말과 칸을 바꾼다.
- 술래는 무조건 도둑말이 있는 곳으로 이동을 해야 함.
- 술래말이 이동할 수 있는 곳에 도둑말이 더 이상 존재하지 않는 경우에 끝!

[출력] 얻을 수 있는 점수의 최댓값
'''
DX, DY = [0, -1, -1, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1, 0, -1]
board = [[[] for _ in range(4)] for _ in range(4)]
CAUGHT = (-1, -1)
answer = 0

def in_range(x, y):
    return 0 <= x < 4 and 0 <= y < 4

def get_runner(idx, board):
    for y in range(4):
        for x in range(4):
            if board[y][x][0] == idx:
                return x, y
    return None

def get_movable_dir(x, y, catcher, board):
    num, dir = board[y][x]
    for i in range(8):
        new_dir = (dir + i) % 8
        nx, ny = x + DX[new_dir], y + DY[new_dir]
        if in_range(nx, ny) == False: # 범위 안에 없으면 continue #
            continue
        if board[ny][nx] == CAUGHT: # 빈칸인 경우에 #
            if nx == catcher[0] and ny == catcher[1]: # 술래말이면 continue #
                continue
            # 그냥 빈칸이면 채워 넣기 #
            board[ny][nx] = (num, new_dir)
            board[y][x] = CAUGHT
            return
        else: # 다른 도둑말이 위치한 칸이라면 swap #
            temp = board[ny][nx]
            board[ny][nx] = (num, new_dir)
            board[y][x] = temp
            return
    
def get_max_score(score, catcher, board):
    global answer
    answer = max(answer, score)
    '''recursive function'''
    # (1) 모든 말들이 이동 #
    # for i in range(16):
    for i in range(1, 17):
        ret = get_runner(i, board)
        if ret is None:
            continue
        x, y = ret
        # print(x, y)
        # 이동 가능한 방향을 찾기 위해서 도둑말이 45도씩 반시계 회전하도록 함 #
        get_movable_dir(x, y, catcher, board)
        # print(board, score)
    # exit(0)
    # (2) 술래말이 이동 #
    did_move = False
    # for di, (dx, dy) in enumerate(zip(DX, DY)):
    xx, yy, dir = catcher
    # print(board)
    while True:
        nx, ny = xx + DX[dir], yy + DY[dir]
        if in_range(nx, ny) == False:
            break
        if board[ny][nx] == CAUGHT:
            xx, yy = nx, ny
            continue
        # 도둑말이 있는 위치를 잡은 경우 #
        org_board = copy.deepcopy(board)
        org = board[ny][nx]
        org_board[ny][nx] = CAUGHT
        did_move = True
        get_max_score(score+org[0], (nx, ny, org[1]), org_board)
        # board[ny][nx] = org
        xx, yy = nx, ny
            
    if did_move == False:
        answer = max(answer, score)
        # print(answer)
        return
        
                
    
for i in range(4):
    arr = list(map(int, input().strip().split(' ')))
    for j in range(4):
        board[i][j] = (arr[2*j], arr[2*j+1]-1) # (번호, 방향) #

start = board[0][0]
board[0][0] = CAUGHT
get_max_score(start[0], (0, 0, start[1]), board)
print(answer)