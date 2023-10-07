import sys
sys.stdin = open('./input.txt', 'r')

readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' ')) # 격자의 크기, 폭탄 종류의 수 #

board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]
answer = 0 # 폭탄이 터지면서 얻은 점수의 합 #

#### STEP 1 : 제일 큰 폭탄 묶음 선택 ####
# 먼저 같은 색깔끼리 묶어 놓고 근처에 빨간색을 최대한 많이 찾아보자 #
def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

# def bfs(sx, sy, visited):
#     from collections import deque
#     import heapq
#     DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
#     q = deque([[sx, sy, 1, 0, sx, sy]]) # x, y, 크기, 빨간 폭탄 개수, 최소 열, 최대 행
#     visited[sy][sx] = True
#     color = board[sy][sx]
#     heap = []
#     track = [[[] for _ in range(N)] for _ in range(N)]
    
#     while q:
#         x, y, size, red_n, mcol, mrow = q.popleft()
#         if size >= 2:
#             heapq.heappush(heap, [size, red_n, -mrow, mcol])
            
#         for dx, dy in zip(DX, DY):
#             nx, ny = x + dx, y + dy
#             if in_range(nx, ny) == False:
#                 continue
#             if board[ny][nx] == color: # query 좌표랑 동일한 폭탄 색일 경우 #
#                 q.append([nx, ny, size+1, red_n, min(mcol, nx), max(mrow, ny)])
#                 if track[ny][nx] == []:
#                     track[ny][nx] = [x, y, size+1]
#                 else:
#                     if track[ny][nx][-1] < size+1:
#                         track[ny][nx] = [x, y, size+1]
#             if board[ny][nx] == 0: # 빨간색인 경우에 #
#                 q.append([nx, ny, size+1, red_n+1, mcol, mrow])
# MAX_GROUP = []
# MAX_SIZE, MIN_RED, MAX_ROW, MIN_COL = -1, float("INF"), -1, float("INF")
# def dfs(x, y, group, size, num_red, mrow, mcol):
#     global MAX_GROUP, MAX_SIZE, MIN_RED, MAX_ROW, MIN_COL
#     if size >= 2:
#         if MAX_SIZE < size:
#             MAX_SIZE = size
#             MAX_GROUP = group;MIN_RED = num_red;MAX_ROW = mrow;MIN_COL=mcol
#         elif MAX_SIZE == size:
#             if MIN_RED > num_red:
                
def bfs(sx, sy):
    color = board[sy][sx]
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    from collections import deque
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True
    q = deque([[sx, sy]])
    
    while q:
        x, y = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) == False:
                continue
            if visited[ny][nx] == True:
                continue
            if board[ny][nx] == color or board[ny][nx] == 0:
                visited[ny][nx] = True
                q.append([nx, ny])
    return visited
    
def get_group(sx, sy):
    visited = bfs(sx, sy)
    import heapq
    red_cnt = 0
    size = 0
    query = [float("INF"), -1] # 기준점의 좌표 (x, y) = (열, 행)#
    for y in range(N):
        for x in range(N):
            if visited[y][x] == False:
                continue
            if board[y][x] == 0:
                red_cnt += 1
            else: # 빨간 폭탄은 기준점이 될 수 없다. # 
                if y > query[1]:
                    query = [x, y]
                elif y == query[1]:
                    if x < query[0]:
                        query = [x, y]
            size += 1
    return size, red_cnt, query[0], query[1]
            
            
            
def largest_group():
    global board
    import heapq
    q = []
    
    for y in range(N):
        for x in range(N):
            if 1 <= board[y][x] <= M: # 빨간 폭탄만 있는 경우를 배제하기 위해서 일부러 색이 있는 폭탄에 대해서 탐색 #
                size, red_cnt, mx, my = get_group(x, y)
                heapq.heappush(q, [-size, red_cnt, -my, mx])
    if len(q) != 0:
        largest = heapq.heappop(q)
    else:
        largest = [-1, -1, -1, -1]
        
    return largest

    
    
#### 중력 작용 ####
def gravity():
    global board
    new_board = [[-2 for _ in range(N)] for _ in range(N)] # 처음에 빈칸으로 채워 주어야 한다. #
    for x in range(N):
        srcY = N-1
        ny = N-1
        while True:
            if srcY == -1:
                break
            n = board[srcY][x]
            if n == -2:
                srcY -= 1
                continue
            if n == -1: # 벽돌인 경우에 # 
                ny = srcY
            new_board[ny][x] = board[srcY][x]
            ny -= 1
            srcY -= 1
            if srcY == -1:
                break
    board = new_board
                
            
            
#### STEP 2 : 선택된 영역의 폭탄 제거 ####
def remove(x, y):
    global board
    visited = bfs(x, y)
    for i in range(N):
        for j in range(N):
            if visited[i][j] == True:
                board[i][j] = -2
    
#### STEP 3 : 반시계 방향으로 90도만큼 회전 ####
def rotate_anti90():
    global board
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    for y in range(N):
        i = 0
        for x in range(N-1, -1, -1):
            new_board[i][y] = board[y][x]
            i += 1
            
    board = new_board
    
    
def simulate():
    global answer
    # (1) 제일 큰 묶음 찾기 #
    largest = largest_group()
    large_size, _, large_y, large_x = largest[0]*-1, largest[1], largest[2]*-1, largest[3]
    
    if large_size <= 1 or largest == [-1, -1, -1, -1]:
        return True
    
    # (2) 폭탄 제거 & 중력 작용 #
    remove(large_x, large_y)
    # print(board)
    gravity()
    # print(board)
    answer += large_size**2
    
    # (3) 회전 & 중력 작용 #
    rotate_anti90()
    gravity()
    
    return False

while True:
    stop = simulate()
    if stop:
        break
print(answer)
    