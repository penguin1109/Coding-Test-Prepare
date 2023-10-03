""" 14502: 연구소
- NxM 크기의 연구소가 있고, 여기서 1x1 크기의 정사각형으로 나누어져 있다
- 바이러스는 상하좌우로 인접한 빈 칸으로 모두 퍼져나갈 수 있다. 
- 새로 세울 수 있는 벽은 3개이며, 반드시 3개를 세워야 한다.
- 0: 빈칸 1: 벽 2: 바이러스
- 벽을 3개 세운 뒤에 바이러스가 퍼질 수 없는 곳을 안전영역이라고 한다면 안전 영역의 최대 크기를 구하여라
"""
## 문제를 해결하기 위해서는 벽을 3개 이내로 세운 뒤에 바이러스가 퍼진 상황을 봐야 하는 것이다.
from copy import deepcopy
from collections import deque
global N, M
answer = 0
def spread(space):
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    area = N*M
    check = deque()
    for i in range(N):
        for j in range(M):
            if space[i][j] == 2:
                check.append((i,j))
            elif space[i][j] == 1:
                area -= 1
 
    area -= len(check)
    while check:
        x,y = check.pop()
    
        for d in range(4):
            nx, ny = x + dx[d], y + dy[d]
            if (0 <= nx < N and 0 <= ny < M and space[nx][ny] == 0):
                space[nx][ny] = 2
                area -= 1
                check.append((nx, ny))

    return area


def buildwall(start, cnt, space):
    global answer
    if cnt == 0:
        answer = max(answer, spread(deepcopy(space)))
        return
    for i in range(start, N*M):
        x, y = i // M, i % M
        if space[x][y] == 0:
            space[x][y] = 1
            buildwall(i+1, cnt-1, space)
            space[x][y] = 0


    



org_wall = 0
N, M = map(int, input().split(' ')) # 세로, 가로
space = []
for _ in range(N):
    temp = list(map(int, input().split(' ')))
    org_wall += temp.count(1)
    space.append(temp)


buildwall(0,3,deepcopy(space))
print(answer)


