import sys

sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

Q = int(readl().strip()) # 명령의 수 #
rabbits = []
import heapq
class Rabbit:
    def __init__(self, pid, x, y,  jump):
        super(Rabbit, self).__init__()
        self.pid = pid
        self.x = x
        self.y = y
        self.jump = jump

first_command = list(map(int, readl().strip().split(' ')))
N, M, P = first_command[1:4]
idx = 0
PID_MAP = {}
did_run = [False for _ in range(P)]
scores = [0 for _ in range(P)]
point = [[0, 0] for _ in range(P)]
jump_cnt = [0 for _ in range(P)]
dist_arr = [0 for _ in range(P)]

for p in range(4, len(first_command), 2):
    pid, dist = first_command[p:p+2]
    new_rabbit = Rabbit(pid, 0, 0, 0)
    rabbits.append(new_rabbit)
    PID_MAP[pid] = idx
    dist_arr[idx] = dist
    idx += 1

total_sum = 0



###### CMD 200 : 경주를 진행함 ######
def in_range(x, y):
    return (0 <= x < M and 0 <= y < N)

DIR_DICT = {0 : 1, 1 : 0, 2 : 3, 3 : 2}

def race(K, S):
    global rabbits, did_run, total_sum
    DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0]
    did_run = [False for _ in range(P)]
    for k in range(K):
        # (1) 우선순위가 제일 높은 토끼 뽑기 #
        rabbits.sort(key = lambda x : (x.jump, x.x+x.y, x.y, x.x, x.pid))
        highest = rabbits[0]
        # print(highest.pid)
        hx, hy = highest.x, highest.y
        q = []
        for idx in range(4):
            sx, sy = hx, hy;dx, dy = DX[idx], DY[idx]
            move_dist = dist_arr[PID_MAP[highest.pid]]
            
            if idx <= 1: # 상-하로 움직이는 경우 # 
                move_dist %= ((N-1)*2)
            else: # 좌-우로 움직이는 경우 #
                move_dist %= ((M-1)*2)
            di = idx
            for d in range(move_dist):
                nx, ny = sx + dx, sy + dy
                if in_range(nx, ny) == False:
                    di = DIR_DICT[di]
                    dx, dy = DX[di], DY[di]
                    nx, ny = sx + dx, sy + dy
                sx, sy = nx, ny
            # print("SX", sx, "SY", sy)
            q.append([sx+sy, sx, sy])
                
        q.sort(key = lambda x : (-x[0], -x[2], -x[1]))
        new_pos = q[0]
        ri, ci = new_pos[2], new_pos[1]
        # print(ri, ci)
        scores[PID_MAP[highest.pid]] -= (ri + ci+2)
        total_sum += (ri + ci+2)
        rabbits[0] = Rabbit(highest.pid, ci, ri, highest.jump+1)
        point[PID_MAP[highest.pid]] = [ri, ci]
        jump_cnt[PID_MAP[highest.pid]] = highest.jump+1
        did_run[PID_MAP[highest.pid]] = True
        
        
    # (2) 추가 점수를 받을 토끼 찾기 #
    rabbits.sort(key = lambda x : (-x.x-x.y, -x.y, -x.x, -x.pid))
    for i in range(P):
        temp = rabbits[i]
        if did_run[PID_MAP[temp.pid]] == False:
            continue
        else:
            break
    scores[PID_MAP[temp.pid]] += S
    

###### CMD 300 : 고유 번호가 pid인 토끼의 이동거리를 L배 늘려줌 ######
def change_movedist(pid, L):
    global dist_arr
    
    idx = PID_MAP[pid]
    dist_arr[idx] *= L
                    

####### CMD 400 : 제일 점수가 높은 토끼 선택 ########
def highest_score():
    answer = 0
    for i in range(P):
        answer = max(answer, scores[i] + total_sum)         
    return answer
                
            
        
        
for q in range(1, Q):
    cmd = list(map(int, readl().strip().split(' ')))
    # print(scores, total_sum)
    if cmd[0] == 200:
        K, S = cmd[1:]
        race(K, S)
    elif cmd[0] == 300:
        pid, L = cmd[1:]
        change_movedist(pid, L)
    elif cmd[0] == 400:
        answer = highest_score()
        print(answer)