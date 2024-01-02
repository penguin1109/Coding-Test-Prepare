import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 크기 #
board = [[0 for _ in range(N)] for _ in range(N)]
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

for y in range(N):
    arr = str(readl().strip())
    for x in range(N):
        if arr[x] == '#':
            board[y][x] = -1
        elif arr[x] == 'B':
            bx, by = x, y

answer = 0

def expand(sx, sy, turn):
    curs = [[sx, sy]]
    t = 0
    check = [[False for _ in range(N)] for _ in range(N)]
    check[sy][sx] = True
    while True:
        if t == turn:
            break
        new = []
        for x, y in curs:
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) == False:
                    return False
                if board[ny][nx] == -1:
                    return False
                if check[ny][nx] == True:
                    continue

                check[ny][nx] = True
                new.append([nx, ny])
        curs = new
        t += 1

    return True


def dfs(x, y, turns):
    global answer
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy
        if in_range(nx, ny) == False:
            continue
        if board[ny][nx] == -1:
            continue
        ret = expand(nx, ny, turns+1) # 현재의 turn으로 이동이 가능한건지 확인하기 #
        if ret:
            answer = max(answer, turns+1)
            dfs(nx, ny, turns+1)


# visited = [[False for _ in range(N)] for _ in range(N)]
# visited[sy][sx] = True
dfs(bx, by, 0)

print(answer+1)