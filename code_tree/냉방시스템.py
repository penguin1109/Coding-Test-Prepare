import sys
sys.stdin = open('./input2.txt', 'r')
readl = sys.stdin.readline

N, M, K = map(int, readl().strip().split(' ')) # 격자의 크기, 벽의 개수, 사무실의 시원함 정도 #

# AIR_DICT = {
#     2 : [(-1, -1), (-1, 0), (-1, 1)], 
#     3 : [(-1, -1), (0, -1), (1, -1)],
#     4 : [(1, -1), (1, 0), (1, 1)],
#     5 : [(-1, 1), (0, 1), (1, 1)]
# }

AIR_DICT = {
    2 : [[1, 0], [0], [3, 0]],
    3 : [[0, 1], [1], [2, 1]], # [[1, 0], [1], [1, 2]],
    4 : [[1, 2],[2], [3, 2]],
    5 : [[0, 3], [3], [2, 3]], # [[3, 0], [3], [3,2]]
}

DX, DY = [-1, 0, 1, 0], [0, -1, 0, 1] # 좌-상-우-하 #
conditioners = []
offices = []
cold_board = [[0 for _ in range(N)] for _ in range(N)]
check_board = [[[True for _ in range(4)] for _ in range(N)] for _ in range(N)]

def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

for y in range(N):
    arr = list(map(int, readl().strip().split(' ')))
    for x in range(N):
        if 2 <= arr[x] <= 5: 
            conditioners.append([x, y, arr[x]])
        elif arr[x] == 1: # 사무실인 경우 #
            offices.append([x, y])

for m in range(M):
    y, x, s = map(int, readl().strip().split(' ')) # 벽의 좌표, 벽의 위치 #
    y -= 1;x -= 1
    if s == 0: # 위에 벽이 있는 경우 #
        tx, ty = x + DX[1], y + DY[1]
        if in_range(tx, ty):
            check_board[ty][tx][3] = False
            check_board[y][x][1] = False
    elif s == 1: # 왼쪽에 벽이 있는 경우 #
        lx, ly = x + DX[0], y + DY[0]
        if in_range(lx, ly):
            check_board[ly][lx][2] = False
            check_board[y][x][0] = False

###################### STEP 1 : 에어컨 바람 뿜기 ########################
def spread_cold():
    global cold_board
    from collections import deque
    
    for idx, ac in enumerate(conditioners):
        x, y, d = ac # 좌표, 방향 #
        dirs = AIR_DICT[d]
        nx, ny = x + DX[d-2], y + DY[d-2]
        q = deque([[5, nx, ny]])
        visited = [[False for _ in range(N)] for _ in range(N)]
        if check_board[y][x][d-2] == False:
            continue
        visited[ny][nx] = True
        while q:
            cold, x, y = q.popleft()
            cold_board[y][x] += cold
            for i, direction in enumerate(dirs):
                a, b = x, y;valid=True
                for dir in direction:
                    dx, dy = DX[dir], DY[dir]
                    nx, ny = a + dx, b + dy
                    if in_range(nx, ny) == False:
                        valid = False
                        break
                    if check_board[b][a][dir] == False:
                        valid = False
                        break
                    
                    a, b = nx, ny
                
                if valid==True and visited[b][a] == False and cold > 1:
                    q.append([cold-1, a, b])
                    visited[b][a] = True
              
######################## STEP 2 : 에어컨 바람 섞기 ########################
def mix_air():
    global cold_board
    import copy
    # new_cold_board = cold_board
    new_cold_board = copy.deepcopy(cold_board)
    # visited = [[[] for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            for idx, (dx, dy) in enumerate(zip(DX, DY)):
                nx, ny = x + dx, y + dy
                if in_range(nx, ny) == False:
                    continue
                if check_board[y][x][idx] == False:
                    continue
                # if [x, y] in visited[ny][nx] or [nx, ny] in visited[y][x]:
                #     continue
                a, b = cold_board[y][x], cold_board[ny][nx]
                if a < b:
                    diff = (b-a) // 4
                    new_cold_board[y][x] += diff # ;new_cold_board[ny][nx] -= diff
                else:
                    diff = (a-b) // 4
                    new_cold_board[y][x] -= diff # ;new_cold_board[ny][nx] += diff
                # visited[y][x].append([nx, ny])
                # visited[ny][nx].append([x, y])
    cold_board = new_cold_board
######################## STEP 3 : 테두리만 -1 #############################
def confirm():
    global cold_board
    cold_board[0] = [max(0, a-1) for a in cold_board[0]]
    cold_board[-1] = [max(0, a-1) for a in cold_board[-1]]
    for y in range(1, N-1):
        if cold_board[y][0] > 0:
            cold_board[y][0] -= 1
        if cold_board[y][-1] > 0:
            cold_board[y][-1] -= 1
        
def check_finish():
    for x, y in offices:
        if cold_board[y][x] < K:
            return False
    return True
######################## MAIN ############################################
time = 0
while (check_finish() == False):
    spread_cold()
    mix_air()
    confirm()
    time += 1
    ## 최소 시간이 100분을 넘을때는 -1을 출력해주는 조건을 빼놓았어서 41%에서 TLE 발생! 조건 꼼꼼하게 읽기 ##
    if time >= 100:
        time = -1
        break
  
    
# print(cold_board)       
print(time)     
                
            
            
        


