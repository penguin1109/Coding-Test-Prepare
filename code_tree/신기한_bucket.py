import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline
# [출력] block이 떨어질 위치가 정해지지 않은 경우에 대해 떨어질 위치를 잘 정하여 얻을 수 있는 점수의 합을 최대로 하여라 #
N = int(readl().strip()) # 블록의 수 #
board = [[0 for _ in range(4)] for _ in range(N+1)]

DX, DY = [0, -1, -1, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1, 0, -1]
BLOCK_DICT = {}
for n in range(1, 8+1):
    arr = list(map(int, readl().strip().split(' ')))
    arr = [i-1 for i in arr]
    BLOCK_DICT[n] = arr
import copy
cases = []
block_order = []
for n in range(N):
    k, c = map(int, readl().strip().split(' ')) # 블록의 종류, 블록이 떨어질 위치 #
    block_order.append(k)

    if 1 <= c <= 4:
        if len(cases) == 0:
            cases.append([c])
        else:
            new = []
            for i, case in enumerate(cases):
                case.append(c);new.append(case)
            cases = new
    else:
        new = []
        for j in range(1, 5):
            if len(cases) == 0:
                new.append([j])
            else:
                for i, case in enumerate(cases):
                    temp = copy.deepcopy(case)
                    temp.append(j);new.append(temp)
        cases = new

def gravity():
    """중력이 작용해서 블록이 아래로 내려가는 것을 구현하기 위해서는 아래부터 차례로, 0이 아닌 수가 나오면 temp배열에 옮겨 준다."""
    global board
    temp = [[0 for _ in range(4)] for _ in range(N+1)]
    for x in range(4):
        prev_idx = N
        for y in range(N, -1, -1):
            if board[y][x]:
                temp[prev_idx][x] = board[y][x]
                prev_idx -= 1

    for y in range(N+1):
        for x in range(4):
            board[y][x] = temp[y][x]

def check_row():
    global board, score
    for y in range(N+1):
        if board[y][0] and board[y][1] and board[y][2] and board[y][3]: ## 0이 아닌 수들에 대해서 ##
            board[y][0] = board[y][1] = board[y][2] = board[y][3] = 0 # 0으로 변경 해줌 #
            score += 1



## (1) 블럭이 떨어져서 제일 바닥으로 이동하는 상황 ##
def fall_block(block_idx, c):
    global board
    """블록의 번호와 떨어질 x좌표 위치를 입력으로 받는다."""
    did = False
    for y in range(N, -1, -1):
        if board[y][c] == 0:
            board[y][c] = block_idx # 아래에서 위로 올라가면서 비어 있는 부분에 넣어준다. #
            did = True
            break
    if did == False:
        return False

    check_row()
    gravity()
    return True

def in_range(x, y):
    return 0 <= x < 4 and 0 <= y <= N

## (2) 블럭이 각각의 방향의 우선순위에 맞게 이동하기 위한 방법 ##
def move_block():
    global board
    new_board = [[0 for _ in range(4)] for _ in range(N+1)]
    for y in range(N+1):
        for x in range(4):
            if board[y][x] == 0:
                continue
            moves = BLOCK_DICT[board[y][x]]
            for mv in moves:
                nx, ny = x + DX[mv], y + DY[mv]
                if in_range(nx, ny) == True:
                    if new_board[ny][nx] == 0:
                        new_board[ny][nx] = board[y][x]
                    else:
                        new_board[ny][nx] = min(board[y][x], new_board[ny][nx])
                    break
    for y in range(1+N):
        for x in range(4):
            board[y][x] = new_board[y][x]
    ## 중력 작용 ##
    gravity()
    check_row()
    gravity()



answer = 0
def simulate(case):
    global score
    score = 0
    for idx, c in enumerate(case):
        block_idx = block_order[idx] # 현재 블록 번호의 방향의 우선순위 배열 #
        ret = fall_block(block_idx, c-1)
        if ret == False:
            return 0
        move_block()
    return score

for case in cases:
    board = [[0 for _ in range(4)] for _ in range(N+1)] ## 배열을 반복해서 동일한 것을 사용하기 때문에 무조건 case하나 simulation이 끝난 다음에 초기화를 해 주어야 한다. ##
    score = simulate(case)
    answer = max(answer, score)
print(answer)


