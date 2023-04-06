""" 나무박멸
<조건>
nxn 격자에 나무의 그루 수와 벽의 정보가 주어진다.
제초제: k의 범위만큼 대각선으로 퍼지며, 벽이 있으면 가로막혀서 전파되지 못함

<순서>
1. 인접한 4개의 칸 중 나무가 있는 칸의 수만큼 나무 성장. 모든 나무가 **동시**에 성장
2. 기존에 있던 나무들은 인접한 4개의 칸 중 <벽, 다른 나무, 제초제가 없는> 칸에 **동시에** 번식한다.
    각 칸의 나무 그루 수 // 총 번식이 가능한 수
    이때 각 칸의 나무 그루 수는 (1)번에서 성장을 한 이후의 개수이다.
3. 전체 칸 중에서 나무가 가장 많이 박멸되는 칸에 제초제를 뿌림
    나무가 있는 칸에 뿌려야만 4 대각선으로 k칸만큼 전파가 된다.
    전파 도중 <벽이 있거나> <나무가 아얘 없는> 칸까지만 뿌려진다.
    제초제가 뿌려진 곳에 다시 뿌려지면 새로 뿌려진 해로부터 다시 c년간 유지된다.
    한번 뿌린 칸에는 c년만큼 남아 있고, c+1년째에 사라진다.

<문제>
m년동안 총 박멸한 나무의 수의 합을 구하여라.
"""

N, M, K, C = map(int, input().strip().split(' '))  # 격자의 크기, 박멸이 진행되는 햇수, 제초제 확산 범위, 제초제가 남아있는 햇수

board = []
death = [[0 for _ in range(N)] for _ in range(N)]

for n in range(N):
    # 벽: -1 | 빈칸: 0 | 나무 그루 수
    board.append(list(map(int, input().strip().split(' '))))


def check_tree_spreadable(x, y):
    # 나무가 해당 칸에 번식이 가능한지 확인한다
    return death[x][y] == 0 and board[x][y] == 0


def check_range(x, y):
    return (0 <= x < N and 0 <= y < N)


def check_death_stop(x, y):
    # 이게 True가 나오면 더이상 제초제가 확산이 될수 없음을 의미한다.
    return board[x][y] == -1 or board[x][y] == 0


def tree_growth():
    global board

    DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]
    new_growth = [[0 for _ in range(N)] for _ in range(N)]
    ## STEP 1: 인접한 4칸에 있는 나무의 개수만큼 동시에 성장
    ## STEP 2: 기존에 있던 나무들은 인접한 4개의 칸중 조건을 만족하는 경우에 번식
    for i in range(N):
        for j in range(N):
            cnt = 0
            if board[i][j] <= 0:
                continue
            valid = []
            for dx, dy in zip(DX, DY):
                nx, ny = i + dx, j + dy
                if check_range(nx, ny) and board[nx][ny] > 0:  # 나무가 있는 칸의 수만큼 해당 칸의 나무 개수 증가
                    cnt += 1
                if check_range(nx, ny) and check_tree_spreadable(nx, ny):
                    valid.append([nx, ny])
            board[i][j] += cnt  # 동시에 성장
            if len(valid) == 0: # 주변에 번식이 가능한 경우가 없다.
                continue
            add_val = board[i][j] // len(valid)
            for pt in valid:
                x, y = pt
                new_growth[x][y] += add_val
    for i in range(N):
        for j in range(N):
            board[i][j] += new_growth[i][j]
    # print(board) -> 디버깅 결과를 보니 나무의 성장까지는 문제가 없다.


def calc_kill(x, y):
    global board
    DX, DY = [1, 1, -1, -1], [-1, 1, -1, 1]
    add = 0
    spreadable = []
    for dx, dy in zip(DX, DY):
        for k in range(1, K + 1):
            nx, ny = x + dx * k, y + dy * k
            if check_range(nx, ny) == False:
                break
            if check_death_stop(nx, ny) == True: # 여기까지만 뿌리고 멈춰야 한다.
                # 벽이 있거나 나무가 있는 경우에 멈추니까 add에는 더할 값이 없다.
                spreadable.append([nx, ny])
                break
            add += board[nx][ny]
            spreadable.append([nx, ny])
    spreadable.append([x,y])
    add += board[x][y]
    return add, spreadable


def spread_kill(spread_list):
    #DX, DY = [ 1, 1, -1, -1], [-1, 1, -1, 1]  # 4개의 대각선의 방향

    for i in range(N):
        for j in range(N):
            if death[i][j] > 0:
                death[i][j] -= 1
                # if death[i][j] == 0: # 제초제 유효 기간이 지났으면
                #     board[i][j] = 0 # 다시 board의 좌표값을 0, 즉 빈칸으로 바꿔 놓는다.

    for pt in spread_list:
        sx, sy = pt
        death[sx][sy] = C # 이미 이전에 뿌려서 번식 시간이 남아 있어도 번식이 가능하다.
        if board[sx][sy]  > 0:
            board[sx][sy] = 0
        # board[sx][sy] = -2 # -2는 제초제가 있음을 의미한다.


def find_most_kill():
    global board, death, K, C
    MAX_KILL = 0
    spread_x, spread_y = 0, 0
    spreadable = []

    for i in range(N):
        for j in range(N):
            if board[i][j] <= 0:
                continue
            kill_val, sp_list = calc_kill(i, j)
            if kill_val > MAX_KILL:
                MAX_KILL = kill_val
                spread_x, spread_y = i, j
                spreadable = sp_list

    spread_kill(spreadable)
    return MAX_KILL


def run():
    answer = 0
    for m in range(M):
        tree_growth()
        killed = find_most_kill()
        answer += killed
        # print(board)

    return answer


print(run())