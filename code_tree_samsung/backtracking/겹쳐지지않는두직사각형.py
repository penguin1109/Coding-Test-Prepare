import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' ')) 

board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

# [출력] 두 직사각형을 잡아서 안에 적힌 숫자들의 합을 최대로 할때의 최대합 #
ANSWER = -float("INF")
add = 0
def check_overlap(x, y, x1, y1, x2, y2, x3, y3):
    global add
    add = 0
    visited = [[0 for _ in range(M)] for _ in range(N)]
    for j in range(x, x1+1):
        for i in range(y, y1+1):
            visited[i][j] += 1
            add += board[i][j]
    for j in range(x2, x3+1):
        for i in range(y2, y3+1):
            if visited[i][j] == 1:
                return True
            visited[i][j] += 1
            add += board[i][j]
    return False
def update_max_sum(x, y, x1, y1):
    global ANSWER
    for y2 in range(N):
        for x2 in range(M):
            for y3 in range(y2, N):
                for x3 in range(x2, M):
                    if check_overlap(x,y,x1, y1, x2,y2,x3,y3) == False:
                        ANSWER = max(ANSWER, add)
                        
                        
                    
def get_single_rect():
    for y in range(N):
        for x in range(M):
            for y1 in range(y, N):
                for x1 in range(x, M):
                    update_max_sum(x, y, x1, y1)


get_single_rect()
print(ANSWER)