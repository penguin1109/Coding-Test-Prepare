import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline
N, M, K = map(int, input().strip().split(' '))
maze = [list(map(int, input().strip().split(' '))) for _ in range(N)]
for y in range(N):
    for x in range(N):
        maze[y][x] *= -1
"""
0 : 빈칸
-1 ~ -9: 벽 (내구도는 양수)
-10 : 출구
1 이상의 자연수 : 해당 칸에 존재하는 참가자의 

"""
moved_cnt = 0

for m in range(M):
    y, x = map(int, input().strip().split(' '))
    y-=1;x-=1;
    maze[y][x] += 1 # 참가자의 수 업데이트

outy, outx = map(int, input().strip().split(' ')) # 출구의 좌표
outy -= 1;outx -= 1
maze[outy][outx] = -10

DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] ## 상하좌우로의 움직임이 우선순위가 높음

def calc_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def find_exit():
    for y in range(N):
        for x in range(N):
            if maze[y][x] == -10:
                return (y, x)
            
# 참가자들이 이동하는 함수.
def move_people():
    global moved_cnt, maze
    newMaze = [[0 for _ in range(N)] for _ in range(N)] # 이동한 결과를 저장할 배열
    nowExit = find_exit()
    
    # 상하좌우 이동
    dx = [-1, 1, 0, 0]  # 상, 하, 좌, 우
    dy = [0, 0, -1, 1]
    
    # 미로를 확인하면서, 새로운 미로를 업데이트 해준다.
    for i in range(N):
        for j in range(N):
            if maze[i][j] >= -9 and maze[i][j] <= -1:   
                newMaze[i][j] = maze[i][j]  # 벽이어도 참가자는 없지만 new_maze에 벽에 대한 정보 갱신 필요
                continue
            if maze[i][j] == 0: # 그냥 빈칸인 경우에는 이동할 참가자가 없는 경우
                continue
                
            # 참가자가 있다면, 상하좌우로 이동가능한지 체크한다. 짧아지는 방향으로 이동해야 한다.
            # 현재 좌표 : (i, j)
            curDist = calc_dist(i, j, nowExit[0], nowExit[1]) # 현재좌표에서 출구까지 거리.
            minDist = curDist   # 나중에 업데이트 될, 이동한 좌표에서 출구까지 거리. => minDist인 좌표로 이동가능하다.
            
            # 상하좌우 이동가능한지, 이동했을 때 출구까지 거리가 가까워지는지 확인한다.
            for d in range(4):
                nx = i + dx[d]
                ny = j + dy[d]
                if nx < 0 or nx >= N or ny < 0 or ny >= N:  # 이동한 좌표가 미로 범위를 넘어가면, 무시한다.
                    continue
                if maze[nx][ny] >= -9 and maze[nx][ny] <= -1:   # 이동한 좌표가 벽이라면, 무시한다.
                    continue
                # 이동가능 하다면, 출구까지 짧은거리와 해당 좌표 갱신
                afterDist = calc_dist(nx, ny, nowExit[0], nowExit[1])  # 새로운 위치와 출구 사이의 거리를 계산
                if minDist > afterDist: # 이동한 거리가 출구까지 거리와 더 가깝다면, 이동할 좌표를 갱신한다. (minI, minJ)를.
                    minDist = afterDist
                    minI = nx
                    minJ = ny
            
            # 상하좌우 이동을 할 수 없는 경우에는 그냥 그 위치 그대로 존재
            if minDist == curDist:
                newMaze[i][j] += maze[i][j]
                continue
            
            # 이동가능 하다면,
            moved_cnt += maze[i][j]   # 참가들이 움직이니까, 격자 안의 참가자 수 만큼 더해준다.
            
            # 참가자가 exit에 도달하는 경우에는 <모두> 탈출하는 개념이기 때문에 이어서 진행 안함
            if maze[minI][minJ] == -10:
                continue
            
            newMaze[minI][minJ] += maze[i][j]
            
    # 기존 maze 배열 업데이트
    maze = newMaze

def rotate_square(x, y, d):
    temp = [[0 for _ in range(d+1)] for _ in range(d+1)]
    new = [[0 for _ in range(d+1)] for _ in range(d+1)]
    for i in range(1+d):
        for j in range(1+d):
            temp[i][j] = maze[x+i][y+j]
    for i in range(1+d):
        for j in range(1+d):
            if temp[i][j] >= -9 and temp[i][j] <= -1:
                temp[i][j] += 1 ## 벽인 경우에는 내구도를 바꿔 주어야 한다. (음수로 지정했으니 +1)
            new[j][d-i] = temp[i][j]
    for i in range(x, x+d+1):
        for j in range(y, y+d+1):
            maze[i][j] = new[i-x][j-y]
            
# 이동 후에 정사각형을 회전해야 하므로 회전함수를 구현.
def Rotate():
    ##### STEP1 : 제일 작은 가능한 정사각형을 찾기 #####
    # 길이를 먼저 정해 놓은 다음에 출구와 참가자 최소 1명이 존재해야 한다는 조건을 만족하는지 확인 
    # 최소의 정사각형의 크기가 정해지면 그 다음에 최상단의 좌표가 제일 좌측 상단에 있는 것을 결정
    minDist = 1000000   # 정사각형의 변의 길이.
    nowExit = find_exit()    # 출구 좌표
    
    for i in range(N):
        for j in range(N):
            if maze[i][j] >= 1:  # 참가자가 있다면, 출구까지 거리 계산
                dist = max(abs(i-nowExit[0]), abs(j-nowExit[1])) # 가로, 세로 중 큰 값이 가장 작은 정사각형이 된다.
                minDist = min(minDist, dist)    # 최소 정사각형을 찾는다. => 좌표의 차이기 때문에 칸 개념으로 하려면 +1 해줘야함.
    # print(f"MIN DIST : {minDist}")
    # 2. 작은 정사각형 크기 중, 좌상단의 숫자가 작은 것이 정사각형의 위치
    bestRow, bestCol = -1, -1 # 좌상단.
    for i in range(N-minDist): ## Y축기준으로 볼 때 좌측 상단의 값이 제일 작은 것 부터 for loop
        for j in range(N-minDist):  ## X축 기준으로 볼 때 좌측 상단의 값이 제일 작은 것 부터 for loop
            # 현재좌표 : (i, j)
            # 정사각형 우하단 좌표 : (i+minDist, j+minDist)
            
            flagExit, flagPerson = False, False     # 출구와 참가자가 모두 존재하는지 확인할 변수
            for r in range(i, i+minDist+1):
                for c in range(j, j+minDist+1):
                    if maze[r][c] == -10:   flagExit = True   # 출구가 포함되어 있다면, 
                    if maze[r][c] >= 1: flagPerson = True      # 사람이 포함되어 있다면,
            
            if (flagExit and flagPerson): # 좌상단이 (i, j)인 정사각형에 출구와 사람이 모두 포함되어 있다면, 바로 그것이 최소 정사각형 결정.
                bestRow = i
                bestCol = j
                break
        if bestRow != -1:
            break
    # print(bestRow, bestCol, minDist)
    # 3. 찾은 최소 정사각형을 회전한다.
    rotate_square(bestRow, bestCol, minDist)
            
    

# 게임종료 확인
def isFinish():
    for i in range(N):
        for j in range(N):
            if maze[i][j] > 0: # 참가자가 한명이라도 있으면, 아직 다 못빠져나간것(게임종료 불가능)
                return False
    return True

###################### MAIN ###########################
for _ in range(K):
    move_people()
    # print("MOVED", maze)
    if isFinish():
        break
    Rotate()
    # print(maze)
    # print(find_exit())

    print(moved_cnt)
nowExit = find_exit()
print(moved_cnt)
print(nowExit[0]+1, nowExit[1]+1)         