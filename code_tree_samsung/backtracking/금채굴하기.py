import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' ')) 

board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

# [출력] 손해를 보지 않으면서 채굴 가능한 가장 많은 금의 개수 #

DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0]
MAX_GOLD = 0

def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)
"""
[1, 4, 8, 12]
"""
def update(gold, K):
    global MAX_GOLD
    cost = K**2 + (K+1)**2
    if cost <= gold * M:
        MAX_GOLD = max(MAX_GOLD, gold)
        
def search(x, y):
    global MAX_GOLD
    gold = 1 if board[y][x] == 1 else 0
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[y][x] = True
    temp = [[x, y]]
    K = 0;new = 4
    update(gold, K)
    while True:
        if len(temp) == 0:
            break
        new_temp = [];new_gold = 0
        for (sx, sy) in temp:
            for dx, dy in zip(DX, DY):
                nx, ny = sx + dx, sy + dy
                if in_range(nx, ny)==False:continue
                if visited[ny][nx]==True:continue
                visited[ny][nx] = True
                new_temp.append([nx, ny])
                new_gold += board[ny][nx]
        
        K += 1
        temp = new_temp
        new += 4
        gold += new_gold
        
        update(gold, K)
        
        
            
for y in range(N):
    for x in range(N):
        search(x, y)
print(MAX_GOLD)
        