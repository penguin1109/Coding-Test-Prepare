""" 17837. 새로운 게임 2
<문제 설명>
- NxN 크기의 판, 말의 개수는 K개
- 각 말은 위-아래-왼-오 의 4방향으로 이동
- 하나의 말 위에 다른 말을 올릴 수 있음
- 체스판의 각 칸은 흰색, 빨간색, 파란색 중 하나

<조건>
1. 한번의 턴에서 1~K 번 말이 순서대로 이동을 하고, 말이 4개 이상 쌓이면 게임이 종료된다.
2. if (흰색):제일 위에 올려 놓음
    elif (빨간색): 이동 후에 반대 순서로 올려놓음
    elif (파란색): 방향을 바꾸고 한칸 이동한 다음에 파란색이 아닌 경우에만 이동하고 아니면 원래 위치 그대로
    else: # 판 밖을 벗어나는 겅우 파란색과 동일하게 이동
3. 게임이 종료되는 턴의 벙호가 1000보다 크거나 게임이 종료될 수 없는 경우에는 -1을 출력

<주의>
- 처음부터 같은 칸에 말이 2개 이상 있는 경우는 없다.
- 무조건 말이 이돌 할 때는 위에 얹혀져 있는 말까지 함께 움직여야 한다.
"""
import sys
input = sys.stdin.readline

N, K = map(int, input().split(' '))## 판의 크기, 말의 개수
DX, DY = [1, -1, 0, 0], [0, 0, -1, 1]

board = [] ## 게임판의 색깔 정보를 저장하는 배열
marker_board = [[[] for _ in range(N)] for _ in range(N)] # [[] for _ in range(N**2)]
markers = [[] for _ in range(K)] ## 모든 알들의 좌표, 그리고 이동 방향을 기록한 배열

def get_idx(y, x):
    return (y,x)

for n in range(N):
    board.append(list(map(int, input().split(' ')))) ## 판의 정보 저장

for k in range(K):
    y, x, d = map(int, input().split(' ')) ## 행, 열, 이동방향
    markers[k] = [y-1, x-1, d-1] ## 이동하는 말의 정보를 저장
    marker_board[y-1][x-1].append(k)
    # marker_board[get_idx(y-1, x-1)].append(k)

def white(y, x, ny, nx, idx):
    # nx, ny = x + DX[d], y + DY[d]
    heap, tmp = [], -1
    while tmp != idx:
        tmp = marker_board[y][x].pop()
        heap.append(tmp)

    heap.reverse()
    marker_board[ny][nx].extend(heap)

    for i in heap:
        markers[i][0] = ny
        markers[i][1] = nx

    if len(marker_board[ny][nx]) >= 4:
        return True
    else:
        return False
def red(y, x,ny, nx,  idx):
    # nx, ny = x + DX[d], y + DY[d]
    heap, tmp = [], -1
    while tmp != idx:
        tmp = marker_board[y][x].pop()
        heap.append(tmp)

    ## pop()을 했기 때문에 이미 reverse되어 있는 상태이다.
    marker_board[ny][nx].extend(heap)

    for i in heap:
        markers[i][0] = ny
        markers[i][1] = nx

    if len(marker_board[ny][nx]) >= 4:
        return True
    else:
        return False
def inverse_dir(d):
    if d == 1:return 0
    elif d == 0:return 1
    elif d == 2:return 3
    elif d == 3:return 2
def blue(y, x, d, idx):
    nd = inverse_dir(d)
    nx, ny = x + DX[nd], y + DY[nd]

    if ny < 0 or nx < 0 or ny >= N or nx >= N or board[ny][nx] == 2: ## 범위 안 맞거나 파란색인 경우
        markers[idx] = [y, x, nd]
        return False ## 게임을 멈출 필요가 없는 상황
    else:
        heap, tmp = [], -1
        while tmp != idx:
            tmp = marker_board[y][x].pop()
            heap.append(tmp)

        if board[ny][nx]==0:
            heap.reverse()
        marker_board[ny][nx].extend(heap)

        for i in heap:
            if idx == i:
                markers[i] = [ny, nx,nd]
            else:
                markers[i] = [ny, nx, d]

        if len(marker_board[ny][nx]) >= 4:
            return True
        else:
            return False


def move(y, x, d, idx):
    nx, ny = x + DX[d], y + DY[d]
    ## 파란색 칸이거나 칸의 범위를 넘어갈 때
    if ny < 0 or nx < 0 or ny >= N or nx >= N or board[ny][nx] == 2:
        d = inverse_dir(d)
        markers[idx][-1] = d
        nx, ny = x + DX[d], y + DY[d]
    if ny < 0 or nx < 0 or ny >= N or nx >= N or board[ny][nx] == 2:
        return False
    if board[ny][nx] == 1: ## 빨간색일 때
        stop = red(y, x,  ny, nx, idx)
    elif board[ny][nx] == 0:
        stop = white(y, x, ny, nx, idx)
    else:
        print("NO!")
    return stop

def move_game(idx):
    y, x, d = markers[idx]
    nx, ny = x + DX[d], y + DY[d]

    ##  현재 돌이 파란색 칸에 있는 경우에, 방향을 바꿔서 파란색이 아닌 칸에 도달하면 그 위에 있는 돌들의
    # 방향은 바뀌어서는 ㅇ나된다.
    if 0 > nx or  0 > ny or N <= nx or N <=ny or board[ny][nx] == 2:
        d = inverse_dir(d)
        markers[idx][-1] = d
        nx, ny = x  + DX[d], y + DY[d]

    if 0 > nx or 0 > ny or N <= nx or N <= ny or board[ny][nx] == 2:
        return False

    stack, tmp = [], -1
    while tmp != idx:
        tmp = marker_board[y][x].pop()
        stack.append(tmp)

    if board[ny][nx] == 0: # WHITE
        stack.reverse()
    marker_board[ny][nx].extend(stack)

    for i in stack:
        markers[i][0] = ny
        markers[i][1] = nx

    if len(marker_board[ny][nx]) >= 4:
        return True

    return False


iter = 1
while iter <= 1000:
    # print(marker_board)
    for idx, value in enumerate(markers):
        y, x, d = value
        stop = move(y, x, d, idx)
        # stop = move_game(idx)

        if stop == True:
            # print(marker_board)
            print(iter)
            sys.exit()
    iter += 1

print(-1)

