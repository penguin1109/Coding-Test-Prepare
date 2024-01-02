import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline
# [출력] K초후, 혹은 모든 참가자가 미로를 탈출 했을 때 모든 참가자들의 이동 거리의 합과 출구 좌표 #

N, M, K = map(int, readl().strip().split(' ')) # 격자의 크기, 참가자의 수, 반복 횟수 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)] # 1~9까지의 값이면 벽이고, 숫자는 내구도를 의미한다. #
board = [[-1*i for i in arr] for arr in board] # 내구도의 값을 음수로 둬서 참가자의 인원수까지 같이 트래킹 할 수 있도록 한다. #
for m in range(M):
    y, x = map(int, readl().strip().split(' '))
    board[y-1][x-1] += 1 # 참가자의 인원수를 추가해 준다. #
exit_y, exit_x = map(int, readl().strip().split(' ')) # 출구는 -10으로 나타낸다. #
board[exit_y-1][exit_x-1] = -10
exit_y-=1;exit_x-=1 # 출구 좌표 1씩 빼주는 부분 빼놓지 말자 #

left_people = M

ALL_MOVE = 0 # 모든 참가자들의 이동 거리의 합 #

DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] # 상-하-좌-우 (상,하의 이동에 우선순위가 있음)
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

#### (1) 참가자 이동 ####
def find_close_place(x, y):
    """출구로부터 상하좌우로 한칸 이동해서 제일 가까운 위치를 찾아 준다."""
    cur_dist = abs(exit_x - x) + abs(exit_y - y) # 현재 머물러 있던 칸과 출구까지의 거리 #
    min_dist = cur_dist;min_x, min_y = -1, -1
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy
        # print(nx, ny)
        if in_range(nx, ny) == False: # 격자 밖을 벗어나는 경우에는 이동 불가능 #
            continue
        if -9 <= board[ny][nx] <= -1: # 벽이 있는 곳으로는 이동을 할 수 없다. #
            continue
        dist = abs(exit_x - nx) + abs(exit_y - ny)

        if dist < min_dist: # 원래 칸보다 출구로부터 가까워 진 경우 #
            # print(dist, cur_dist)
            min_dist = dist;
            min_x = nx;min_y = ny

    if min_dist == cur_dist:
        return x, y, float("INF")
    else:
        return min_x, min_y, min_dist


def move_people():
    global board, left_people, ALL_MOVE
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            if board[y][x] >= 1: # 사람이 존재하는 경우에 #
                nx, ny, dist = find_close_place(x, y)
                if dist != float("INF"):
                    ALL_MOVE += board[y][x] # 참가자가 이동한 거리 업데이트 #
                if nx == exit_x and ny == exit_y: # 참가자가 이동하다가 출구에 도달한 경우 #
                    left_people -= board[y][x]
                    new_board[ny][nx] = -10
                else:
                    new_board[ny][nx] += board[y][x] # 참가자의 인원수를 업데이트 해 줌 -> 근데 여기서 실수를 했던 부분이 board[y][x]로 값을 바꾸는게 아니라, 다른 위치의 참가자도 이동하면서 여기 도달할 수 있기 때문에 더해 주었어야 했다 ##
            elif board[y][x] < 0:
                new_board[y][x] = board[y][x]
    return new_board


##### (2) 미로 회전 ######
def make_square(x, y):
    temp_dx = abs(exit_x - x)+1;temp_dy = abs(exit_y - y)+1 # 현재 출구까지의 가로, 세로 길이 #
    square_info = [-1, -1, -1]

    if temp_dx > temp_dy: # 가로가 세로보다 긴 경우에 #
        square_size = temp_dx # 세로 길이를 사각형의 크기로 선택 #
        # 세로 길이가 모자라기 때문에 위, 아래로 늘려준다. 우선 위로 늘릴 수 있을 때까지 #
        left_size = square_size - temp_dy # 늘려 주어야 하는 길이 #
        sy = min(y, exit_y);ey = max(y, exit_y)
        while left_size:
            for i in range(sy-1, -1, -1):
                if left_size == 0:break
                sy -= 1
                left_size -= 1
                if left_size == 0:break
            for i in range(ey+1, N):
                if left_size ==0:break
                ey += 1
                left_size -= 1
                if left_size == 0:break
            if left_size > 0: # 해당 크기의 정사각형을 만들 수 없는 경우에 #
                return square_info
            if left_size == 0:break
        square_info[0] = min(x, exit_x)
        square_info[1] = sy
        square_info[2] = square_size

    elif temp_dx < temp_dy: # 세로가 가로보다 긴 경우에 #
        square_size = temp_dy
        left_size = square_size - temp_dx # 좌우로 늘려줄 수 있는 길이 #
        sx = min(x, exit_x);ex = max(x, exit_x)
        while left_size:
            for i in range(sx-1, -1, -1):
                if left_size == 0:break
                sx -= 1;left_size -= 1
            for i in range(ex + 1, N):
                if left_size == 0:break
                ex += 1
                left_size -= 1
            if left_size > 0:
                return square_info
            if left_size == 0:
                break
        square_info[0] = sx
        square_info[1] = min(y, exit_y)
        square_info[2] = square_size

    else: # 둘이 같은 길이인 경우에 #
        square_info[0] = min(x, exit_x);square_info[1] = min(y, exit_y);square_info[2] = temp_dx
    # print(x, y, square_info, temp_dx, temp_dy)
    return square_info




def rotate_square(sx,sy, size):
    global board, exit_x, exit_y
    import copy
    new_board =  copy.deepcopy(board)
    for y in range(size):
        for x in range(size):
            org_x, org_y = x + sx, y + sy
            nx, ny = size-y-1, x
            if -9 <= board[org_y][org_x] <= -1:
                new_board[ny+sy][nx+sx] = board[org_y][org_x] + 1 # 벽은 회전하면서 내구도가 1씩 감소, 음수로 처리하기 때문에 1을 더해줌 #
            elif board[org_y][org_x] > 0:
                new_board[ny+sy][nx+sx] = board[org_y][org_x]
            elif board[org_y][org_x] == 0:
                new_board[ny+sy][nx+sx] = 0
            elif board[org_y][org_x] == -10:
                exit_x, exit_y = nx+sx, ny+sy
                new_board[exit_y][exit_x] = -10
            # print(x+sx, y+sy, nx+sx, ny+sy)
            # print(new_board)
    # print(f"SPINNED : {new_board}")
    return new_board


def get_min_size():
    min_size = 1000000
    for y in range(N):
        for x in range(N):
            if board[y][x] >= 1:
                size = max(abs(exit_x-x), abs(exit_y-y))
                if min_size > size:
                    min_size = size
    return min_size
def spin_maze():
    global board
    squares = []
    # for y in range(N):
    #     for x in range(N):
    #         if board[y][x] >= 1: # 한명 이상의 참가자가 존재하는 경우 #
    #             square_info = make_square(x, y)
    #             if square_info == [-1, -1, -1]:
    #                 continue
    #             squares.append(square_info)
    min_size = get_min_size()
    # print(f"SQUARE SIZE : {min_size}")
    min_x, min_y = -1, -1
    for y in range(N-min_size):
        for x in range(N-min_size):
            is_exit = False;is_player=False
            for i in range(y, y+min_size+1):
                for j in range(x, x+min_size+1):
                    if board[i][j] >= 1:
                        is_player=True
                    if board[i][j] == -10:
                        is_exit = True
            if is_exit and is_player:
                min_x, min_y = x, y
                break
        if min_x != -1:
            break
    # print(min_x, min_y, min_size)
    # squares.sort(key = lambda x : (x[2], x[1], x[0]))
    # if squares:
    #     min_square = squares[0]
    #     # print(f"MIN SQUARE : {min_square}")
    #     board = rotate_square(min_square[0], min_square[1], min_square[2])
    if min_x == -1:
        return
    board = rotate_square(min_x, min_y, min_size+1)









# print(board)
for k in range(K):
    if left_people == 0:
        break
    board = move_people()
    # print(f"MOVED: {k+1} -> ", board)
    if left_people == 0:
        break
    spin_maze()
    # if left_people == 0:
    #     break
    # print(board)
    # break
    # print(exit_x, exit_y)
    # print(ALL_MOVE)
print(f"{ALL_MOVE}")
print(f"{exit_y+1} {exit_x+1}")


