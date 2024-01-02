import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 크기 #
board = []
not_certain = []

combinations = []
init = []

def make_init():
    global init
    for x in range(N):
        init.append([x, 0])
    for y in range(N):
        init.append([N-1, y])
    for x in range(N-1, -1, -1):
        init.append([x, N-1])
    for y in range(N-1, -1, -1):
        init.append([0, y])

for y in range(N):
    arr = list(map(int, readl().strip().split(' ')))
    board.append(arr)
    for x in range(N):
        if arr[x] == 3:
            not_certain.append([x, y])

def make_combinations(n, idx, temp):
    import copy
    global combinations

    if idx == n:
        combinations.append(temp)
        return
    for i in range(3):
        new = copy.deepcopy(temp);new[idx] = i
        make_combinations(n, idx+1, new)

def remove_many(check):
    num_ball = 0
    for y in range(N):
        for x in range(N):
            if len(check[y][x]) >= 2:
                check[y][x] = []
            elif len(check[y][x]) == 1:
                num_ball += 1
    return check, num_ball

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

DIR_DICT = {0 : {0:0,1:1,2:2,3:3}, 1 : {0:1,1:0,2:3,3:2}, 2 : {0:3,3:0,1:2,2:1}}
def simulate(combination):
    import copy
    DX, DY = [0, -1, 0, 1], [1, 0, -1, 0] # 하-좌-상-우 #

    escaped = 0 # 격자 밖으로 탈출한 구슬의 개수를 업데이트 할 변수 #
    # (1) 불확실한 칸에 대해서 지정된 값으로 바꾼 격자판을 새로 만들어 준다. #
    new_board = copy.deepcopy(board)
    for idx, (x, y) in enumerate(not_certain):
        new_board[y][x] = combination[idx]

    # (2) 구슬 이동을 시작한다. #
    check = [[[] for _ in range(N)] for _ in range(N)]
    for i in range(N*4):
        if balls[i] == 1:
            x, y = init[i]
            dir = DIR_DICT[new_board[y][x]][i//N]
            check[y][x].append(dir)
    # (3) 2개 이상의 구슬이 놓여 있으면 제거 #
    check, num_ball = remove_many(check)
    if num_ball == 0:
        return escaped
    while True:
        new_check = [[[] for _ in range(N)] for _ in range(N)]
        for y in range(N):
            for x in range(N):
                if len(check[y][x]) == 0:
                    continue
                dir = check[y][x][0]
                nx, ny = x + DX[dir], y + DY[dir]
                if in_range(nx, ny) == False: # 격자를 벗어나면 탈출한 것임 #
                    escaped += 1
                else:
                    dir = DIR_DICT[new_board[ny][nx]][dir]
                    new_check[ny][nx].append(dir)
        check, num_ball = remove_many(new_check)

        if num_ball == 0:
            break

    return escaped



balls = list(map(int, readl().strip().split(' '))) # 구슬이 어떤 격자의 벽면 중 어디에 위치해 있는지 나타냄 #


temp = [0 for _ in range(len(not_certain))]
make_combinations(len(not_certain), 0, temp)

answer = 0
make_init()
for combination in combinations:
    ret = simulate(combination)
    answer = max(answer, ret)
print(answer)


