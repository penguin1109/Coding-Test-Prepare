import sys
from collections import deque
import heapq
input = sys.stdin.readline

N, M = map(int, input().strip().split(' ')) # 격자의 크기, 빨간색 외의 다른 폭탄의 종류 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # -1에서 M 사이의 값들 #

'''[출력] 폭탄묶음이 없을 때까지 진행한 후의 최종 점수'''
# 돌 : -1 #
# 빨 : 0 #
# 나머지 : 1,2,3 #

DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
answer = 0

def gravity_old():
    global board
    new_board = [[-2 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        blank = deque([])
        dst_y = N-1
        for y in range(N-1, -1, -1):
            if board[y][x] == -2:
                # blank.append((x, y))
                # blank.append((x, dst_y))
                # dst_y -= 1
                continue
            elif board[y][x] == -1:
                new_board[y][x] = -1
                # if len(blank) > 0:
                #     xx, yy = blank.popleft()
                #     new_board[yy][xx] = board[y][x]
                # else:
                #     new_board[y][x] = board[y][x]
                # blank = deque([])
                dst_y = y-1
            else:
                # if blank:
                #     xx, yy = blank.popleft()
                #     new_board[yy][xx] = board[y][x]
                # else:
                #     new_board[y][x] = board[y][x]
                # blank.append((x, dst_y))
                new_board[dst_y][x] = board[y][x]
                dst_y -= 1
            if dst_y == -1:
                break
    return new_board

def gravity():
    new_board = [[-2 for _ in range(N)] for _ in range(N)]            
    for x in range(N):
        src_y = N-1
        ny = N-1
        while True:
            if src_y == -1:
                break
            color = board[src_y][x]
            if color == -2: # 빈 곳인 경우 #
                src_y -= 1
                continue
            if color == -1: # 벽돌인 경우 #
                ny = src_y
            new_board[ny][x] = board[src_y][x]
            ny -= 1
            src_y -= 1
            '''불필요한 if 문은 최대한 제외하자. 시간 복잡도가 증가함.'''
    return new_board
                
def bfs(sx, sy):
    color = board[sy][sx]
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[sy][sx] = True
    q = deque([[sx, sy]])
    while q:
        x, y = q.popleft()
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if in_range(nx, ny) and visited[ny][nx] == False:
                if board[ny][nx] == color or board[ny][nx] == 0:
                    visited[ny][nx] = True
                    q.append([nx, ny])
    return visited

def get_group(sx, sy):
    visited = bfs(sx, sy)
    red_cnt, size = 0,0
    query = [float("INF"), -1]
    for y in range(N):
        for x in range(N):
            if visited[y][x] == False:
                continue
            if board[y][x] == 0:
                red_cnt += 1
            elif board[y][x] >= 1:
                if y > query[1]:
                    query = [x, y]
                elif y == query[1]:
                    if x < query[0]:
                        query = [x, y]
            if visited[y][x] == True:
                size += 1
    return size, red_cnt, query[0], query[1]

def largest_group():
    q = []
    for y in range(N):
        for x in range(N):
            if M >= board[y][x] >= 1:
                size, red_cnt, qx, qy = get_group(x, y)
                heapq.heappush(q, (-size, red_cnt, -qy, qx))
    if len(q) > 0:
        largest = heapq.heappop(q)
    else:
        largest = [-1, -1, -1, -1]
    return largest
                
def rotate_90():
    global board
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    for y in range(N):
        i = 0
        for x in range(N-1, -1, -1):
            new_board[i][y] = board[y][x]
            i += 1
            
    return new_board

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

        
def search_big_group(x, y):
# def search_big_group(x, y, visited):
    q = [(-1, 1, y, x, [(x, y)])]
    # visited[y][x] = True
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[y][x] = True
    ret_q = []
    while q:
        num, red, yy, xx, coords = heapq.heappop(q)
        # heapq.heappush(ret_q, (num, red, coords))
        valid = False
        for dx, dy in zip(DX, DY):
            nx, ny = xx + dx, yy + dy
            # print(xx, yy, nx, ny)
            if in_range(nx, ny) and visited[ny][nx] == False and board[ny][nx] >= 0:
                if board[ny][nx] == 0:
                    heapq.heappush(q, (num-1, red+1, ny, nx, coords + [(nx, ny)]))
                elif board[ny][nx] >= 1:
                    heapq.heappush(q, (num-1, red, ny, nx, coords + [(nx, ny)]))
                else:
                    continue
                visited[ny][nx] = True
                valid = True
        if valid == False:
            coords = sorted(coords, key = lambda coord : (-coord[1], coord[0]))
            
            for cx, cy in coords:
                if board[cy][cx] != 0:
                    heapq.heappush(ret_q, (-num, red, -cy, cx, coords))
                    break
    # print(q)
    # print(ret_q)
    while ret_q:
        num, red, cy, cx, coords = heapq.heappop(ret_q)
        color_set = set([board[y][x] for (x, y) in coords])
        print("COLOR SET ", color_set, coords)
        if -num < 2:
            return None
        if -num >= 2:
            if (0 in color_set and len(color_set) == 2) or (0 not in color_set and len(color_set) == 1):
                return -num, red, coords, cx, -cy
    return None  

def update_visited(visited, coords):
    for (x, y) in coords:
        visited[y][x] = True
    return visited

def remove(x, y):
    visited = bfs(x, y)
    global board
    for yy in range(N):
        for xx in range(N):
            if visited[yy][xx] == True:
                board[yy][xx] = -2
                
def run():
    global board, answer
    largest = largest_group()
    largest_size, _, qy, qx = largest[0]*-1, largest[1], largest[2] * -1, largest[3]
    # print(largest_size)
    if largest_size <= 1 or largest == [-1, -1, -1, -1]:
        return True
    remove(qx, qy)
    # print(board)
    # debug_board(board)
    board = gravity_old()
    # board = gravity()
    # debug_board(board)
    answer += largest_size ** 2
    board = rotate_90()
    # debug_board(board)
    # board = gravity()
    board = gravity_old()
    
    return False

def debug_board(board):
    global iter
    print("*"*30)
    print(f"Iter {iter}")
    for y in range(N):
        print(' '.join([str(s) for s in board[y]]))
    print("*" * 30)
def biggest_group():
    global board, answer
    '''모두 같은 색 폭탄 (-> 이게 빨간색이면 안됨) or 빨간색 포함 2개의 색 
    -> 폭탄 묶음은 무조건 2개 이상
    - (0) 개수가 제일 많은 것
    - (1) 빨간색이 적은 것
    - (2) 가장 좌측 하단의 '기준점'이 제일 밑에 (Y가 큼) -> 제일 왼쪽에 (X가 작음) 위치한 
    - (3) 선택된 폭탄 전부 제거 -> 이때 폭탄 묶음의 개수 C개면 answer += C ** 2
    - (4) 중력 작용
    - (5) 반시계 90도 회전
    - (6) 중력 작용
    '''
    q = []
    visited = [[False for _ in range(N)] for _ in range(N)]
    for y in range(N):
        for x in range(N):
            ret = search_big_group(x, y)
            if ret is None:
                continue
            else:
                num, red, coords, cx, cy = ret
                heapq.heappush(q, (-num, red, -cy, cx, coords))
    print(board)
    # print("REMOVE " , coords)
    if q:
        num, red, y, x, coords = heapq.heappop(q)
        for (xx, yy) in coords:
            board[yy][xx] = -2
        answer += (-num) ** 2
    else: # 제거될 폭탄 묶음이 없는 경우 #
        return True # 게임 멈춰야 함 #
    print(board)
    
    board = gravity()
    print(board)
    
    board = rotate_90()
    print(board)
    
    board = gravity()
    print(board)

    return False

iter = 0
while True:
    # do_stop = biggest_group()
    do_stop = run()
    
    if do_stop:
        break
    # exit(0)
    # iter += 1
    # print(board)
    # debug_board(board)
    iter += 1
print(answer)