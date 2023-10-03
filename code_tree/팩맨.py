"""
STEP 1: 몬스터 복제 시도
- 몬스터가 본인과 동일한 위치, 방향의 몬스터를 복제. 복제된 몬스터는 움직일수 X
- 복제된 몬스터는 자신의 복제 원본인 몬스터와 동일한 방향을 가짐.
STEP 2: 몬스터 이동
- 이동 불가 조건: (1) 칸에 몬스터 시체가 있는 경우 (2) 팩맨이 있는 경우 (3) 격자를 벗어나는 경우
    -> 반시계 방향으로 45도 회전 (이동할 수 있을 때까지) -> 한바퀴 돌았는데 이동 불가면 고정
STEP 3: 팩맨 이동
- 팩맨은 **상하좌우**로만 이동 가능
- 총 3칸을 이동, 매 이동마다 다른 방향으로 이동 가능. 몬스터를 최대로 먹을 수 있는 방향으로 이동
- 먹고, 시체 남김. 알은 먹지 X -> 즉, 죽은 몬스터도 모두 트래킹 해야 함. 
- class Monster안에 status항목으로 Dead Alive 구분 (0이면 dead, -3이 되면 소멸 시체)
STEP 4: 몬스터 시체 소멸
- 2턴 동안만 시체 유지. 그 이상이 지나면 소멸
STEP 5: 몬스터 복제 완성
- 알의 형태였던 몬스터 부화 ( status = 1 )
- 완전히 깨어 있는 몬스터는 ( status = 2 )

[출력]
모든 턴이 진행 된 이후에 살아 남아 있는 몬스터의 개수를 출력하여라.
"""

M, T = map(int, input().strip().split(' ')) # 몬스터의 개수, 턴의 수
r, c = map(int, input().strip().split(' ')) # 팩맨의 격자에서의 초기 위치
r -= 1;c -= 1

monsters = []
alive_monster = [[0 for _ in range(4)] for _ in range(4)]

DX, DY = [0, -1, -1, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1, 0, -1] # 몬스터의 이동 방향 (8방)

class Monster:
    def __init__(self, x, y, d, s):
        self.status = s  ## 완전히 깨어 있는 몬스터
        self.x = x
        self.y = y
        self.d = d

board = [[[] for _ in range(4)] for _ in range(4)]
for m in range(M):
    y, x, d = map(int, input().strip().split(' '))
    new_monster = Monster(x-1, y-1, d-1, 2)
    board[y-1][x-1].append(new_monster)
    alive_monster[y-1][x-1] += 1


def _check_movable(x, y):
    if x < 0 or x >= 4 or y < 0 or y >= 4:
        return False
    if x == pack_x and y == pack_y:
        return False
    for m in board[y][x]:
        if -2 <= m.status <= 0: ## 자리에 소멸 예정인 몬스터가 있어도 몬스터는 이동이 불가능하다.
            return False
    return True

def clone_monster():
    global board
    for y in range(4):
        for x in range(4):
            cloned = []
            if len(board[y][x]) > 0:
                for m in board[y][x]:
                    if m.status == 2:
                        clone = Monster(m.x, m.y, m.d, 1) # 아직 부화 직전 알의 형태
                        cloned.append(clone)
            board[y][x].extend(cloned)

def move_monster():
    global board, alive_monster
    new_board = [[[] for _ in range(4)] for _ in range(4)]

    for y in range(4):
        for x in range(4):
            for idx, m in enumerate(board[y][x]):
                if m.status == 2: # 움직일 수 있는 몬스터인 경우에
                    d = m.d
                    start = m.d
                    movable = False
                    while True:
                        nx, ny = x + DX[d], y + DY[d]
                        if _check_movable(nx, ny):
                            movable=True
                            m.x = nx;m.y = ny
                            break
                        else:
                            d = (d+1)%8 # 반시계방향으로 45도만큼 회전
                            m.d = d
                        if d == start:
                            break
                    if movable:
                        new_board[ny][nx].append(Monster(nx, ny, d, 2))
                        alive_monster[ny][nx] += 1
                        alive_monster[y][x] -= 1
                    else:
                        new_board[y][x].append(m)
                else:
                    new_board[y][x].append(m)

    board = new_board

most_eat = -1
pack_road = []
max_road = []
flag = 0

def search_most_eat(x, y, cnt, m_cnt):
    MX, MY = [0, -1, 0, 1], [-1, 0, 1, 0] # 상-좌-하-우
    global most_eat, pack_road, max_road, flag

    if cnt == 3: ## 3번 이동을 이미 한 경우에
        if flag == 0: ##  처음 도착한 경우 -> 우선순우가 제일 높을 것임
            most_eat = m_cnt
            flag = 1
            max_road = pack_road[:]
        if m_cnt > most_eat: ## 우선순위 반드시 고려해 주어야 함
            most_eat = m_cnt
            max_road = pack_road[:]
        return

    for dx, dy in zip(MX, MY):
        nx, ny = x + dx, y + dy
        if (0 <= nx < 4 and 0 <= ny < 4):
            new_arrive =False
            if visited[ny][nx] == 0:
                new_arrive=True
                m_cnt += alive_monster[ny][nx]
            visited[ny][nx] += 1
            pack_road.append([nx, ny])
            search_most_eat(nx, ny, cnt+1, m_cnt)
            pack_road.pop()
            if new_arrive:
                m_cnt -= alive_monster[ny][nx]
            visited[ny][nx] -= 1
 
def move_packman():
    global board, alive_monster
    # print(f"PACK ROAD: {pack_road}")
    for pack in pack_road:
        px, py = pack[0], pack[1]
        

        if alive_monster[py][px] > 0:
            for idx, m in enumerate(board[py][px]):
                if m.status == 2:
                    board[py][px][idx].status = 0 # 죽은 상태로 바꿔 놓
            alive_monster[py][px] = 0
            
                

def update_monster():
    global board

    for y in range(4):
        for x in range(4):
            for idx, m in enumerate(board[y][x]):
                if m.status == 1:
                    m.status = 2
                    alive_monster[y][x] += 1 ## 알에서 부화하는 경우에 
                
                elif -2 < m.status <= 0:
                    m.status -= 1
                elif m.status == -2: ## 이제 2턴이 지났으니까 몬스터는 소멸된다.
                    m.status = -100
                board[y][x][idx] = m

pack_x = c
pack_y = r

for t in range(T):
    clone_monster()
    # print(alive_monster)
    move_monster()
    # print(alive_monster)
    # print(board)
    visited = [[0] * 4 for _ in range(4)]
    # visited[pack_y][pack_x] = 1
    most_eat = -1
    pack_road, max_road = [], []

    search_most_eat(pack_x, pack_y, 0, 0)
    # print(f"MOST EAT: {most_eat}")
    pack_road = max_road[:]
    move_packman()
    # print(alive_monster)
    pack_x, pack_y = pack_road[-1]
    pack_road.clear()

    update_monster()
    print(alive_monster)
# print(alive_monster)
tot_alive = sum([sum(a) for a in alive_monster])
print(tot_alive)
