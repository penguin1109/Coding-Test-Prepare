"""
routes = [[(x1, y1), (x2, y1) ..], [], []] ==> 각 군집의 머리 사람 -> 2 -> 꼬리 사람까지의 경로 좌표
teams = [[0,1,..], [], ..] ==> routes에서 각 팀의 좌표들의 순서
teams_dir = [-1, 1, -1,..] ==> 시계 방향인지 시계 반대 방향인지
"""

import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

N, M, K = map(int, readl().strip().split(' '))
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]

v = [[0 for _ in range(N)] for _ in range(N)]
DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
routes = []
teams = []
teams_dir = [-1 for _ in range(M)]
team_track = [[-1 for _ in range(N)] for _ in range(N)]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

team_cnt = 0

for i in range(N):
    for j in range(N):
        if board[j][i] == 1: # 머리사람을 발견함! 
            temp = [[i, j]] # (x, y의 순서)
           
            ## 머리 사람 -> 2인 사람 -> 꼬리 사람의 순서로 탐색을 할 예정 ##
            visited = [[False for _ in range(N)] for _ in range(N)]
            visited[j][i] = True
            from collections import deque
            q = deque([[i, j]])
            people_cnt = 1
            team_track[j][i] = team_cnt
            while q:
                x, y = q.popleft()
                curr = board[y][x]
                for dx, dy in zip(DX, DY):
                    nx, ny = x + dx, y + dy
                    if in_range(nx, ny) and visited[ny][nx] == False and curr <= board[ny][nx] <= curr + 1:
                        
                        temp.append([nx, ny])
                        q.append([nx, ny])
                        visited[ny][nx] = True
                        team_track[ny][nx] = team_cnt
                        if board[ny][nx] != 4:
                            people_cnt += 1
            routes.append(temp)
            # print(temp)
            teams.append([i for i in range(people_cnt)])
            team_cnt += 1 # 군집 번호 업데이트 

def move():
    for i in range(len(teams)):
        d = teams_dir[i] # 현재 군집의 이동 방향
        """
        둘레를 따라서 이동하는 것을 구현하기 위해서 직접 격자 위에서 복잡하게 생각할 것 없이
        v 배열안에 좌표들은 그대로 있음에도 
        오른쪽으로 한칸 이동한다고 생각할 때 
        [0,1,2,3,4]의 순서에서 [1,2,3,4,0]의 순서로 바뀌는 것이다
        """
        for pid in range(len(teams[i])):
            teams[i][pid] = (teams[i][pid] + d) % len(routes[i]) 

def throw_ball():
    global time, answer
    temp = time % (4*N)
    
    team_idx = -1
    ppl_idx = -1
    if 0 <= temp < N: ## 공이 오른쪽으로 던져지는 경우 ##
        row = temp
        for i in range(N):
            team_idx = team_track[row][i]
            # print(f"Team IDX : {team_idx}")
            for pid, ppl in enumerate(teams[team_idx]):
                px, py = routes[team_idx][ppl]
                if px == i and py == row:
                    ppl_idx = pid
                    reverse(team_idx, ppl_idx)
                    return
                    
    elif N <= temp < 2*N: ## 공이 위로 던져지는 경우 ##
        col = temp - N
        for i in range(N-1, -1, -1):
            team_idx = team_track[i][col]
            for pid, ppl in enumerate(teams[team_idx]):
                px, py = routes[team_idx][ppl]
                if px == col and py == i:
                    ppl_idx = pid
                    reverse(team_idx, ppl_idx)
                    return
    elif 2*N <= temp < 3*N: ## 공이 왼쪽으로 던져지는 경우 ##
        row = 3*N - temp - 1
        for i in range(N-1, -1, -1):
            team_idx = team_track[row][i]
            for pid, ppl in enumerate(teams[team_idx]):
                px, py = routes[team_idx][ppl]
                if px == i and py == row:
                    ppl_idx = pid
                    reverse(team_idx, ppl_idx)
                    return
    elif 3*N <= temp < 4*N: ## 공이 아래로 던져지는 경우 ##
        col = (4*N - temp) - 1
        for i in range(N):
            team_idx = team_track[i][col]
            for pid, ppl in enumerate(teams[team_idx]):
                px, py = routes[team_idx][ppl]
                if px == col and py == i:
                    ppl_idx = pid
                    reverse(team_idx, ppl_idx)
                    return
    reverse(team_idx, ppl_idx)
    return

def reverse(team_idx, ppl_idx):
    global teams_dir, teams, answer
    if ppl_idx != -1:
        # print(f"Team : {team_idx} Person : {ppl_idx} INDXES: {routes[team_idx][teams[team_idx][ppl_idx]]}")
        answer += (ppl_idx + 1) ** 2
        teams[team_idx] = teams[team_idx][::-1]
        teams_dir[team_idx] *= -1 # 이동 방향 반대로 바꿔주기         
            
############ MAIN ##############
answer = 0
for time in range(K):
    move()
    # print(team_track)
    throw_ball()

print(answer)