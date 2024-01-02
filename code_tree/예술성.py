import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 한 칸의 크기 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def make_group(sx, sy, check, group_idx):
    n = board[sy][sx]
    from collections import deque, defaultdict

    q = deque([[sx, sy]])
    visited = [[False for _ in range(N)] for _ in range(N)]
    check[sy][sx] = group_idx
    visited[sy][sx] = True
    group_size = 0
    # near_dict = defaultdict(int)

    while q:
        x, y = q.popleft()
        group_size += 1
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) == False:
                continue
            if visited[ny][nx] == True:
                continue
            if board[ny][nx] == n:
                q.append([nx, ny])
                visited[ny][nx] = True
                check[ny][nx] = group_idx
            # else:
            #     near_dict[board[ny][nx]] += 1
    return group_size, check

def get_neighbors(group_info, check):
    near_arr = [[0 for _ in range(len(group_info))] for _ in range(len(group_info))]
    visited = [[False for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) == False:
                    continue
                if visited[ny][nx] == True:
                    continue
                visited[y][x] = True
                if check[ny][nx] != check[y][x]:
                    near_arr[check[y][x]][check[ny][nx]] += 1
                    near_arr[check[ny][nx]][check[y][x]] += 1
    return near_arr



def get_score():
    group_info = {}
    check = [[-1 for _ in range(N)] for _ in range(N)]
    group_idx = 0
    for y in range(N):
        for x in range(N):
            if check[y][x] == -1:
                group_size, check = make_group(x, y, check, group_idx)
                group_info[group_idx] = {'group_size': group_size, 'group_n': board[y][x]}
                group_idx += 1
                # print(check)
    near_arr = get_neighbors(group_info, check)
    # print(near_arr)
    score = 0
    for i in range(len(group_info)):
        for j in range(i+1, len(group_info)):
            temp = (group_info[i]['group_size'] + group_info[j]['group_size']) * group_info[i]['group_n'] * group_info[j]['group_n'] * near_arr[i][j]
            score += temp
    # print(f"SCORE : {score}")
    return score

def rotate_clock(x1, y1, x2, y2, s):
    global board
    # (1) 좌 상단의 좌표를 (0, 0)으로 바꿔 준다. #
    nx1, ny1 = 0, 0;nx2, ny2 = x2 - x1, y2-y1
    temp = [[0 for _ in range(s)] for _ in range(s)]
    for y in range(ny1, ny2):
        for x in range(nx1, nx2):
            nx, ny = s-y-1, x
            temp[ny][nx] = board[y+y1][x+x1]
    for y in range(y1, y2):
        for x in range(x1, x2):
            board[y][x] = temp[y-y1][x-x1]

def rotate_anticlock():
    global board
    import copy
    temp = copy.deepcopy(board)
    for x in range(N):
        nx, ny = N//2, N-x-1
        temp[ny][nx] = board[N//2][x]
    for y in range(N):
        nx, ny = y, N//2
        temp[ny][nx] = board[y][N//2]
    board = temp

def rotate_picture():
    global board
    mx, my = N//2, N//2;s = N//2
    ## (1) 4개의 정사각형을 개별적으로 시계로 90도 회전 ##
    rotate_clock(0, 0, mx, my, s)
    rotate_clock(mx+1,my+1, N,N, s)
    rotate_clock(0, my+1, mx, N, s)
    rotate_clock(mx+1, 0, N, my, s)

    ## (2) 십자 모양을 반시계로 90도 회전 ##
    rotate_anticlock()


def simulate():
    answer = 0
    answer += get_score() #  초기 예술 점수 #
    for i in range(3):
        rotate_picture()
        answer += get_score()
    return answer

answer = simulate()
print(answer)





