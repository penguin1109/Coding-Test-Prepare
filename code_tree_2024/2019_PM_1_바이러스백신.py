import sys
from itertools import combinations
import math

input = sys.stdin.readline
''' M개의 병원을 적당히 골라 바이러스를 전부 없애는데 걸리는 최소 시간을 구하여라.
골라진 병원을 시작으로 매 초 상하좌우 인접한 지역중 벽을 제외한 지역에 백신이 공급되어 바이러스가 사라짐.
바이러스를 없앨 수 있는 방법이 없으면 -1 출
'''
N, M = map(int, input().strip().split(' ')) 
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
board = []
hosp = []

def check_range(x, y):
    return 0 <= x < N and 0 <= y < N

def simulate(hospitals, board):
    import heapq
    q = [[0, a[0], a[1]] for a in hospitals]
    # print(q)
    visited = [[False for _ in range(N)] for _ in range(N)]
    ret = 0
    time_arr = [[0 for _ in range(N)] for _ in range(N)]
    moved = 0
    while q:
        # print(q)
        time, x, y = heapq.heappop(q)
        visited[y][x] = True
      
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if check_range(nx, ny) == True:
                # print(f"visit {nx} {ny} {visited[ny][nx]}")
                if visited[ny][nx] == False:
                    if board[ny][nx] == 0:
                        visited[ny][nx] = True
                        time_arr[ny][nx] = time+1
                        heapq.heappush(q, [time+1, nx, ny])
                        moved += 1
                        if moved == virus:
                            break
                    elif board[ny][nx] == 2:
                        visited[ny][nx] = True
                        # time_arr[ny][nx] = time+1
                        heapq.heappush(q, [time+1, nx, ny])
            
    # print(time_arr)
    # print(f"Moved {moved}")
    if moved < virus:
        return math.inf
    else:
        ret = max([max(a) for a in time_arr])
        return ret

virus = 0
for n in range(N):
    arr = list(map(int, input().strip().split(' ')))
    board.append(arr)
    for x in range(N):
        if arr[x] == 2:
            hosp.append([x, n])
        elif arr[x] == 0:
            virus += 1

combs = combinations(hosp, M)
answer = 10 ** 7
for c in combs:
    # print(c)
    ans = simulate(c, board)
    # print(f"{c} {ans}")
    answer = min(answer, ans)
if answer == 10 ** 7:
    print(-1)
else:
    print(answer)