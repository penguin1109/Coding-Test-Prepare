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
    def __lt__(self, other):
        if self.jump != other.jump:
            return self.jump < other.jump
        if self.x + self.y !=   other.x + other.y:
            return self.x + self.y < other.x + other.y
        if self.y != other.y:
            return self.y < other.y
        if self.x != other.x:
            return self.x < other.x
        return self.pid < other.pid

def compare(a, b):
    if a.x + a.y != b.x + b.y:
        return a.x + a.y < b.x + b.y
    if a.y != b.y:
        return a.y < b.y
    if a.x != b.x:
        return a.x < b.x
    return a.pid < b.pid

    
first_command = list(map(int, readl().strip().split(' ')))
N, M, P = first_command[1:4]
idx = 1
PID_MAP = {}
did_run = [False for _ in range(P+1)]
scores = [0 for _ in range(P+1)]
point = [[1,1] for _ in range(P+1)]
jump_cnt = [0 for _ in range(P+1)]
dist_arr = [0 for _ in range(P+1)]
pid_arr = [0 for _ in range(P+1)]

for p in range(4, len(first_command), 2):
    pid, dist = first_command[p:p+2]
    PID_MAP[pid] = idx
    dist_arr[idx] = dist
    pid_arr[idx] = pid
    idx += 1
total_sum = 0

# 토끼를 위로 이동시킵니다.
def get_up_rabbit(cur_rabbit, dis):
    global N;n = N
    up_rabbit = cur_rabbit
   # up_rabbit.x += 1;up_rabbit.y += 1
    dis %= 2 * (n - 1)

    if dis >= up_rabbit.y - 1:
        dis -= (up_rabbit.y - 1)
        up_rabbit.y = 1
    else:
        up_rabbit.y -= dis
        dis = 0

    if dis >= n - up_rabbit.y:
        dis -= (n - up_rabbit.y)
        up_rabbit.y = n
    else:
        up_rabbit.y += dis
        dis = 0

    up_rabbit.y -= dis
    # up_rabbit.x -= 1;up_rabbit.y -= 1

    return up_rabbit


# 토끼를 아래로 이동시킵니다.
def get_down_rabbit(cur_rabbit, dis):
    global N;n = N
    down_rabbit = cur_rabbit
    # down_rabbit.x += 1;down_rabbit.y  +=1
    dis %= 2 * (n - 1)

    if dis >= n - down_rabbit.y:
        dis -= (n - down_rabbit.y)
        down_rabbit.y = n
    else:
        down_rabbit.y += dis
        dis = 0

    if dis >= down_rabbit.y - 1:
        dis -= (down_rabbit.y - 1)
        down_rabbit.y = 1
    else:
        down_rabbit.y -= dis
        dis = 0
    
    down_rabbit.y += dis
    # down_rabbit.x -= 1;down_rabbit.y -= 1
    return down_rabbit


# 토끼를 왼쪽으로 이동시킵니다.
def get_left_rabbit(cur_rabbit, dis):
    global M;m = M
    left_rabbit = cur_rabbit
    # left_rabbit.x += 1;left_rabbit.y += 1
    dis %= 2 * (m - 1)

    if dis >= left_rabbit.x - 1:
        dis -= (left_rabbit.x - 1)
        left_rabbit.x = 1
    else:
        left_rabbit.x -= dis
        dis = 0

    if dis >= m - left_rabbit.x:
        dis -= (m - left_rabbit.x)
        left_rabbit.x = m
    else:
        left_rabbit.x += dis
        dis = 0

    left_rabbit.x -= dis
    # left_rabbit.x -= 1;left_rabbit.y -= 1
    return left_rabbit


# 토끼를 오른쪽으로 이동시킵니다.
def get_right_rabbit(cur_rabbit, dis):
    global M;m = M
    right_rabbit = cur_rabbit
    # right_rabbit.x += 1;right_rabbit.y += 1
    dis %= 2 * (m - 1)

    if dis >= m - right_rabbit.x:
        dis -= (m - right_rabbit.x)
        right_rabbit.x = m
    else:
        right_rabbit.x += dis
        dis = 0

    if dis >= right_rabbit.x - 1:
        dis -= (right_rabbit.x - 1)
        right_rabbit.x = 1
    else:
        right_rabbit.x -= dis
        dis = 0
    
    right_rabbit.x += dis

    # right_rabbit.x -= 1;right_rabbit.y -= 1
    return right_rabbit



###### CMD 200 : 경주를 진행함 ######
def in_range(x, y):
    return (0 <= x < M and 0 <= y < N)

DIR_DICT = {0 : 1, 1 : 0, 2 : 3, 3 : 2}
def copy_rabbit(rabbit):
    return Rabbit(rabbit.pid, rabbit.x, rabbit.y, rabbit.jump)

def race(K, S):
    global rabbits, did_run, total_sum
    DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0]
    did_run = [False for _ in range(P+1)]
    rabbit_pq = []
    for i in range(1,P+1):
        x, y = point[i]
        heapq.heappush(rabbit_pq, Rabbit(pid_arr[i], x, y, jump_cnt[i]))
        
    for k in range(K):
        # (1) 우선순위가 제일 높은 토끼 뽑기 #
        # rabbits.sort(key = lambda x : (x.jump, x.x+x.y, x.y, x.x, x.pid))
        # highest = rabbits[0]
        cur_rabbit = heapq.heappop(rabbit_pq)
        dis = dist_arr[PID_MAP[cur_rabbit.pid]]
        nex_rabbit = Rabbit(cur_rabbit.pid, 0, 0, cur_rabbit.jump)
        
                # 토끼를 위로 이동시킵니다.
        up_rabbit = get_up_rabbit(copy_rabbit(cur_rabbit), dis)
        # 지금까지의 도착지들보다 더 멀리 갈 수 있다면 도착지를 갱신합니다.
        if compare(nex_rabbit, up_rabbit): 
            nex_rabbit = up_rabbit


        # 토끼를 아래로 이동시킵니다.
        down_rabbit = get_down_rabbit(copy_rabbit(cur_rabbit), dis)
        # 지금까지의 도착지들보다 더 멀리 갈 수 있다면 도착지를 갱신합니다.
        if compare(nex_rabbit, down_rabbit): 
            nex_rabbit = down_rabbit


        # 토끼를 왼쪽으로 이동시킵니다.
        left_rabbit = get_left_rabbit(copy_rabbit(cur_rabbit), dis)
        # 지금까지의 도착지들보다 더 멀리 갈 수 있다면 도착지를 갱신합니다.
        if compare(nex_rabbit, left_rabbit): 
            nex_rabbit = left_rabbit


        # 토끼를 오른쪽으로 이동시킵니다.
        right_rabbit = get_right_rabbit(copy_rabbit(cur_rabbit), dis)
        # 지금까지의 도착지들보다 더 멀리 갈 수 있다면 도착지를 갱신합니다.
        if compare(nex_rabbit, right_rabbit): 
            nex_rabbit = right_rabbit

        # 토끼의 점프 횟수를 갱신해주고, priority queue에 다시 집어넣습니다.
        nex_rabbit.jump += 1
        heapq.heappush(rabbit_pq, nex_rabbit)

        # 실제 point, jump_cnt 배열에도 값을 갱신해줍니다.
        nex_idx = PID_MAP[nex_rabbit.pid]
        point[nex_idx] = (nex_rabbit.x, nex_rabbit.y)
        jump_cnt[nex_idx] += 1

        # 토끼가 달렸는지 여부를 체크해줍니다.
        did_run[nex_idx] = True

        # 토끼가 받는 점수는 (현재 뛴 토끼)만 (r + c)만큼 점수를 빼주고,
        # 모든 토끼(total_sum)에게 (r + c)만큼 점수를 더해줍니다.
        # 최종적으로 i번 토끼가 받는 점수는 result[i] + total_sum이 됩니다.
        scores[nex_idx] -= (nex_rabbit.x + nex_rabbit.y)
        total_sum += (nex_rabbit.x + nex_rabbit.y)

        
        
    # (2) 추가 점수를 받을 토끼 찾기 #
    # rabbits.sort(key = lambda x : (-x.x-x.y, -x.y, -x.x, -x.pid))
    # for i in range(P):
    #     temp = rabbits[i]
    #     if did_run[PID_MAP[temp.pid]] == False:
    #         continue
    #     else:
    #         break
    add_score = Rabbit(0, 0,0, 0)
    while rabbit_pq:
        temp = heapq.heappop(rabbit_pq)
        if did_run[PID_MAP[temp.pid]] == False:
            continue
        if compare(add_score, temp):
            add_score = temp
    scores[PID_MAP[add_score.pid]] += S
    

###### CMD 300 : 고유 번호가 pid인 토끼의 이동거리를 L배 늘려줌 ######
def change_movedist(pid, L):
    global dist_arr
    
    idx = PID_MAP[pid]
    dist_arr[idx] *= L
                    

####### CMD 400 : 제일 점수가 높은 토끼 선택 ########
def highest_score():
    answer = 0
    for i in range(1, P+1):
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