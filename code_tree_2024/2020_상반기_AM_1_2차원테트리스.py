import sys
input = sys.stdin.readline

'''
- 한 행이나 열이 가득 차서 지워질 때 각각의 행/열의 개수마다 1점씩 얻는다.

[출력]
(1) 수행이 끝난뒤 얻은 점수
(2) 빨간색 보드와 노란색 보드에 남은 블록이 차지하는 칸의 수의 합
'''
K = int(input().strip()) # 블록을 입력한 횟수 #
red_board = [[0 for _ in range(4)] for _ in range(6)]
yellow_board = [[0 for _ in range(4)] for _ in range(6)]

score = 0

def remove_soft():
    global red_board, yellow_board
    for y in range(1, -1, -1):
        if sum(red_board[y]) != 0:
            del red_board[-1]
        if sum(yellow_board[y]) != 0:
            del yellow_board[-1]
    red_board = [[0 for _ in range(4)] for _ in range(6-len(red_board))] + red_board
    yellow_board = [[0 for _ in range(4)] for _ in range(6-len(yellow_board))] + yellow_board
    
def get_final_block():
    red_cnt = sum([sum(a) for a in red_board])
    yellow_cnt = sum([sum(a) for a in yellow_board])
    
    return red_cnt + yellow_cnt

def update_score():
    global score, red_board, yellow_board
    for y in range(6):
        if sum(yellow_board[y]) == 4:
            score += 1
            del yellow_board[y]
            yellow_board = [[0 for _ in range(4)]] + yellow_board
        if sum(red_board[y]) == 4:
            score += 1
            del red_board[y]
            red_board = [[0 for _ in range(4)]] + red_board
    
    
def move_type2(x, y):
    global red_board, yellow_board
    stop_y = None
    for yy in range(1, 6):
        # if yellow_board[yy][x] == 0 and yellow_board[yy][x+1] == 0:
        if yellow_board[yy][x] == 1 or yellow_board[yy][x+1] == 1:
            # 둘다 비어 있을 때 멈춰서 채워 넣어줌 #
            stop_y = yy-1
            # (1) 멈춘 위치가 0 또는 1, 즉 연한 부분인 경우 #
            # if stop_y == 0 or stop_y == 1:
            #     yellow_board[stop_y][x] = 1;yellow_board[stop_y][x+1] = 1
            #     del yellow_board[(stop_y-2):]
            #     yellow_board = [[0 for _ in range(4)] for _ in range(-(stop_y-2))] + yellow_board
            # # (2) 멈춘 위치가 0 또는 1이 아닌 경우 #
            # else:
            yellow_board[stop_y][x] = 1;yellow_board[stop_y][x+1] = 1
            break
    if stop_y is None:
        yellow_board[-1][x] = 1;yellow_board[-1][x+1] = 1
    stop_y = None
    for yy in range(2, 6, 1):
        # if red_board[yy][3-y] == 0 and red_board[yy+1][3-y] == 0:
        if red_board[yy][3-y] == 1:
            stop_y = yy-2
            # print("type 2 stop Y : ", stop_y)
            # if stop_y == 1:
            #     red_board[stop_y][3-y] = 1;red_board[stop_y-1][3-y] = 1
            #     del red_board[(stop_y-2):]
            #     red_board = [[0 for _ in range(4)] for _ in range(-(stop_y-2))] + red_board
            # else:
            red_board[stop_y][3-y] = 1;red_board[stop_y+1][3-y] = 1
            break
    if stop_y is None:
        red_board[-1][3-y] = 1;red_board[-2][3-y] = 1
          
def move_type3(x, y):
    global red_board, yellow_board
    stop_y = None
    for yy in range(1, 6):
        if red_board[yy][3-y] == 1 or red_board[yy][3-y-1] == 1:
            stop_y = yy-1
        # if red_board[yy][3-y] == 0 and red_board[yy][3-y-1] == 0:
            # 둘다 비어 있을 때 멈춰서 채워 넣어줌 #
            # stop_y = yy
            # (1) 멈춘 위치가 0 또는 1, 즉 연한 부분인 경우 #
            # if stop_y == 0 or stop_y == 1:
            #     red_board[stop_y][3-y] = 1;red_board[stop_y][3-y-1] = 1
            #     del red_board[(stop_y-2):]
            #     red_board = [[0 for _ in range(4)] for _ in range(-(stop_y-2))] + red_board
            # # (2) 멈춘 위치가 0 또는 1이 아닌 경우 #
            # else:
            red_board[stop_y][3-y] = 1;red_board[stop_y][3-y-1] = 1
            break
    if stop_y is None:
        red_board[-1][3-y] = 1;red_board[-1][3-y-1] = 1
        
    stop_y = None
    for yy in range(2, 6, 1):
        # if yellow_board[yy][x] == 0 and yellow_board[yy+1][x] == 0:
        if yellow_board[yy][x] == 1: #  or yellow_board[yy+1][x] == 1:
            stop_y = yy-2
            # if stop_y == 1:
            #     yellow_board[stop_y][x] = 1;yellow_board[stop_y-1][x] = 1
            #     del yellow_board[(stop_y-2):]
            #     yellow_board = [[0 for _ in range(4)] for _ in range(-(stop_y-2))] + yellow_board
            # else:
            yellow_board[stop_y][x] = 1;yellow_board[stop_y+1][x] = 1
            break        
    if stop_y is None:
        yellow_board[-1][x] = 1;yellow_board[-2][x] = 1
        
def move_type1(x, y):
    global red_board, yellow_board
    stop_y = None
    for yy in range(1, 6):
        # if red_board[yy][3-y] == 0:
        if red_board[yy][3-y] == 1:
            stop_y = yy-1
            # if stop_y == 0 or stop_y == 1:
            #     red_board[stop_y][3-y] = 1
            #     del red_board[-1]
            #     red_board = [[0 for _ in range(4)]] + red_board
            # else:
            red_board[stop_y][3-y] = 1
            break
    if stop_y is None:
        red_board[-1][3-y] = 1
    stop_y = None
    for yy in range(1, 6):
        # if yellow_board[yy][x] == 0:
        if yellow_board[yy][x] == 1:
            stop_y = yy-1
            # print(f"type 1 : {stop_y}")
            # if stop_y == 0 or stop_y == 1:
            #     yellow_board[stop_y][y] = 1
            #     del yellow_board[-1]
            #     yellow_board = [[0 for _ in range(4)]] + yellow_board
            # else:
            yellow_board[stop_y][x] = 1
            break
    if stop_y is None:
        yellow_board[-1][x] = 1
for k in range(K):
    t, y, x = map(int, input().strip().split(' ')) # 블록의 종류, 블록의 위치 #
    if t == 2:
        move_type2(x, y)
    elif t == 3:
        move_type3(x, y)
    elif t == 1:
        move_type1(x, y)
    # print("YELLOW ", yellow_board)
    # print("RED ", red_board)
    # print("=" * 30)
    update_score()
    remove_soft()

print(score)
print(get_final_block())