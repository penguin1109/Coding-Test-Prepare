import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
from collections import deque
import heapq

input = sys.stdin.readline
T = int(input().strip())

reserve_queue = [] # 접수 창구 대기열 #
fix_queue = [] # 정비 창구 대기열 #
client_status = {} # 각각의 고객이 사용한 정비 창구 확인 #
reserve_status = []
fix_status = []
ended = 0
def init():
    global reserve_status, reserve_queue, fix_queue, client_status, fix_status, ended
    reserve_queue = []
    fix_queue = []
    client_status = {}
    reserve_status = [[-1, -1] for _ in range(N)]
    fix_status = [[-1, -1] for _ in range(M)]
    ended = 0
def one_step(time):
    global ended, reserve_status, reserve_queue, fix_status, fix_queue
    if time < len(visit_time):
        visiters = visit_time[time]
        for visiter in visiters: # 동시에 사람들이 도착할 수가 있다. #
            heapq.heappush(reserve_queue, [visiter])
    # print(f"{time} {reserve_queue}")
    #### 정비 접수 시작 ####
    for i in range(len(reserve_status)):
        temp = reserve_status[i]
        if temp == [-1, -1]:
            if reserve_queue:
                v = heapq.heappop(reserve_queue)[0]
                # print(f"V: {v}")
                reserve_status[i] = [v, reserve_time[i]-1] # 정비 중이던 사람이 없으면 우선순위에 맞춰서 채워 넣어 준다. #
                client_status[v] = [i, -1] # 고객 정보에서 사용한 정비 찬구 번호 저장 #
        elif temp[-1] == 0: # 접수 처리가 끝난 경우에 #
            heapq.heappush(fix_queue, [time, i, reserve_status[i][0]])  # 정비 대기열에 넣어준다. (대기 시작 시간, 사용한 접수 창구 번호, 사람 번호)
            if reserve_queue:
                v = heapq.heappop(reserve_queue)[0]
                reserve_status[i] = [v, reserve_time[i]-1]
                client_status[v] = [i, -1]
            else:
                reserve_status[i] = [-1, -1]
        else:
            reserve_status[i][1] -= 1 # 정비 중엔 사람의 남은 시간 업데이트 #
    # print(f"CLIENT STATUS : {client_status}")
    # print(f"RESERVE STATUS : {reserve_status}")
    #### 정비 시작 ####
    for i in range(len(fix_status)):
        temp = fix_status[i]
        if temp == [-1,-1]:
            if fix_queue:
                v = heapq.heappop(fix_queue) # (대기 시작 시간, 사용한 접수 창구 번호
                fix_status[i] = [v[-1], fix_time[i]-1] # (사람 번호, 남은 처리 시간) #
                ended += 1 # 정비 시작했으면 ended로 처리해도 무방 #
                client_status[v[-1]][-1] = i
        elif temp[-1] == 0:
            if fix_queue:
                v = heapq.heappop(fix_queue)
                fix_status[i] = [v[-1], fix_time[i]-1]
                ended += 1
                client_status[v[-1]][-1] = i
            else:
                fix_status[i] = [-1, -1]
        else:
            fix_status[i][-1] -= 1 # 남은 정비 시간 업데이트 #
    # print(f"CLIENT STATUS : {client_status}")
    # print(f"RESERVE STATUS : {reserve_status}")
def find_same():
    answer = 0
    for key, value in client_status.items():
        if value[0] == A and value[1] == B:
            answer += key+1
    if answer != 0:
        return answer
    else:
        return -1


for test_case in range(1, T+1):
    N, M, K, A, B = map(int, input().strip().split(' ')) # 접수 창구의 개수, 정비 창구의 개수, 고객 수, 지갑 분실 접수번호, 지갑 분실 정비번호 #
    A, B = A-1, B-1
    reserve_time = list(map(int, input().strip().split(' '))) # 고장 접수 처리 시간 #
    fix_time = list(map(int, input().strip().split(' '))) # 고장 정비 처리 시간 #
    arr = list(map(int, input().strip().split(' '))) # K명의 고객이 각각 정비소에 방문하는 시간 #
    # print(f"ARR : {arr}")
    visit_time = [[] for _ in range(max(arr)+1)]
    for idx, t in enumerate(arr):
        visit_time[t].append(idx) # 각각의 시간대별로 고객 입장 시간 관리
    # print(visit_time)

    init()
    time = 0
    while True:
        one_step(time)
        time += 1
        if ended == K:
            break
    answer = find_same()

    print(f"#{test_case} {answer}")
    # if test_case == 10:
    #     break
    # break # 우선 한 케이스만 디버깅을 위해서 실행해 보자 #



