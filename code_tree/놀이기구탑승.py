import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N = int(readl().strip()) # 격자의 크기 #
# favor = [list(map(int, readl().strip().split(' '))) for _ in range(N*N)] # 각 학생이 좋아하는 학생의 번호 #
favor = {}
orders = []
for i in range(N*N):
    arr = list(map(int, readl().strip().split(' ')))
    arr = [a-1 for a in arr]
    favor[arr[0]] = arr[1:] # 각 학생의 번호마다 좋아하는 학생 4명의 번호를 저장 #
    orders.append(arr[0])

board = [[-1 for _ in range(N)] for _ in range(N)]
import heapq
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N
def select_place(idx):
    global board
    q = []
    for y in range(N):
        for x in range(N):
            empty = 0;fav = 0
            if board[y][x] == -1: # 비어 있는 자리인 경우에 #
                for dx, dy in zip(DX, DY):
                    nx, ny = x + dx, y + dy
                    if in_range(nx, ny) == False:
                        continue
                    if board[ny][nx] == -1:
                        empty += 1
                    elif board[ny][nx] in favor[idx]:
                        fav += 1
                heapq.heappush(q, [-fav, -empty, y, x])
    temp = heapq.heappop(q)
    x, y = temp[3], temp[2]
    board[y][x] = idx

def count_fav():
    answer = 0
    for y in range(N):
        for x in range(N):
            if board[y][x] == -1:
                continue

            idx = board[y][x]
            temp = 0
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) == True:
                    if board[ny][nx] in favor[idx]:
                        temp += 1
            if temp > 0:
                answer += 10 ** (temp-1)
    return answer

for order in orders:
    select_place(order)
answer = count_fav()
print(answer)

