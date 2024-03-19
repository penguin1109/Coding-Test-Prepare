import sys
input = sys.stdin.readline
'''
- 턴이 한번 진행될 때 한 칸씩 이동
- 독점 계약은 k만큼의 턴 동안 유효 (k번 이후 주인 없는 칸이 됨)
- 각 플레이어는 방향 별 우선 순위가 존재. (우선은 독점 계약이 없는 칸으로, 그런게 없으면 자신이 독점 계약한 땅으로 이동)
- 모든 플레이어 이동 후 여러 플레이어가 있으면 제일 작은 번호를 갖는 플레이어만 살아남음.

**중요: 모든 플레이어는 동시에 이동함**

[출력] 1번 플레이어만 살아남기까지 걸린 턴의 수
'''
DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] # 상하좌우 #
DIR_DICT = {
    0 : [0,1,2,3], 1 : [1,0,3,2], 2 : [2,3,1,0], 3 : [3,2,0,1]
}
class Player:
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.view_dir = -1
        self.priority = [-1, -1, -1, -1]
        self.is_dead = False
        
N, M, K = map(int, input().strip().split(' ')) # 격자의 크기, 플레이어의 수, 독점 계약 턴 수 #

players = [Player(-1, -1) for _ in range(K+1)]
board = [[[] for _ in range(N)] for _ in range(N)]
position = [[-1 for _ in range(N)] for _ in range(N)]

## (1) get all inputs ##
for n in range(N):
    arr = list(map(int, input().strip().split(' '))) # 플레이어 정보 #
    # board.append(arr)
    for x in range(N):
        if arr[x] != 0:
            players[arr[x]] = Player(x, n)
        board[n][x].append([arr[x], K])
        position[n][x] = arr[x]

view_dirs = list(map(int, input().strip().split(' ')))
for di, view_dir in enumerate(view_dirs):
    players[di+1].view_dir = view_dir - 1

for m in range(M):
    prior = list(map(int, input().strip().split(' ')))
    players[m+1].priority = [i-1 for i in prior]
    
## (2) 
def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def update_all():
    global board
    '''K시간이 지나면 각 칸의 독점 계약이 해제되기 떄문!'''
    for y in range(N):
        for x in range(N):
            new_arr = []
            for (idx, time_left) in board[y][x]:
                if time_left - 1 == 0:
                    continue
                new_arr.append((idx, time_left-1))
            board[y][x] = new_arr
        
def move_all_players():
    global players, board
    '''모든 player을 움직이게 함.'''
    for pi in range(1, M+1):
        player = players[pi]
        if player.is_dead == True:
            continue
        
        self_piece = None
        do_stop = False;valid = False
        for direction in player.priority:
            move_dir = DIR_DICT[player.view_dir][direction]
            nx, ny = player.x + DX[move_dir], player.y + DY[move_dir]
            if in_range(nx, ny):
                if len(board[ny][nx]) == 0: # 아무도 독점 계약을 맺지 않은 경우 #
                    if position[ny][nx] != -1 and position[ny][nx] > pi or position[ny][nx] == -1:
                        if position[ny][nx] > pi:
                            org_pi = position[ny][nx]
                            players[org_pi].is_dead = True
                        board[ny][nx].append((pi, K+1)) # board에 현재 플레이어가 독점 계약을 맺었음을 저장 #
                        players[pi].x, players[pi].y = nx, ny # 플레이어의 위치도 업데이트 #
                        players[pi].view_dir = move_dir # 플레이어가 보고 있는 방향 변경 #
                        do_stop = True;valid = True
                    else:
                        players[pi].is_dead = True
                        do_stop = True
                        valid = True
                        
                elif self_piece is None:
                    for info in board[ny][nx]:
                        if info[0] == pi:
                            self_piece = (nx, ny, move_dir)
            if do_stop:
                break           
        if valid == False:
            nx,ny, move_dir = self_piece
            # board[ny][nx].append((pi, K+1))
            players[pi].view_dir = move_dir
            players[pi].x, players[pi].y = nx, ny
                            
def play():
    move_all_players
        
            
    