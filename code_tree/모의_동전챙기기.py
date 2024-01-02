import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 크기 #
board = []
sx,sy=-1, -1
ex,ey = -1, -1
numbers = []
for y in range(N):
    arr = str(readl().strip())
    temp = []
    for x, a in enumerate(arr):
        if a == '.':temp.append(0)
        elif a == '#':temp.append(-1)
        elif a == 'E':
            ex, ey = x, y
            temp.append(-10) # 도착점 #
        elif a == 'S':
            sx, sy = x, y
            temp.append(-11) # 시작점 #
        else:
            numbers.append([int(a), x, y])
            temp.append(int(a))
    board.append(temp)

from collections import deque
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N
tot_nums = len(numbers)
numbers.sort(key = lambda x : x[0])
combinations = []
def dfs(prev_n, temp):
    global combinations
    import copy
    if len(temp) == 3:
        combinations.append(temp)
        return
    if prev_n >= tot_nums:
        return
    dfs(prev_n+1, temp)
    new = copy.deepcopy(temp)
    new.append(prev_n)
    dfs(prev_n+1, new)

dfs(0, [])

MIN_DIST = float("INF")
def bfs(x1,y1, x2, y2):
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    q = deque([[x1, y1, 0]])
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[y1][x1] = True

    while q:
        x, y, d = q.popleft()
        if x == x2 and y == y2:
            return d
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) == False:
                continue
            if board[ny][nx] == -1:
                continue
            if visited[ny][nx] == True:
                continue
            visited[ny][nx] = True
            q.append([nx, ny, d+1])
    return -1
for comb in combinations:
    x1, y1 = sx, sy
    temp = 0;valid = True
    for i in comb:
        x, y = numbers[i][1:]
        dist = bfs(x1, y1, x, y)
        if dist == -1:
            valid = False
            break
        temp += dist
        if temp > MIN_DIST:
            valid = False
            break
        x1, y1 = x, y
    if valid:
        dist = bfs(x1, y1, ex, ey)
        if dist != -1:
            temp += dist
            MIN_DIST = min(MIN_DIST, temp)
if MIN_DIST == float("INF"):
    print(-1)
else:
    print(MIN_DIST)



