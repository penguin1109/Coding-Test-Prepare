import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip())

# [출력] 기울어진 직사각형에서 최대의 합 #
# [풀이] 가로, 세로 조합에 대해서 탐색을 해도 될 듯 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

DIRS = [(1, -1), (-1, -1), (-1, 1), (1, 1)]
ANSWER = 0

def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)


def search(x, y, dir, sx, sy, cnt, track):
    global ANSWER
    if dir == 4:
        return
    # if (x == sx and y == sy and dir != 0):
    #     ANSWER = max(ANSWER, cnt)
    #     return
    """4방중 한방향으로 적어도 1번 이상은 움직여야 함"""
   
    nx, ny = x + DIRS[dir][0], y + DIRS[dir][1]
    if nx == sx and ny == sy:
        ANSWER = max(ANSWER, cnt)
        return
    if in_range(nx, ny) == True:
        track[dir] += 1
        search(nx, ny, dir, sx, sy, cnt+board[ny][nx], track)
        track[dir] -= 1
        if track[dir] > 0:
            search(nx, ny, dir+1, sx, sy, cnt+board[ny][nx], track)
    else:
        if track[dir] > 0:
            search(x, y, dir+1, sx, sy, cnt, track)

for y in range(N):
    for x in range(N):
        track = [0 for _ in range(4)]
        search(x, y, 0, x, y, board[y][x], track)
print(ANSWER)
        