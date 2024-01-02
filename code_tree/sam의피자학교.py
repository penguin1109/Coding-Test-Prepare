import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, K = map(int, readl().strip().split(' ')) # 배열의 크기, 최대와 최소의 차이 # 

# [출력] 밀가루의 양의 최대와 최소가 차이가 k이하가 되는 최소 연산 횟수 #
"""
1 <= N <= 100이기 떄문에 O(N)에 대한 연산이 큰 무리가 없다.
열과 행의 크기로 정렬하는 부분이 있기 때문에 2차원 배열로 관리

"""
board = [[0 for _ in range(N+1)] for _ in range(N+1)]
board[N][1:] = list(map(int, readl().strip().split(' ')))

def add_min(): ## STEP 1 ##
    global board
    MIN = float("INF")
    arr = []
    for y in range(1, N+1):
        for x in range(1, N+1):
            n = board[y][x]
            if n == 0:
                continue
            if n < MIN:
                MIN = n
                arr = [(x, y)]
            elif n == MIN:
                arr.append((x, y))
    for x, y in arr:
        board[y][x] += 1
   

def roll(): ## STEP 2 ##
    global board
    query, w, h = 1, 1, 1
    idx = 0
    while True:
        if (query-1+w+h > N):
            break
        
        for col in range(query, query + w):
            for row in range(N, N-h, -1):
                nrow = (N-w) + (col-query)
                ncol = (query+w) + (N-row)
                board[nrow][ncol] = board[row][col]
                board[row][col] = 0
        query += (idx//2+1)
        if query%2 == 0:
            h += 1
        else:
            w += 1
        idx += 1

def in_range(x, y):
    return (1 <= x <= N and 1 <= y <= N)

def push(): ## STEP 3 ##
    global board
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    new_board = [[0 for _ in range(N+1)] for _ in range(N+1)]
    # new_board = board
    for y in range(1, N+1):
        for x in range(1, N+1):
            if board[y][x] != 0:
                new_board[y][x] += board[y][x] ## TODO 처음에 그냥 new_board = board로 할때는 안됬는데 이렇게 바꾸니까 됨! ##
                for dx, dy in zip(DX, DY):
                    nx, ny = x + dx, y + dy
                    if in_range(nx, ny) == False:
                        continue
                    if board[ny][nx] == 0:
                        continue
                    if board[y][x] > board[ny][nx]:
                        diff = (board[y][x] - board[ny][nx]) // 5
                        new_board[y][x] -= diff
                        # new_board[ny][nx] += diff
                    else:
                        diff = (board[ny][nx] - board[y][x])  // 5
                        new_board[y][x] += diff
    board = new_board

def unsqueeze(): ## 중간에 step3, 4 마치고 바로 1D로 펴주는 작업 ## 
    """열이 작은 것부터 먼저 나열 -> 행이 큰 것 부터 나열"""
    temp = []
    for x in range(1, N+1):
        for y in range(1, N+1):
            if board[y][x] != 0:
                temp.append((board[y][x]))
                board[y][x] = 0
    for idx, n in enumerate(temp):
        board[N][idx+1] = n
    
            
def fold(): ## STEP 4 ##
    quarter = N // 4
    col_arr = [0, N, N-quarter+1, N]
    col_dir = [0, -1, 1, -1]
    
    srcY = 1
    for i in range(1, 4):
        col = col_arr[i]
        for j in range(quarter):
            board[N-i][col] = board[N][srcY]
            board[N][srcY] = 0
            col += col_dir[i]
            srcY += 1

def do_finish():
    MIN, MAX = float("INF"), -1
    for x in range(1, N+1):
        for y in range(1, N+1):
            if board[y][x] == 0:
                continue
            n = board[y][x]
            MIN = min(MIN, n);MAX = max(MAX, n)
    print(MIN, MAX)
    if MAX-MIN <= K:
        return True
    return False

def simulate():
    add_min()
    
    roll() # 말아주기 # 
    push() # 눌러주기 # 
    unsqueeze() # 2D 격자 -> 1D 격자로 변환 #
   
    fold() # 접어주기 #
    push() # 눌러주기 # 
    unsqueeze() # 2D 격자 -> 1D 격자로 변환 #

answer=1
while True:
    simulate()
    if do_finish():
        break
    answer += 1

 
print(answer)
    