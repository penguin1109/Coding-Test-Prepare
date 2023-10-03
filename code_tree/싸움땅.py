"""
1-1. 자신이 향한 방향으로 한 칸 이동 (격자를 벗어나면 정반대로 방향을 바꾸어 1만큼 이동)
2-1. 이동한 칸에 플레이어가 없고 총이 있으면 본인꺼랑 거기 있는 총들중 제일 센거 선택
2-2-1. 이동한 칸에 플레이어가 있으면 (초기 능력 + 총의 공격력)이 더 큰 플레이어가 이김. 같으면 (초기 능력)이 크면 승
    -> 이때 (초기 능력의 차이) + (총의 공격력 합의 차이)를 이기면 포인트를 따간다.
2-2-2. 지면 총을 내려놓고 자신의 이동 방향으로 한 칸 이동. 
    -> 이동한 칸에 다른 플레이어가 있거나 범위 밖이면 원래 자리에서 90도씩 우회전 하면서 빈칸이 있으면 바로 이동
    -> 칸에 총이 있으면 본인꺼랑 거기 있는 총들 중 제일 센거 선택
2-2-3. 이기면 승리한 칸에 떨어져 있는 총들과 원래 있는 총 중 가장 센 총 선택

===> 위의 과정을 1~n번 플레이어까지 반복

[출력] k번의 라운드 동안 각 플레이어들이 획득한 포인트를 출력하여라.
"""

N, M, K = map(int, input().strip().split(' ')) # 격자의 크기, 플레이어의 수, 라운드의 수

# guns = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 총의 정보 
guns = []
for n in range(N):
    arr = list(map(int, input().strip().split(' ')))
    arr = [[a] for a in arr]
    guns.append(arr)


DX, DY = [0, 1, 0, -1], [-1, 0, 1, 0]
dir_pair = {0:2, 1:3, 2:0, 3:1}
players = []
board = [[-1 for _ in range(N)] for _ in range(N)]

class Player:
    def __init__(self, x, y, d, s, i):
        self.idx = i
        self.x = x-1 # 
        self.y = y-1
        self.d = d # 이동 방향 
        self.s = s # 초기 능력치
        self.gun = 0 # 플레이어의 총의 공격력 
        self.point = 0 # 게임 진행하면서 얻는 포인트

for m in range(M): # 플레이어의 정보는 번호 순서대로 제공이 된다.
    y, x, d, s = map(int, input().strip().split(' ')) # 위치, 방향, 초기 능력치
    new_player = Player(x, y, d, s, m)
    players.append(new_player)
    board[y-1][x-1] = m

def in_range(x, y):
    return (0 <= x < N and 0 <= y < N)

def loser_move(loser):
    global board, players, guns

    x, y = loser.x, loser.y
    guns[y][x].append(loser.gun)
    """ 진 플레이어는 총을 내려 놓고, 그럼 우선은 플레이어 객체의 gun은 0이 되어야 한다.
    """
    loser.gun = 0

    d = loser.d
    nx, ny = x + DX[d], y + DY[d]
    nd = d

    if in_range(nx, ny) == False or board[ny][nx] != -1:
        for i in range(1, 4):
            nd = (d + i) % 4
            nx, ny = x + DX[nd], y + DY[nd]
            if in_range(nx,ny) and board[ny][nx] == -1:
                break

    g = guns[ny][nx]
    if len(g) > 0:
        g = sorted(g, reverse=True)
        loser.gun = g[0]
        guns[ny][nx] = g[1:]

    loser.d = nd # 회전하며 방향 변경
    board[y][x] = -1 
    board[ny][nx] = loser.idx
    loser.x, loser.y = nx, ny
    players[loser.idx] = loser


def winner_move(winner):
    global players, guns, board

    x, y = winner.x, winner.y
    g = guns[y][x]
    g.append(winner.gun)
    g = sorted(g, reverse=True)
    winner.gun = g[0]
    guns[y][x] = g[1:]
    players[winner.idx] = winner

    board[y][x] = winner.idx

def one_player(idx):
    global players, guns, board
    player = players[idx]
    x, y = player.x, player.y
    d = player.d
    nx, ny = x + DX[d], y + DY[d]

    if in_range(nx, ny) == False:
        d = dir_pair[d]
        nx, ny = x + DX[d], y + DY[d]
        player.d = d
    player.x, player.y = nx, ny
    # print(f"IDX : {idx} X, Y: {nx}, {ny}")
    # print(board)
    board[y][x] = -1

    if board[ny][nx] != -1:
        org_player = players[board[ny][nx]]
        op_score = org_player.gun + org_player.s
        score = player.gun + player.s
        if op_score < score:
            winner = player
            loser = org_player
        elif op_score > score:
            winner = org_player
            loser = player
        else:
            if org_player.s > player.s:
                winner = org_player;loser=player
            else:
                winner = player;loser=org_player
    else:
        board[y][x] = -1
        board[ny][nx] = idx
        g = guns[ny][nx]
        g.append(player.gun)
        g = sorted(g, reverse=True)
        player.gun = g[0]
        guns[ny][nx] = g[1:]
        players[player.idx] = player

        return

    winner.point += (winner.s - loser.s) + (winner.gun - loser.gun)

    ## Loser Move ##
    loser_move(loser)
    ## Winner Change ##
    winner_move(winner)


def one_round():
    global players

    for idx in range(M):
        # print(board)
        one_player(idx)
        

for k in range(K):
    one_round()

for player in players:
    print(player.point, end = ' ')
