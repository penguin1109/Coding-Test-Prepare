import sys
sys.stdin = open('./input.txt', 'r')

readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' '))
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

ANSWER = 0

def update_sum(x, y, x1, y1):
    temp = 0
    global ANSWER
    for Y in range(y, y1+1):
        for X in range(x, x1+1):
            if board[Y][X] <= 0:
                return 
            temp += 1
    ANSWER = max(ANSWER, temp)
    return 

for y in range(N):
    for x in range(M):
        for y1 in range(y, N):
            for x1 in range(x, M):
                update_sum(x, y, x1, y1)

if ANSWER == 0:
    print(-1)
else:
    print(ANSWER)