import sys
input = sys.stdin.readline
'''
- 각각의 말마다 이동 방향이 정해져 있음 (상하좌우 4방 중 하나로 이동 가능)
- 이미 말이 있으면 그 위에 올림
- 이동 칸이 빨간색이면 '순서'를 이동하기 전 뒤집음 (만약에 말이 2개 이상 있으면)
- 이동 칸이 파란색이면 '방향'을 반대로 전환한 다음에 이동. 바꾼 방향의 칸도 파란색이면 가만히 있음.
- 쌓여있는 말은 가장 밑에 있는 말의 방향대로 쌓여있는 말들이 함께 움직임
- 4개 이상의 말들이 겹쳐서 쌓여 있으면 그대로 게임 중지
'''

class Player():
    def __init__(self, x, y, dir, k):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.dir = dir
        self.k = k
        self.up = None
        self.down = None
        
# DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] # 상하좌우 #
DX, DY = [1, -1, 0, 0], [0, 0, -1, 1] # 우좌상하 #
N, K = map(int, input().strip().split(' ')) # 판의 크기, 말의 개수 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
# player_board = [[None for _ in range(N)] for _ in range(N)]
player_board = [[[] for _ in range(N)] for _ in range(N)]
# player_list = []

#### INITIALIZE ####
####################
for k in range(K):
    y, x, d = map(int, input().strip().split(' '))
    # player = Player(x-1, y-1, d-1, k)
    # player_board[y-1][x-1] = player
    # player_board[y-1][x-1].append(player)
    player_board[y-1][x-1].append((k, d-1))
    # player_list.append(player)
####################

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def reverse_order(player):
    p = player
    temp = [p]
    while (p.up is not None):
        temp.append(p.up)
    
    for i in range(len(temp)-1, -1, -1):
        temp_p = temp[i]
        temp_p.up = None if i == 0 else temp[i-1]
        temp_p.down = None if i == len(temp)-1 else temp[i+1]
        temp[i] = temp_p
        
    return temp[0]

DIR_DICT={0:1,1:0,2:3,3:2}
def change_dir_check(player):
    org_dir = player.dir
    new_dir = DIR_DICT[org_dir]
    nx, ny = player.x + DX[new_dir], player.y + DY[new_dir]
    if in_range(nx, ny):
        if board[ny][nx] == 2:
            player.dir = new_dir
            return player
        elif board[ny][nx] == 1:
            player = reverse_order(player)
            
def find_player_idx(idx):
    for y in range(N):
        for x in range(N):
            for number, dir in player_board[y][x]:
                if number == idx:
                    return (x, y, dir)

def pop_top(x, y, idx):
    for i, (num, dir) in enumerate(player_board[y][x]):
        if num == idx:
            to_remove = player_board[y][x][i:]
            del player_board[y][x][i:]
            return to_remove

def move(x, y, to_move, do_reverse):
    if do_reverse:
        to_move = to_move[::-1]
    player_board[y][x].extend(to_move)
    
def play():
    for k in range(K):
        temp_x, temp_y, temp_dir = find_player_idx(idx=k)
        dx, dy = DX[temp_dir], DY[temp_dir]
        
        nx, ny = temp_x + dx, temp_y + dy # 그냥 이동한 위치가 흰색인 경우에는 여기로 이동 #
        need_reverse = False
        
        if in_range(nx, ny) == False or board[ny][nx] == 2: # 이동한 위치가 파란색이거나 격자 안에 있지 않을 떄 #
            temp_dir = DIR_DICT[temp_dir]
            nx, ny = temp_x + DX[temp_dir], temp_y + DY[temp_dir]
            
            if in_range(nx, ny) == False or board[ny][nx] == 2: # 방향 바꿔서 이동한 위치도 마찬가지일 때 #
                nx, ny = temp_x, temp_y # 그냥 원래 자리 그대로 위치 #
                
            elif board[ny][nx] == 1: # 방향 바꿔서 이동한 위치가 빨간색일 때 #
                need_reverse = True
                
        elif board[ny][nx] == 1: # 이동한 위치가 빨간색인 경우 #
            need_reverse = True
        
        to_move = pop_top(temp_x, temp_y, k) # 원래 위치에서 그 위에 있는 애들 없앰 #
        # print(to_move)
        to_move[0] = (k, temp_dir) # 처음 player의 방향만 바꾸면 됨 #
        move(nx, ny, to_move, do_reverse=need_reverse)
        # print(player_board)
        if len(player_board[ny][nx]) >= 4:
            return True
    return False


for time in range(1, 1001):
    do_stop = play()
    if do_stop:
        print(time)
        exit(0)
print(-1)
    
    