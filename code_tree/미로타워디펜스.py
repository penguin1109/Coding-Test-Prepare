import sys

sys.stdin = open('./input.txt')
readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' ')) # 격자의 크기, 총 라운드의 수 #
monsters = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # 우-하-좌-상 #
play_x, play_y = N//2, N//2 # 플레이어의 고정된 좌표 #
answer = 0 # 플레이어의 획득 점수 #
CIRCLE = [2, 1, 0, 3] # 달팽이 모양으로 회전 할 때 방향 순서 #
tracker = []

###################### UTILS #########################
def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

def __init__():
    """ 1D로 몬스터들을 처리하는게 빈칸 채우기에도 편할테니까 1D 배열과 2D 격자의 위치 변환을 쉽게 하도록 미리 좌표 저장
    """
    global tracker
    cx, cy = N//2, N//2
    shift = 0
    
    while True:
        for i, dir in enumerate(CIRCLE):
            if i == 2 or i == 0:shift += 1
            for s in range(shift):
                nx, ny = cx + DX[dir], cy + DY[dir]
                tracker.append([nx, ny])
                cx, cy = nx, ny
                if (cx == 0) and (cy == 0): # 좌상단에 도달하면 멈춰야 함 # 
                    return
    
            
def fill_blank():
    global monsters, new_monsters
    i = 0
    next_idx = 0
    
    while (i < len(tracker)):
        tx, ty = tracker[i]
        if monsters[ty][tx] > 0:
            x, y = tracker[next_idx]
            new_monsters[y][x] = monsters[ty][tx]
            next_idx += 1
        i += 1

def remove_duplicated():
    global monsters, answer
    i = 1
    num = monsters[tracker[0][1]][tracker[0][0]]
    cnt = 1
    group = [0]
    
    stop = True
    while (i < len(tracker)):
        x, y = tracker[i]
        if monsters[y][x] == num:
            group.append(i)
            cnt += 1
        else:
            if cnt >= 4 and num > 0:
                stop = False
                for g in group:
                    answer += monsters[tracker[g][1]][tracker[g][0]]
                    monsters[tracker[g][1]][tracker[g][0]] = 0
    
            cnt = 1
            group = [i]
            num = monsters[y][x]
            
        i += 1
    return stop
        
def rearange():
    global monsters
    i = 1
    cnt = 1
    num = monsters[tracker[0][1]][tracker[0][0]]
    index = 0
    
    while (i < len(tracker)):
        x, y = tracker[i]
        if monsters[y][x] == num:
            cnt += 1
        else:
            
            new_monsters[tracker[index][1]][tracker[index][0]] = cnt
            new_monsters[tracker[index+1][1]][tracker[index+1][0]] = num
            index += 2
            if index >= len(tracker):
                return
            num = monsters[y][x]
            cnt = 1
        i += 1
    
        
######################################################
def simulate(d, p):
    import copy
    global answer, new_monsters, monsters
    # (1) 공격칸수만큼 몬스터 제거 # 
    for mv in range(1, p+1):
        nx, ny = play_x + DX[d] * mv,  play_y + DY[d] * mv
        if in_range(nx, ny) == False:
            break
        answer += monsters[ny][nx]
        monsters[ny][nx] = 0
    fill_blank()
    monsters = copy.deepcopy(new_monsters)
    new_monsters = [[0 for _ in range(N)] for _ in range(N)]
    # print(monsters)
    # (2) 동일 몬스터가 4번 이상 반복해서 나오면 몬스터 삭제, 그리고 이 과정의 반복 #
    while True:
        stopable = remove_duplicated()
        if stopable == True:
            break
        fill_blank()
        monsters = copy.deepcopy(new_monsters)
        # print(monsters)
        new_monsters = [[0 for _ in range(N)] for _ in range(N)]
    # (3) 같은 숫자끼리 짝 지어서 (총 개수, 숫자 크기)로 다시 미로에 배치 #
    rearange()
    monsters = copy.deepcopy(new_monsters)
    
    
####################### MAIN ##########################
__init__()

for m in range(M):
    d, p = map(int, readl().strip().split(' ')) # 각 라운드 마다의 플레이어의 방향과 공격 칸 수
    new_monsters = [[0 for _ in range(N)] for _ in range(N)] # 새로 바뀌는 monster 위치 정보를 업데이트 할 배열 #
    
    simulate(d,p)
    # print(monsters)
print(answer)