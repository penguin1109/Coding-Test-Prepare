import sys
input = sys.stdin.readline

N, M, K = map(int, input().strip().split(' ')) # 격자 크기, 원자 개수, 실험 시간 #
DX, DY = [0, 1, 1, 1, 0, -1, -1, -1], [-1, -1, 0, 1, 1, 1, 0, -1] # 상 부터 시계방향 #
class Atom:
    def __init__(self, x, y, mass, speed, dir):
        self.x = x
        self.y = y
        self.m = mass
        self.s = speed
        self.d = dir
ATOMS = []
# board = [[[] for _ in range(N)] for _ in range(N)]

def new_loc(a,b, speed, dir):
    x = a + speed * DX[dir];y = b + speed * DY[dir]
    x %= (2 * N);y %= (2 * N)
    x %= N;y %= N
    if x < 0:
        x += N
    if y < 0:
        y += N
    # print(a, b, speed, dir, x, y)
    return x, y
        
def move_one_step():
    new_board = [[[] for _ in range(N)] for _ in range(N)]
    NEW_ATOM = []
    for i, atom in enumerate(ATOMS):
        # atom = board[y][x]
        x, y = atom.x, atom.y
        new_x, new_y = new_loc(x, y, atom.s, atom.d)
        new_board[new_y][new_x].append(atom)
    # print(new_board)
    for y in range(N):
        for x in range(N):
            if len(new_board[y][x]) >= 2:
                total_mass = sum([a.m for a in new_board[y][x]])
                total_speed = sum([a.s for a in new_board[y][x]])
                total_dir = sum([a.d % 2 for a in new_board[y][x]])
                new_mass = total_mass // 5
                new_speed = total_speed // len(new_board[y][x])
                if new_mass == 0:
                    continue
                if total_dir == 0 or total_dir == len(new_board[y][x]):
                    DIRS = list(range(0, 8, 2))
                else:
                    DIRS = list(range(1, 8, 2))
                NEW_ATOM.append(Atom(x, y, new_mass, new_speed, DIRS[0]))
                NEW_ATOM.append(Atom(x, y, new_mass, new_speed, DIRS[1]))
                NEW_ATOM.append(Atom(x, y, new_mass, new_speed, DIRS[2]))                
                NEW_ATOM.append(Atom(x, y, new_mass, new_speed, DIRS[3]))
                
            elif len(new_board[y][x]) == 1:
                org_atom = new_board[y][x][0]
                new_atom = Atom(x, y, org_atom.m, org_atom.s, org_atom.d)
                # NEW_ATOM.append(new_board[y][x][0])
                NEW_ATOM.append(new_atom)
    
    return NEW_ATOM

                
                
for m in range(M):
    y, x, m, s, d = map(int, input().strip().split(' '))
    new_atom = Atom(x-1, y-1, m, s, d)
    ATOMS.append(new_atom)
    # board[y-1][x-1].append(new_atom)
for k in range(K):
    ATOMS = move_one_step()
answer = sum([a.m for a in ATOMS])
print(answer)

    