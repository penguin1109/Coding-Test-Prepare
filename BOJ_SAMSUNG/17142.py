N, M = map(int, input().split(' '))
OFFICE = []
from collections import deque
from itertools import combinations
import copy
VIRUS = deque()
# 활성 바이러스가 있는 위치는 -1로 설정할 것이다.
wall = 0 # 벽의 개수
for n in range(N):
    row = list(map(int, input().split(' ')))
    for i in range(N):
        if row[i] == 2:
            VIRUS.append((n, i))
        if row[i] == 1:
            wall += 1
    OFFICE.append(row)

ANSWER = 1e+6

def spread(office, virus):
    global ANSWER
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    # print(len(VIRUS), wall)
    visit = [[False for _ in range(N)] for _ in range(N)]
    no_virus = (N * N) - (wall + len(VIRUS)) # 바이러스에 감염 되지 않은
    time = 0

    for v in virus:
        visit[v[0]][v[1]] = True
        office[v[0]][v[1]] = -1

    while (no_virus > 0):
        if (no_virus == 0):
            ANSWER = min(ANSWER, time)
            return

        new_virus = deque()
        if len(virus) == 0:
            return
        # for v in virus:
            # no_virus -= 1
            # office[v[0]][v[1]] = -1
        while(virus):
            x, y= virus.popleft()
            # no_virus -= 1
            office[x][y] = -1
            for dx, dy in zip(DX, DY):
                nx = x + dx
                ny = y + dy
                if (0 <= nx < N and 0 <= ny < N):
                    if office[nx][ny] == 2 and visit[nx][ny] == False: # 비활성화된 바이러스가 활성 바이러스로 바뀐다.
                        new_virus.append((nx, ny))
                        visit[nx][ny] = True
                        # office[nx][ny] = -2
                        # new_virus.append((nx, ny))
                        # no_virus -= 1
                    elif office[nx][ny] == 0 and visit[nx][ny] == False: # 빈 공간인 경우에 활성 바이러스가 복제가 된다.
                        new_virus.append((nx, ny))
                        visit[nx][ny] = True
                        # office[nx][ny] = -2
                        no_virus -= 1
        virus = nwe_virus # copy.deepcopy(new_virus)

        time += 1
    if time < ANSWER:
        ANSWER = time



# choose_virus(deque(), 0, 0)
for active_virus in combinations(VIRUS, M):
    temp_office = copy.deepcopy(OFFICE)
    q = deque()
    for x, y in active_virus:
        q.append((x, y))
        temp_office[x][y] = -1
    spread(temp_office, q)

if ANSWER == 1e+6:
    print(-1)
else:
    print(ANSWER)