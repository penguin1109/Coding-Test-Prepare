import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # 우-하-좌-상 #
# [출력] M번 주사위를 굴렸을 때 얻게 되는 총 점수의 합 #
N, M = map(int, readl().strip().split(' ')) # 격자의 크기, 굴리는 횟수 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

dice = [
    [0, 0, 5, 0], [1, 4, 6, 3], [0, 0, 2, 0]
]
BOT = [[2, 0], [0, 1], [2, 2], [2, 1], [2, 0]]
TOP = [[2, 0], [2, 1], [2, 2], [0, 1], [2, 0]]
DIR_DICT = {0:2,1:3,2:0,3:1}
def copy_mat(org):
    new = [[0 for _ in range(4)] for _ in range(3)]
    for y in range(3):
        for x in range(4):
            new[y][x] = org[y][x]
    return new
def roll_dice(dir):
    # import copy
    global dice
    new_dice = copy_mat(dice)
    if dir == 0: # 오른쪽으로 굴리는 경우 #
        arr = dice[1]
        top = arr[0]
        new = arr[1:];new.append(top)
        new_dice[1] = new
    elif dir == 1: # 아래로 굴리는 경우 #
        for i in range(4):
            x, y = BOT[i]
            nx, ny = BOT[i+1]
            new_dice[ny][nx] = dice[y][x]
            # print(new_dice, dice)
    elif dir == 2: # 왼쪽으로 굴리는 경우 #
        arr = dice[1]
        last = arr[-1]
        new = arr[:-1];new.insert(0, last)
        new_dice[1] = new
    else: # 위로 굴리는 경우 #
        for i in range(4):
            x, y = TOP[i];nx, ny = TOP[i+1]
            new_dice[ny][nx] = dice[y][x]
    # print(new_dice)
    return new_dice
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N
def get_score(sx, sy):
    from collections import deque
    q = deque([[sx, sy]])
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True
    cnt = 1
    while q:
        x, y = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) == False:
                continue
            if visited[ny][nx] == True:
                continue
            if board[ny][nx] != board[sy][sx]:
                continue
            visited[ny][nx] = True
            q.append([nx, ny])
            cnt += 1
    return cnt
def move_dice(x,y,dir):
    global dice
    nx, ny = x + DX[dir], y + DY[dir]
    if in_range(nx, ny) == False: # 격자를 벗어나서 굴려지는 경우 #
        dir = DIR_DICT[dir]
        nx, ny = x + DX[dir], y + DY[dir] # 다시 이동 #
    dice = roll_dice(dir)
    # print(dice, dir)
    board_n = board[ny][nx]
    dice_bot = dice[1][2] # 주사위의 밑면의 숫자 #
    if dice_bot > board_n:
        dir = (dir+1)%4
    elif dice_bot < board_n:
        dir = (dir-1+4)%4
    score = get_score(nx, ny) * board[ny][nx]
    return nx, ny, dir, score

x, y, dir = 0, 0, 0
answer = 0
for m in range(M):
    x, y, dir, score = move_dice(x, y, dir)
    answer += score
print(answer)



