import heapq
import copy

# 상어가 먹을 수 있는 물고기 번호의 합의 최댓값을 구하여라.
# 근데 구현을 하려고 하다 보니 DFS를 사용해서 모든 경우에서 상어가 물고기를 먹는 조합을 생각해야 했음을 확인하였다.

DY, DX = [0, -1, -1, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1, 0, -1]

area = [[-1 for _ in range(4)] for _ in range(4)]
fish = [] # 물고기의 번호와 방향만 저장 -> 번호가 작은 순으로 빼내기 위해서
fish_loc = [-1 for _ in range(17)] # 물고기의 번호 별 위치를 저장한다.
fish_dir = [-1 for _ in range(17)]
board = [[] for _ in range(4)]
shark = [0, 0, -1] # x좌표, y좌표, 방향

for j in range(4):
    row = list(map(int, input().split(' ')))
    for i in range(0, len(row), 2):
        a, b = row[i], row[i+1]-1 # 물고기의 번호, 물고기의 방향
        """ 방항 처리하는데 놓친 부분
        - 방향을 고려하는데 첫 시작이 당연히 0부터일 것이라고 생각했다.
        - 하지만 물고기의 번호도, 방향도 모두 1부터 시작하였다.
        """
        board[j].append([a, b])
        heapq.heappush(fish, (a, b))
        fish_loc[a] = [j, i] # 물고기의 번호에 따른 물기의 위치
        fish_dir[a] = b
        area[j][i // 2] = a # 물고기의 번호만 저장

def swap_fish(x, y, nx, ny):
    # 방향은 위치가 바뀌어도 우선은 그대로임.
    src_fish = area[y][x]
    tar_fish = area[ny][nx]
    fish_loc[tar_fish] = [x,y]
    fish_loc[src_fish] = [nx, ny]
    area[ny][nx] = src_fish
    area[y][x] = src_fish

def move_all_fish(arr):
    new_fish = []
    while len(fish) != 0:
        temp = heapq.heappop(fish)
        a, b = temp # 물고기 번호, 방향, 좌표
        if fish_loc[a] == [-1, -1]: # 잡아먹힌 물고기
            continue # 이제 물고기가 빠지니까 더이상 loop에서 관여를 하지 않을 것임.

        x, y = fish_loc[a]
        mv = 0
        moved = False
        while (mv < 8):
            new_dir = (b + mv) % 8
            nx, ny = x + DX[new_dir], y + DY[new_dir]
            if (0 <= nx < 4 and  0 <= ny < 4):
                if (area[ny][nx] == -2): # 상어가 해당 칸에 있으면 이동이 불가능.
                    continue
                if (area[ny][nx] == -1):
                    area[ny][nx] = a # 새로운 칸의 위치에 업데이트
                    area[y][x] = -1 # 원래 있던 칸에 아무것도 없음을 표시
                    fish_loc[a] = [nx, ny]
                    fish_dir[a] = new_dir
                    heapq.heappush(new_fish, (a, new_dir)) # 큐에도 다시 넣어줌.
                    moved = True
                elif (area[ny][nx] != -1): # 위치에 다른 물고기가 있었다면
                    swap_fish(x, y, nx, ny)
                    fish_dir[a] = new_dir
                    heapq.heappush(new_fish, (a, new_dir))
                    moved = True

            else:
                mv += 1
        if moved == False: # 움직이지 못한 경우에도 역시나 new_fish에 넣어줌,
            heapq.heappush((a, b), new_fish)

    return new_fish

def eat_fish(x, y):
    fish_id = area[y][x]
    area[y][x] = -2
    fish_loc[y][x] = [-1, -1]
    new_dir = fish_dir[fish_id]
    return [x, y, new_dir]

def move_shark(shark):
    x, y, dir = shark
    if dir == -1: # 처음 상어가 움직이는 경우
        eat_fish(x, y)
        return
    eaten = False

    # 상어가 이동을 처음 하는게 아닌 경우
    while True:
        nx, ny = x + DX[dir], y + DY[dir]
        if (0 <= nx < 4 and 0 <= ny < 4 and area[ny][nx] >= 0):
            eat_fish(nx, ny) # 상어가 물고기를 먹음 -> 물고기는 계속 이동을 해야 한다.
            """
            - 여기서 상어가 물고기를 먹고 백트래킹으로 모든 경우를 시도하려면 당연히 원상 복귀가 되어야 한다.
            - 하지만 이는 재귀적으로 해야만 가능하기 때문에 당연히 여기서 dfs로 해결 했어야 했다.
            """
            eaten = True
        else:
            break
    return False


best_score = -1 # 최대로 상어가 먹을 수 있는 물고기의 번호의 합을 저장하는 변수
def dfs(sx, sy, score, board):
    global best_score
    score += board[sx][sy][0] # 상어가 위치한 곳에 있는 물고기의 번호를 더해줌
    best_score = max(best_score, score) # 점수 갱신
    board[sx][sy][0] = -2 # 잡아 먹힌 상어는 -2로 바꿔준다.

    # fx, fy = -1, -1
    # 모든 물고기가 움직이도록 한다.
    """
    - 물고기의 위치를 기반으로 번호가 전부 저장이 되어 있어야 한다고 생각했지만, 타일의 크기가 4x4로 작고 고정된 만큼 직접 16마리의 물고기에 대해서
    찾아주어도 되는 부분이었다.
    """
    for f in range(1, 17): # 물고기의 번호는 1 ~ 16까지이다.
        fx, fy = -1, -1
        for x in range(4):
            for y in range(4):
                if board[x][y][0] == f: # f번호에 해당하는 물고기 찾기
                    fx = x;fy = y;
                    break
        if fx == -1 and fy == -1:
            continue
        fdir = board[fx][fy][1]

        for i in range(8): # 물고기 이동시켜주기 -> 이동할 수 없다면 그냥 continue를 하면 됨, 별도의 처리 필요 없음.
            new_dir = (fdir + i) % 8
            nx = fx + DX[new_dir]
            ny = fy + DY[new_dir]
            if not (0 <= nx < 4 and 0 <= ny < 4) or (nx == sx and ny == sy):
                continue
            board[fx][fy][1] = new_dir
            board[fx][fy], board[nx][ny] = board[nx][ny], board[fx][fy] # fish_swap는 단순히 이렇게도 구현이 가능했었다.
            break

    sdir = board[sx][sy][1]
    for i in range(1, 5):
        # 상어는 최대 4번씩 해당 방향으로 이동이 가능하다.
        nx = sx + DX[sdir] * i
        ny = sy + DY[sdir] * i
        if (0 <= nx < 4 and 0 <= ny < 4) and board[nx][ny][0] > 0:
            dfs(nx, ny, score, copy.deepcopy(board)) # deepcopy를 사용함으로서 절대 변경된 이동 값이 원본 board에는 반영이 안되도록 한다.

dfs(0, 0, 0, board)
print(best_score)


















