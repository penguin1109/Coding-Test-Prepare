""" 13460
구슬 탈출 2
[문제 설명]
- 직사각형 보드에 빨간 구슬과 파란 구슬을 하나씩 넣은 다음, 빨간 구슬을 구멍을 통해 꺼내는 게임이다.
- 세로 N 가로 M의 크기의 보드이고, 빨간 구슬을 구멍을 통해서 빼냄과 동시에 파란 구슬을 구멍에 들어가지 않게 하는게 목적이다.
- 공은 **중력을 사용해서** 굴려야 한다.
- 빨간 공과 파란 공은 동시에 움직인다.
- 두 공은 같은 칸에 동시에 있을 수 없다.
- 더 이상 두 공 모두 움직일 수 없을 때에 이동을 멈추고 -1을 출력한다.

[실패 조건]
1. 파란 구슬이 구멍에 빠지는 경우
2. 빨간 구슬과 파란 구슬이 구멍에 동시에 빠지는 경우

[입력]
벽: #
구멍: O

[출력]
최소 몇 번 만에 빨간 구슬을 구멍을 통해 빼낼 수 있는가?
단, 이동 횟수가 10번이 넘으면 멈추어야 한다.
"""
DX, DY = [0, 1, 0, -1], [-1, 0, 1, 0] # 위-오-아-왼
red, blue = [-1, -1], [-1, -1] # (x, y)

def check_movable(x, y):
    global board
    return board[y][x] == 'O' or board[y][x] == '#'

MIN_TIME = 1e+9

N,M = map(int, input().strip().split(' ')) # 세로, 가로
board = []
for n in range(N):
    arr = str(input())
    arr = [str(x) for x in arr]
    for m in range(M):
        if arr[m] == 'R':
            red[0] = m; red[1] = n;
            arr[m] = '.'
        elif arr[m] == 'B':
            blue[0] = m;blue[1] = n;
            arr[m] = '.' # 계속 board를 업데이트 시키는 것이 귀찮으니까 R,B 공이 있는 곳에는 빈칸으로 바꾸어 준다.

    board.append(arr)
def update_red(x, y):
    # board[y][x] = 'R'
    # board[red[0]][red[1]] = '.'
    red[0] = y
    red[1] = x

def update_blue(x, y):
    # board[y][x] = 'B'
    # board[blue[0]][blue[1]] = '.'
    blue[0] = y
    blue[1] = x

# 결국에 기울여서 중력에 의해서 움직이게 하는 것이라면 움직일 수 없을 때까지 구슬을 굴리게 될 것이다.
def move(x, y, dir, board):
    dx, dy = DX[dir], DY[dir]
    new_x, new_y = x, y
    moved = 0
    while True:
        if (0 < new_x + dx < M) and (0 < new_y + dy < N): # 범위 내에 존재하는 경우에
            if board[new_y + dy][new_x + dx] == 'O': # 빈 칸에 들어가는 경우에
                moved += 1
                return new_x + dx, new_y + dy, True, moved
            elif board[new_y + dy][new_x + dx] == '#':
                return new_x, new_y, False, moved
            elif board[new_y + dy][new_x + dx] == '.': # 빈 칸인 경우에는 당연히 움직임이 가능하다.
                moved += 1
                new_x += dx
                new_y += dy
        else:
            return new_x, new_y, False, moved
    return new_x, new_y, False, moved

def simulate(R, B, time):
    global MIN_TIME
    if time > 10:
        return -1
    for i in range(4):
        new_r_x, new_r_y, red_hole, red_moved = move(R[0], R[1], i, board)
        new_b_x, new_b_y, blue_hole, blue_moved = move(B[0], B[1], i, board)
        new_red = [new_r_x, new_r_y]
        new_blue = [new_b_x, new_b_y]
        if red_moved == 0 and blue_moved == 0: # 더이상 빨간 공과 파란 공이 움직일 수 없는 경우에는 게임을 멈춤
            continue

        if red_hole == True and blue_hole == True:
            continue

        if new_red == new_blue:
            if red_moved > blue_moved:
                new_red[0] -= DX[i]
                new_red[1] -= DY[i]
            else:
                new_blue[0] -= DX[i]
                new_blue[1] -= DY[i]

        if red_hole:
            MIN_TIME = min(MIN_TIME, time)
            return
        elif blue_hole:
            continue
        else:
            simulate(new_red, new_blue, time + 1)

simulate(red, blue, 1)

if MIN_TIME != 1e+9:
    print(MIN_TIME)
else:
    print(-1)







