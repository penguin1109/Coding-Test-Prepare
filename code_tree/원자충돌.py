import sys
sys.stdin = open('./input.txt','r')
readl = sys.stdin.readline

N, M, K = map(int, readl().strip().split(' ')) # 격자의 크기, 원자의 개수, 실험 시간 #
DX, DY = [0, 1, 1, 1, 0, -1, -1, -1], [-1, -1, 0, 1, 1, 1, 0, -1]  # 상하좌우: 0, 2, 4, 6 (전부 짝수) #

class Atom:
    def __init__(self, speed, mass, dir):
        self.speed = speed
        self.mass = mass
        self.dir = dir
board = [[[] for _ in range(N)] for _ in range(N)]

for m in range(M):
    y, x, m, s, d = map(int, readl().strip().split(' '))
    new_atom = Atom(speed=s, mass=m, dir=d)
    board[y-1][x-1].append(new_atom)

def change_pix(x, y):
    if x == -1:x = N-1
    if x == N:x=0
    if y == -1:y = N-1
    if y == N:y = 0
    return x, y


### STEP 1 : 1초마다 원자 이동 ###
def move_atom():
    global board
    new_board = [[[] for _ in range(N)] for _ in range(N)]
    
    for y in range(N):
        for x in range(N):
            for atom in board[y][x]:
                move = atom.speed
                # move %= (N-1)*2
                sx, sy = x, y
                for m in range(move):
                    nx, ny = change_pix(sx + DX[atom.dir], sy + DY[atom.dir])
                    sx, sy = nx, ny
                # print(f"{x}->{sx} {y}->{sy}")
                new_board[sy][sx].append(atom)
    board = new_board
    
### STEP 2 : 한 칸에 2개 이상의 원자가 있으면 합성 진행 ###
def merge(arr):
    new_mass = sum([a.mass for a in arr]) // 5
    new_speed = sum([a.speed for a in arr]) // len(arr)
    dir_check = [a.dir%2 for a in arr]
    
    if sum(dir_check) == len(arr) or sum(dir_check) == 0: # 전부 상하좌우이거나 전부 대각선인 경우 #
        new_dirs = [0, 2, 4, 6]
    else:
        new_dirs = [1,3, 5, 7]
    # print(f"MASS : {new_mass} SPEED : {new_speed} DIR : {new_dirs}")
    if new_mass == 0:
        return []
    new_arr = []
    for i in range(4):
        new_atom = Atom(speed=new_speed, mass=new_mass, dir=new_dirs[i])
        new_arr.append(new_atom)
    return new_arr

        
def merge_atom():
    global board
    new_board = [[[] for _ in range(N)] for _ in range(N)]
    
    for y in range(N):
        for x in range(N):
            nums = len(board[y][x])
            if nums >= 2:
                new_arr = merge(board[y][x])
                new_board[y][x] = new_arr
            else:
                new_board[y][x] = board[y][x]
    board = new_board

def get_mass_sum(board):
    answer = 0
    for y in range(N):
        for x in range(N):
            mass_sum = sum([a.mass for a in board[y][x]])
            answer += mass_sum
    return answer
                
def simulate():
    move_atom()
    merge_atom()
    

for k in range(K):
    simulate()

answer = get_mass_sum(board)
print(answer)
