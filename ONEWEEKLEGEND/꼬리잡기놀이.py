""" 꼬리잡기놀이
<조건>
- nxn 크기의 격자판.
- 각 팀의 이동선은 끝이 이어져 있고, 서로 겹치지 않는다.
1. 각 팀은 <머리사람>을 따라서 한 칸 이동
2. 각 라운드마다 공이 정해진 선을 따라서 던져진다. (오 - 위 - 왼 - 아래)
3. 공이 던져지는 경우에 해당선에 최초로 만나는 사람만이 공을 얻어 점수를 얻는다.
    - 점수 = 해당 사람이 <머리사람>으로부터 팀 내에서 k번째 사람이라면 k^2만큼 점수를 얻는다.
    - 점수를 얻은 뒤에는 머리사람과 꼬리 사람이 바뀜 (=방향이 바뀜 =동일 묶음에 있는 사람들의 방향이 모두 동일한 만큼 바뀐다.)
4. 한 라운드가 끝나면 모든 팀이 1칸이동

<입력>
총 격자의 크기, 각 팀의 위치, 각 팀의 이동선, 총 진행하는 라운드의 수

<문제>
k번의 라운드 동안 각 팀이 얻게 되는 점수의 총합을 출력하여라.
"""

N, M, K = map(int, input().strip().split(' ' )) # 격자 크기, 팀의 개수, 라운드의 수
board = [[0 for _ in range(N+1)]]
for n in range(N):
    row = list(map(int, input().strip().split(' ')))
    board.append([0] + row) # 0: 빈칸 1: 머리사람 2: 나머지 3: 꼬리 사람 4: 이동선

V = [[] for _ in range(M+1)]
tail = [0 for _ in range(M+1)] # 각 팀별 꼬리사람의 V에서의 index를 관리한다.
visited = [
    [False for _ in range(N+1)] for _ in range(N+1)
]
board_idx = [
    [0 for _ in range(N+1)] for _ in range(N+1)
] # 각 팀별 이동 경로에 해당하는 곳에 팀 번호를 저장해 둔다.

answer = 0
DX, DY = [-1, 0, 1, 0], [0, -1, 0, 1]

def check_range(x, y):
    return (1 <= x <= N and  1 <= y <= N)

def dfs(x, y, idx):
    visited[x][y] = True
    board_idx[x][y] = idx
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy
        if check_range(nx, ny) == False:
            continue
        if visited[nx][ny]:
            continue
        if board[nx][ny] == 0:
            continue
        if len(V[idx]) == 1 and board[nx][ny] != 2: # 애초에 어떤 팀의 경로도 아닌 경우에
            continue
        V[idx].append((nx, ny)) # idx번째 팀의 경로이다.
        if board[nx][ny] == 3:
            tail[idx] = len(V[idx])
        dfs(nx, ny, idx)

def init():
    cnt = 1
    for i in range(1,N+1):
        for j in range(1,N+1):
            if board[i][j] == 1:
                V[cnt].append((i, j))
                cnt += 1
    for i in range(1,M+1):
        x, y = V[i][0] # 머리 사람만을 넣어줌.
        dfs(x, y, i)


def reverse(idx):
    if idx == 0: # 어떤 팀도 공을 받지 못한 경우에
        return
    new_v = []
    for j in range(tail[idx]-1, -1, -1):
        new_v.append(V[idx][j])
    for j in range(len(V[idx])-1, tail[idx]-1, -1):
        new_v.append(V[idx][j])
    V[idx] = new_v[:]
    for j, (x,y) in enumerate(V[idx]):
        if j == 0: # 머리 사람
            board[x][y] = 1
        elif j < tail[idx]-1:
            board[x][y] = 2
        elif j == tail[idx]-1: # 꼬리 사람
            board[x][y] = 3
        else:
            board[x][y] = 4

def move_all():
    for i in range(1, M+1):
        tmp = V[i][-1] # 머리사람
        for j in range(len(V[i])-1, 0, -1):
            V[i][j] = V[i][j-1]
        V[i][0] = tmp
    for i in range(1, M+1):
        for j, (x, y) in enumerate(V[i]):
            if j == 0:
                board[x][y] = 1
            elif j < tail[i]-1:
                board[x][y] = 2
            elif j == tail[i]-1:
                board[x][y] = 3
            else:
                board[x][y] = 4

def get_score(x, y):
    global answer
    idx = board_idx[x][y]
    cnt = V[idx].index((x, y))
    answer += (cnt + 1) * (cnt+1)

def throw_ball(turn):
    t = (turn - 1) % (4 *N) + 1
    if t <= N: # 1~N라운드에 해당하는 경우에 왼쪽에서 오른쪽으로
        for i in range(1,N+1):
            if 1 <= board[t][i] and board[t][i] <= 3:
                get_score(t, i)
                return board_idx[t][i]
    elif t <= 2 * N:
        t -= N
        for i in range(1, N+1):
            if 1 <= board[N-i+1][t] <= 3:
                get_score(N-i+1, t)
                return board_idx[N+1-i][t]
    elif t<= 3 * N:
        t -= (2 * N)
        for i in range(1,N+1):
            if  1 <= board[N-t+1][N-i+1] <= 3:
                get_score(N-t+1, N-i+1)
                return board_idx[N-t+1][N-i+1]
    else:
        t -= (3 *N)
        for i in range(1,N+1):
            if 1 <= board[i][N-t+1] <= 3:
                get_score(i, N-t+1)
                return board_idx[i][N-t+1]
    return 0


init()
for i in range(K):
    move_all()
    got_ball_idx = throw_ball(i+1)
    reverse(got_ball_idx)
print(answer)