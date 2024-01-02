import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 크기 #
board = []
walls = []

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

for y in range(N):
    arr = str(readl().strip())
    temp = []
    for x in range(N):
        if arr[x] == '.': # 빈 칸 #
            temp.append(0)
        else: # 벽 #
            walls.append([x,y])
            temp.append(1)
    board.append(temp)

def simulate(combination):
    import copy
    from collections import deque
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    new_board = copy.deepcopy(board)

    for i in combination:
        wall = walls[i]
        new_board[wall[1]][wall[0]] = 0
    num_blank = N**2 - len(walls) + len(combination)
    # print(num_blank, len(combination))
    for y in range(N):
        do_break = False
        for x in range(N):
            if new_board[y][x] == 0:
                sx, sy = x, y;do_break=True
                break
        if do_break:break

    q = deque([[sx, sy]])
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True

    while q:
        x, y = q.popleft()
        num_blank -= 1
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) == False:
                continue
            if visited[ny][nx] == True:
                continue
            if new_board[ny][nx] == 1:
                continue
            q.append([nx, ny])
            visited[ny][nx] = True

    return num_blank == 0




def get_combinations(select_n, idx, temp):
    global combinations
    import copy
    if len(temp) == select_n:
        combinations.append(temp)
        return
    if idx >= len(walls):
        return
    get_combinations(select_n, idx+1, temp)
    new = copy.deepcopy(temp)
    new.append(idx)
    get_combinations(select_n, idx+1, new)


answer = -1
for remove_n in range(7):
    combinations = []
    get_combinations(remove_n, 0, [])

    for combination in combinations:
        res = simulate(combination)
        if res:
            answer = remove_n
            break
    if answer != -1:
        break

print(answer)

