from collections import defaultdict

MAX_M = 10
head = [0] * MAX_M
tail = [0] * MAX_M

prv = defaultdict(lambda:0)
nxt = defaultdict(lambda:0)

broken = [False] * MAX_M
belt_num = defaultdict(lambda:-1) # 상자 ID마다 벨트 번호를 저장

weight = {} # 각 상자의 아이디마다 따로 무게를 저장해서 관리한다.
N, M = -1,-1
def make_factory(query):
    global N, M
    N, M = query[1], query[2]
    ID, W = query[3:3+N], query[3+N:3+N+N]
    for i in range(N):
        id = ID[i]
        weight[id] = W[i]

    size = N // M
    for i in range(M):
        head[i] = ID[i * size]
        tail[i] = ID[(i+1) * size - 1]
        for j in range(i*size, (i+1) * size):
            belt_num[ID[j]] = i
            if j < (i+1) * size-1:
                nxt[ID[j]] = ID[j + 1]
                prv[ID[j+1]] = ID[j]

## 300: 물건 제거 ##
def remove(r_id):
    if belt_num[r_id] == -1:
        print(-1)
        return
    remove_id(r_id, True)
    print(r_id)

### STEP 4 ###
def find(f_id):
    if belt_num[f_id] == -1:
        print(-1)
        return
    belt_of_id = belt_num[f_id]
    if head[belt_of_id] != f_id:
        orig_tail = tail[belt_of_id] # 현재 벨트의 마지막 원소
        orig_head = head[belt_of_id]
        new_tail = prv[f_id] # 찾고자 하는 ID의 상품 바로 앞에 있던 상자
        tail[belt_of_id] = new_tail
        nxt[new_tail] = 0

        nxt[orig_tail] = orig_head
        prv[orig_head] = orig_tail

        head[belt_of_id] = f_id # 찾고자 하는 ID의 상품을 새로 위치가 바뀐 벨트의 HEAD로 바꾼다.

    print(belt_of_id + 1)
### STEP 5 ###
def broken_belt(b_num):
    if broken[b_num]:
        print(-1)
        return
    broken[b_num] = True
    if head[b_num] == 0: # 비어있는 벨트면 별도의 상자 옮김이 필요 없다.
        print(b_num + 1)
        return
    nxt_num = b_num
    while True:
        nxt_num = (nxt_num + 1) % M
        if broken[nxt_num] == False:
            if tail[nxt_num] == 0:
                head[nxt_num] = head[b_num]
                tail[nxt_num] = tail[b_num]
            else:
                a, b = tail[nxt_num], head[b_num]
                prv[b] = a
                nxt[a] = b

                # 뒤에 이어 붙이려고 했던 것이 전체 벨트의 tail이었다면 벨트의 tail정보도 변경
                if tail[belt_num[a]] == a:
                    tail[belt_num[a]] = b
                tail[nxt_num] = tail[b_num]
            _id = head[b_num]
            while _id != 0:
                belt_num[_id] = nxt_num # 추가된 애들 업데이트를 위해서 각 상자별 벨트 번호를 갱신
                _id = nxt[_id]
            head[b_num] = tail[b_num]
            break
    print(b_num+1)


def remove_id(r_id, remove_belt):
    belt_of_id = belt_num[r_id]
    if remove_belt:
        belt_num[r_id] = -1

    if head[belt_of_id] == tail[belt_of_id]: # 원소가 하나밖에 없었다면
        head[belt_of_id] = tail[belt_of_id] = 0

    elif r_id == head[belt_of_id]:
        nid = nxt[r_id]
        head[belt_of_id] = nid
        prv[nid] =0
    elif r_id == tail[belt_of_id]:
        pid = prv[r_id]
        tail[belt_of_id] = pid
        nxt[pid] = 0
    else:
        pid, nid = prv[r_id], nxt[r_id]
        nxt[pid] = nid
        prv[nid] = pid
    nxt[r_id] = prv[r_id] = 0

def drop_off(w_max):
    global N, M
    add = 0
    for i in range(M):
        if broken[i] == True:
            continue
        if head[i] != 0:
            _id = head[i]
            w = weight[_id]
            if w <= w_max:
                add += w
                remove_id(_id, True)
            elif nxt[_id] != 0:
                remove_id(_id, False)
                tid = tail[i]
                nxt[tid] = _id
                prv[_id] = tid
                if tail[belt_num[tid]] == tid:
                    tail[belt_num[tid]] = _id
    print(add)

Q = int(input())
for _ in range(Q):
    instruction = list(map(int, input().strip().split(' ')))
    query = instruction[0]
    if query == 100:
        make_factory(instruction)
    elif query == 200:
        drop_off(instruction[1])
    elif query == 300:
        remove(instruction[1])
    elif query == 400:
        find(instruction[1])
    elif query == 500:
        broken_belt(instruction[1]-1)


