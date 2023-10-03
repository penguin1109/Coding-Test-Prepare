## 13460-구슬 탈출 2 문제에서 시간 단축을 할 수 있는 방법
from collections import deque

DX, DY = [0, 1, 0, -1], [-1, 0, 1, 0]
N, M = map(int, input().strip().split(' ')) # 세로, 가로
board = []

for n in range(N):
    arr = str(input())
    arr = [str(x) for x in arr]
    for m in range(M):
        if arr[m] == 'R':
            a, b = n, m
        elif arr[m] == 'B':
            c, d=  n, m
    board.append(arr)

visited = [[[[False for _ in range(M)] for _ in range(N)] for _ in range(M)] for _ in range(N)]

dQ = deque()
dQ.append((a, b, c, d, 1)) # red_y, red_x, blue_y, blue_x, time
visited[a][b][c][d] = True

def move(x, y, i):
    dx, dy = DX[i], DY[i]
    count = 0
    while board[x + dx][y + dy] != '#' and board[x][y] != 'O': # 이미 구멍에 들어간 구슬이면 더이상 이동이 어렵다.
        # 만약 board[x + dx][y + dy] != 'O'이었다면
        x, y = x + dx, y + dy
        count += 1
    return x, y, count

def bfs():
    while dQ:
        a, b, c, d, time = dQ.popleft()
        if time > 10:
            break
        for i in range(4):
            na, nb, red_cnt = move(a, b, i)
            nc, nd, blue_cnt = move(c, d, i)
            if board[na][nb] == 'O' and board[nc][nd] != 'O': # 빨간공만 구멍에 들어가고 파란 공은 구멍에 들어가지 않은 경우
                return time
            if board[nc][nd] != 'O':
                if na == nc and nb == nd:
                    if red_cnt > blue_cnt:
                        na -= DX[i]; nb -= DY[i]
                    else:
                        nc -= DX[i]; nd  -= DY[i];
                if visited[na][nb][nc][nd] == False:
                    visited[na][nb][nc][nd] = True
                    dQ.append((na, nb, nc, nd, time+1))

    return -1
print(bfs())


