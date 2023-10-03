import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

M, T = map(int, readl().strip().split(' ')) # 몬스터의 개수, 진행되는 턴의 수

"""
monsters : [[x,y,d,status]..[]]으로 저장
-> status는 살아있으면 1, 시체 상태이면 0, 시체가 된 이후로 몇번의 turn을 거쳤는지 확인 (-2가 된 turn이 모두 끝나면 죽음 처리)
"""
monsters = [[[] for _ in range(4)] for _ in range(4)] # 한 칸에 여러개의 몬스터가 존재할 수 있고 (왜냐면 복제도 가능하고 등등,,)
corpus = [[0 for _ in range(4)] for _ in range(4)] # 몬스터가 이동가능한지 트래킹 한다. 

pack_y, pack_x = map(int, readl().strip().split(' ')) # 팩맨의 y, x 좌표
pack_y -= 1;pack_x -= 1

mDX, mDY = [0, -1, -1, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1, 0, -1] # 몬스터의 이동 방향 (8방) #
pDX, pDY = [0, -1, 0, 1], [-1, 0, 1, 0] # 팩맨의 이동 방향 #

for m in range(M):
    y, x, d = map(int, readl().strip().split(' ')) # 몬스터의 위치, 방향 정보
    # monsters.append([x-1, y-1, d-1, 1])
    monsters[y-1][x-1].append([x-1, y-1, d-1])

def in_range(x, y):
    return 0 <= x < 4 and 0 <= y < 4

global ROUTE
ROUTE = []
global MAX_EAT
MAX_EAT = -1
import copy
def dfs(x, y, route, eaten, visited):
    global ROUTE, MAX_EAT
    if len(route) == 3:
        if MAX_EAT < eaten:
            MAX_EAT =  copy.deepcopy(eaten)
            ROUTE = copy.deepcopy(route)
            # print(f"GLOBAL ROUTE : {ROUTE} MAX EATEN : {eaten}")
        return 
    
    for dx, dy in zip(pDX, pDY):
        nx, ny = x + dx, y + dy
        if in_range(nx, ny):
            if visited[ny][nx] == False:
                visited[ny][nx] = True
                new_route = route + [[nx, ny]]
                dfs(nx, ny, new_route, eaten + len(new_monsters[ny][nx]), visited)
                visited[ny][nx] = False
            else:
                new_route = route + [[nx, ny]]
                dfs(nx, ny, new_route, eaten, visited)
                
    
############ STEP1: 몬스터의 자가 복제 ##############
def clone():
    global monsters
    for y in range(4):
        for x in range(4):
            for m in monsters[y][x]:
                new_monsters[y][x].append(m)
    monsters = new_monsters
            

############ STEP2 : 몬스터 이동 ####################
def move_monster():
    global monsters, new_monsters
    
    for y in range(4):
        for x in range(4):
            if len(monsters[y][x]) == 0:
                continue
            
            for mx, my, d in monsters[y][x]:
                moved = False
                for i in range(8):
                    new_dir = (d + i) % 8
                    nx, ny = mx + mDX[new_dir], my + mDY[new_dir]
                    if in_range(nx, ny) == False: # 격자 내에 존재하지 않는 경우 #
                        continue
                    if nx == pack_x and ny == pack_y: # 팩맨과 동일한 위치인 경우 #
                        continue
                    if corpus[ny][nx] > 0: # 몬스터 사체가 존재하는 경우 #
                        continue
                    new_monsters[ny][nx].append([nx, ny, new_dir])
                    moved = True
                    break
                
                if moved == False:
                    new_monsters[my][mx].append([mx, my, d])
    
    
############ STEP3~5: 팩맨 이동 및 몬스터 상태 업데이트 ########################
def move_packman():
    global ROUTE, MAX_EAT, new_monsters, corpus, pack_x, pack_y
    ROUTE = [];MAX_EAT = -1
    visited = [[False for _ in range(4)] for _ in range(4)]
    # visited[pack_y][pack_x] = True
    dfs(pack_x, pack_y, [], 0, visited)
    
        
    # print(f"NEW ROUTE : {ROUTE} MAX EAT : {MAX_EAT}")

    new_px, new_py = ROUTE[-1]
    pack_x, pack_y = new_px, new_py
    
    for x, y in ROUTE:
        if len(new_monsters[y][x]) > 0:
            new_monsters[y][x] = []
            corpus[y][x] = 3
            
    for y in range(4):
        for x in range(4):
            if corpus[y][x]: # 0보다 큰 값을 갖고 있는 경우에 
                corpus[y][x] -= 1
    

############ MAIN ############################
import copy

for t in range(T):
    new_monsters = [[[] for _ in range(4)] for _ in range(4)]
    cloned = monsters
    move_monster()
    move_packman()
    for y in range(4):
        for x in range(4):
            new_monsters[y][x] += cloned[y][x]
    monsters = new_monsters
    
    
answer = 0
for y in range(4):
    for x in range(4):
        answer += len(monsters[y][x])
print(answer)
    
            
                
        
    
    
    
                    
            
            
        
        
    

