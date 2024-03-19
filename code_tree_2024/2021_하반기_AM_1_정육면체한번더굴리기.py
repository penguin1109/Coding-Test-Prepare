import sys, copy
input = sys.stdin.readline

'''[출력] 주사위를 M번 굴렸을 때까지 얻게 되는 점수의 총 합'''

N, M = map(int, input().strip().split(' ')) # 격자의 크기, 굴리는 횟수 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # 우, 하, 좌, 상 #
# 주사위의 아랫면을 계속 트래킹 해야 함 #
DICE = [
    [0, 0, 5, 0],
    [6, 4, 1, 3],
    [0, 0, 2, 0]
]
DIR = 0
BX, BY = 0, 1 # 주사위의 아랫면 #
SX, SY = 0, 0
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def roll_dice(dir):
    global DICE
    MOVE = [(0, 1), (2, 2), (2, 1), (2, 0)] # 1->0 2->1 3->2 0->3 #
    DOWN_DICT = {1:0,2:1,3:2,0:3}
    UP_DICT = {0:1,1:2,2:3,3:0}
    if dir == 0: # 오른쪽으로 1칸 굴림 #
        arr = DICE[1][:3]
        arr = [DICE[1][-1]] + arr
        DICE[1] = arr
    elif dir == 2: # 왼쪽으로 1칸 굴림 #
        arr = DICE[1][1:]
        arr.append(DICE[1][0])
        DICE[1] = arr
    elif dir == 1: # 아래로 1칸 굴림 #
        new_dice = copy.deepcopy(DICE)
        for i in range(4):
            src_x, src_y = MOVE[i]
            dst_x, dst_y = MOVE[DOWN_DICT[i]]
            new_dice[dst_y][dst_x] = DICE[src_y][src_x]
        DICE = new_dice
    else: # 위로 1칸 굴림 #
        new_dice = copy.deepcopy(DICE)
        for i in range(4):
            src_x, src_y = MOVE[i]
            dst_x, dst_y = MOVE[UP_DICT[i]]
            new_dice[dst_y][dst_x] = DICE[src_y][src_x]
        DICE = new_dice

def get_score(x, y):
    from collections import deque
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[y][x] = True
    q = deque([(x,y)])
    score = board[y][x]
    while q:
        xx, yy = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = xx + dx, yy + dy
            if in_range(nx, ny) and visited[ny][nx] == False and board[y][x] == board[ny][nx]:
                q.append((nx, ny))
                visited[ny][nx] = True
                score += board[ny][nx]
    return score
    
    
def simulate():
    global DIR, DICE, SX, SY
    # (1) #
    nx, ny = SX + DX[DIR], SY + DY[DIR]
    if in_range(nx, ny) == False:
        DIR = (DIR + 2) % 4
        nx, ny = SX + DX[DIR], SY + DY[DIR]
    SX, SY = nx, ny
    # print(DICE)
    # (2) #
    roll_dice(DIR)
    # print(DICE)
    # print(f"ROLLED, {DIR}")
    # (3) #
    down_num = DICE[BY][BX]
    # print(f"DOWN : {down_num}")
    if down_num > board[SY][SX]:
        DIR = (DIR + 1) % 4
    elif down_num < board[SY][SX]:
        DIR = (DIR+3)%4

answer = 0
for m in range(M):
    simulate()
    score = get_score(SX, SY)
    answer += score
print(answer)        