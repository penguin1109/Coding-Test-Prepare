""" 싸움땅
- nxn의 크기의 격자. 빨간색 배경의 숫자는 총의 경우 공격력을, 플레이어의 경우 초기 능력치를 의미하고, 노란색 배경의 숫자는 플레이어의 번호를 의미한다.
1. 첫번째 플레이어부터 순차적으로 본인이 향하고 있는 방향대로 한칸이동. 그 방향에서 격자를 벗어나면 방향을 바꾸어 1만큼 이동
2-1. 이동한 방향에 플레이어가 없다면 해당 칸에 총이 있으면 플레이어는 총을 얻고, 이미 갖고 있다면 더 공격력이 쎈 총을 획득
2-2-1. 이동한 방향에 플레이어가 있다면 (초기 능력치 + 총의 공격력)이 더 큰 플레이어가 이기게 된다. 같으면 (초기 능력치)로 비교. 이긴 플레이어는 (초기 능력치-총의 공격력의 합)을 포인트로 얻는다.
2-2-2. 진 플레이어는 원래 방향으로 이동한다. 역시나 이동하려는 칸에 다른 플레이어가 있거나 범위 밖이면 **오른쪽으로 90도 회전**하여 빈칸으로 이동한다. 총이 있으면 더 공격력이 높은 총 획득
2-2-3. 이긴 플레이어도 가장 공격력이 높은 총을 획득
==> k 라운드 동안 게임을 진행하면서 각 플레이어들이 획득한 포인트를 출력하여라.
"""

""" 주의
# 1 <= x,y <= n
    -> 그치만 나는 0 <= x, y < n으로 저장해서 사용할 것임.
# 90도 회전은 (dir + 1) % 3으로 구현하면 된다.
# 플레이어의 초기 위치에는 총이 존재하지 않는다.
# 게임이 시작한 이후에는 한 칸에 플레이어와 총이 동시에 존재하는 것이 가능하다.
# 게임판에 총은 여러개 존재할 수 있다.
"""

import heapq

N, M, K = map(int, input().split())  # 격자의 크기, 플레이어의 수, 라운드의 수
DX, DY = [-1, 0, 1, 0], [0, 1, 0, -1]

guns = [[[] for _ in range(N)] for _ in range(N)]
for n in range(N):
    temp = list(map(int, input().split(' ')))
    for idx, t in enumerate(temp):
        if t != 0:
            heapq.heappush(guns[n][idx], -t) # 총이 없으면 0, 나머지는 총의 공격력

player_points = [0 for _ in range(M)]  # 플레이어의 포인트를 저장
players = [] # 플레이어들의 정보를 일괄적으로 저장
# player_info = []
for i in range(M):
    x, y, d, s = map(int, input().split(' '))  # 플레이어의 위치, 방향, 초기 능력치
    players.append([x - 1, y - 1, d, s, 0]) # 플레이어의 위치, 방향, 초기 능력치, 총의 공격력

assert len(players) == M

def check_player(x, y):
    for p in players:
        if p[0] == x and p[1] == y:
            return True
    return False

def get_player_info(x, y):
    for idx, p in enumerate(players):
        if p[0] == x and p[1] == y:
            return idx

def play():
    global guns, players
    for m in range(M):
        x, y, d, s, gun = players[m]

        # (1) 플레이어는 움직인다.
        nx, ny = x + DX[d], y + DY[d]
        if (0 > nx or nx >= N or 0 > ny or ny >= N):  # 격자를 넘는 경우에 정반대로 방향을 바꾸어 1만큼 이동한다.
            d = (d + 2) if d < 2 else (d - 2)
            nx, ny = x + DX[d], y + DY[d]
            players[m][2] = d

        if check_player(nx, ny) == False:  # 다른 플레이어는 없음
            #  총 교환
            if gun != 0:
                heapq.heappush(guns[nx][ny], -gun)  # 더 경쟁력이 높은 총이 존재하는 경우 교환.
                new_gun = heapq.heappop(guns[nx][ny]) * -1
                players[m][-1] = new_gun
            else:
                if guns[nx][ny]:
                    new_gun = heapq.heappop(guns[nx][ny]) * -1
                    players[m][-1] =new_gun
            players[m][0] = nx;players[m][1] = ny;


        else:  # 다른 플레이어가 있는 경우
            me = s + gun
            other_player_idx = get_player_info(nx, ny)
            other_player = players[other_player_idx]
            other = other_player[3] + other_player[-1]
            players[m][0] = nx;
            players[m][1] = ny
            if (me, s) > (other, other_player[3]):
                update_fight(m, other_player_idx, nx, ny)

            else:
                update_fight(other_player_idx, m, nx, ny)


def update_fight(winner, loser, win_mx, win_my):
    # 싸우고 이긴 플레이어의 번호, 진 플레이어의 번호를 입력으로 받는다.
    global board, players, player_points
    winner_info = players[winner]
    loser_info = players[loser]

    # (1) 이긴 플레이어의 포인트 추가

    # print(f"WINNER: {winner_info[3] + winner_info[-1]} LOSER: {loser_info[3] + loser_info[-1]}")
    player_points[winner] += ((winner_info[3] + winner_info[-1]) - (loser_info[3] + loser_info[-1]))

    # win_mx, win_my = loser_info[0], loser_info[1]

    # (2) 진 플레이어는 총을 내려놓고 **이동**한다.
    x, y, d = loser_info[0], loser_info[1], loser_info[2]
    loser_gun = loser_info[-1]
    if loser_gun != 0:
        heapq.heappush(guns[x][y], -loser_gun) # 총 내림
        # heapq.heappush(guns[win_mx][win_my], -loser_gun)
    loser_info[-1] = 0
    cnt = 0
    while True:
        nx, ny = x + DX[d], y + DY[d]
        if (0 <= nx < N and 0 <= ny < N) and check_player(nx, ny) == False:  # 이동하려는 위치에 다른 플레이어가 없다면
            if guns[nx][ny] != []:
                new_gun = heapq.heappop(guns[nx][ny]) * -1
                loser_info[-1] = new_gun
            else:
                loser_info[-1] = 0
            loser_info[0] = nx;
            loser_info[1] = ny
            players[loser] = loser_info # 플레이어의 위치 업데이트
            break
        d = (d + 1) % 4  # 오른쪽으로 90도 회전
        cnt += 1
    loser_info[2] = d

    players[loser] = loser_info

    # (3) 이긴 플레이어는 진 플레이어의 총 교환 등이 끝나면 역시나 총들중 가장 공격력이 높은 총을 획득한다.
    # 이긴 플레이어는 이동은 하지 않는다.
    winner_gun = winner_info[-1]
    x, y = winner_info[0], winner_info[1]
    if winner_gun != 0:
        heapq.heappush(guns[win_mx][win_my], -winner_gun)
        new_gun = heapq.heappop(guns[win_mx][win_my]) * -1
        winner_info[-1] = new_gun
    else:
        if guns[win_mx][win_my]:
            new_gun = heapq.heappop(guns[win_mx][win_my]) * -1
            winner_info[-1] = new_gun
    winner_info[0] = win_mx;winner_info[1] = win_my;
    players[winner] = winner_info


for k in range(K):
    play()

for m in range(M):
    print(player_points[m], end=' ')










