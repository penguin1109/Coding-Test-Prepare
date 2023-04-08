""" 120100. 2048 (Easy)
- 게임에서 한 번의 이동 = 보드 위의 전체 블록을 상하좌우 4방향 중 하나로 이동시키는 것
- 같은 값을 갖는 두 블록이 충돌하면 하나로 합쳐지게 된다.
- 똑같은 수가 3개 있는 경우에는 이동하려고 하는 쪽의 칸이 먼저 합쳐진다.
- 한 번의 이동에서 이미 합쳐진 블록은 또 다른 블록과 합쳐질 수 없다.

<조건>
- 정사각형의 board이기 때문에 가로와 세로의 길이가 동일하다.
- 0은 빈칸, 이외의 값은 모두 블록을 나타낸다.
- 2 <= 블록의 수 <= 1024

<출력>
- 최대 5번 이동시켜 얻을 수 있는 가장 큰 블록을 출력하여라.

<풀이 방법>
1. 상-하-좌-우의 원소들을 사용해서 길이가 5인 중복 순열을 구해야 한다.
"""
import sys
input = sys.stdin.readline

N = int(input()) # 보드의 크기

answer = 0 # 최종적으로 제일 큰 타일의 값
init_board = []
move_board = []
for n in range(N):
    arr = list(map(int, input().split(' ')))
    init_board.append(arr)
    move_board.append(arr)

DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]

def init():
    # 움직이는 보드를 초기 입력 상태로 초기화 한다.
    for i in range(N):
        move_board[i] = init_board[i]

def move_left():
    for i in range(N): # 위 -> 아래 탐색
        ptr = 0
        for j in range(1, N):
            if move_board[i][j] > 0:
                tmp = move_board[i][j]
                move_board[i][j] = 0
                if move_board[i][ptr] == tmp:
                    move_board[i][ptr] *= 2
                    ptr += 1
                elif move_board[i][ptr] == 0:
                    move_board[i][ptr] = tmp
                else:
                    ptr += 1
                    move_board[i][ptr] = tmp
def move_right():
    for i in range(N):
        ptr = N-1
        for j in range(N-2, -1, -1):
            if move_board[i][j] > 0:
                tmp = move_board[i][j]
                move_board[i][j] = 0
                if move_board[i][ptr] == tmp:
                    move_board[i][ptr] *= 2
                    ptr -= 1
                elif move_board[i][ptr] == 0:
                    move_board[i][ptr] = tmp
                else:
                    ptr -= 1
                    move_board[i][ptr] = tmp


def rotate_counter_90():
    global move_board
    rotated = []
    for i in range(N-1, -1, -1):
        temp = []
        for j in range(N):
            temp.append(move_board[j][i])
        rotated.append(temp)
    move_board = rotated

def rotate_90():
    global move_board
    rotated = []
    for i in range(N):
        temp = []
        for j in range(N-1, -1, -1):
            temp.append(move_board[j][i])
        rotated.append(temp)
    move_board = rotated


def move_up():
    for i in range(N): # 위 -> 아래 탐색
        ptr = 0
        for j in range(1, N):
            if move_board[j][i] > 0:
                tmp = move_board[j][i]
                move_board[j][i] = 0
                if move_board[ptr][i] == tmp:
                    move_board[ptr][i] *= 2
                    ptr += 1
                elif move_board[ptr][i] == 0:
                    move_board[ptr][i] = tmp
                else:
                    ptr += 1
                    move_board[ptr][i] = tmp

def move_down():
    for i in range(N):
        ptr = N-1
        for j in range(N-2, -1, -1):
            if move_board[j][i] > 0:
                tmp = move_board[j][i]
                move_board[j][i] = 0
                if move_board[ptr][i] == tmp:
                    move_board[ptr][i] *= 2
                    ptr -= 1
                elif move_board[ptr][i] == 0:
                    move_board[ptr][i] = tmp
                else:
                    ptr -= 1
                    move_board[ptr][i] = tmp


## 만들어 놓은 이동 경로대로 이동하기
def move(movement):
    init()
    global answer
    for i in movement:
        if i == '0':
            move_up()
        elif i == '1':
            move_down()
        elif i == '2':
            move_left()
        else:
            move_right()
    answer = max(answer, max([max(a) for a in move_board]))

from collections import deque
movements = deque(['0', '1', '2', '3'])

## 가능한 모든 이동 경로 만들기 => 이렇게 이동 경로를 만드는 것이 잘못 되었다는 뜻이 된다.
# 이유가 무엇일까?? 
while True:
    a = movements.popleft()
    if len(a) == 5:
        movements.append(a)
        break
    for j in range(4):
        movements.append(a + str(j))

while movements:
    movement = movements.popleft()
    move(movement)
print(answer)
