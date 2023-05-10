""" 산타의 선물 공장 2
<API 명세서>
1. 공장 설립
- N개의 벨트, M개의 물건을 각각의 위치에 맞게 벨트에 배치한다.
- 한 벨트에서 각각의 물건의 번호는 오름차순이어야 한다.

[출력]: 없음

2. 물건 모두 옮기기
- m_src번째 벨트에 있는 물건을 **모두** m_dst번째 벨트에 이동한다.
- 옮긴 뒤 m_dst번째 벨트에 있는 선물의 개수를 출력하면 된다. [ 여기서 for문을 써서 다 탐색하거나 각 벨트 번호별 개수를 저장해도 된다. ]

[출력]: destination 벨트에 물건의 개수

3. 앞 물건만 교체하기
- m_src의 가장 앞의 물건을 m_dst 벨트의 선물 중 제일 앞에 있는 선물과 교체한다.
- 둘 중 하나의 벨트에 선물이 아예 없다면 교체하지 않고 m_dst 벨트로 선물을 옮기기만 하면 된다.

[출력]: destination 벨트의 물건의 개수

4. 물건 나누기
- m_src에 있는 물건의 개수가 n개일때 앞에서 floor(n/2)번째까지의 물건을 m_dst **앞으로** 옮긴다.
- m_src에 물건이 1개 있으면 물건을 옮기지 않는다.

[출력]: m_dst 벨트의 물건의 개수

5. 물건 정보 얻기
- 물건 번호 p_num을 입력으로 받을때 선물의 앞번호 a, 뒤번호 b가 있으면 (a + 2 * b) 출력
- 앞선물이 없으면 a= -1, 뒤선물이 없으면 b= -1

[출력]: a + (2 * b)

6. 벨트 정보 얻기
- 벨트 번호 b_num이 주어질 때 벨트의 맨 앞에 있는 선물의 번호 a, 맨뒤의 선물의 번호 b, 벹트의 선물의 개수 c
- 선물이 없으면 a=b=-1, c=0

[출력]: a + (2*b) + (3*c)

<풀이중 깨닳은 점>
<<<<<<< HEAD
- 생각해 보니 전혀 필요 없던 belt_id 정보를 저장하는 배열떄문에 while 문이 들어가서 시간 초과가 났었다.
=======
- 생각해 보니 전혀 필요 없던 belt_id 정보를 저장하는 배열떄문에 while 문이 들어가서 시간초과가 났었다.
>>>>>>> origin/master
- 결론적으로 CASE 400 번만 변경을 하니까 문제가 해결이 되었다.
    => 이제 CASE 400을 구현함에 있어서 문제가 뭐였는지 파악하기 위해서 디버깅을 해 보자.
"""
import math
from collections import defaultdict
N, M = -1, -1
MAX_M = MAX_N = 100000
product_count = [0] * MAX_M # 벨트 별로 물건의 개수
head = [0] * MAX_M # 벨트 별로 제일 앞에 있는 물건의 ID
tail = [0] * MAX_M # 벨트 별로 제일 뒤에 있는 물건의 ID

prv = defaultdict(lambda : 0) # 각 물건 별로 이후에 있는 물건의 ID
nxt = defaultdict(lambda : 0) # 각 물건 별로 이전에 있는 물건의 ID
# belt_id = defaultdict(lambda : -1) # 각 물건 별로 물건이 위치한 벨트의 번호


### CASE 100 ###
def build_factory(instruction):
    N, M = instruction[1], instruction[2]
    for i in range(3, len(instruction)):
        b_num = instruction[i]-1 # 벨트의 ID (0부터 시작하도록 한다)
        p_num = i - 2 # 물건의 ID (1부터 시작하도록 한다)

        product_count[b_num] += 1 # 벨트 ID에 물건 개수 갱신

        # belt_id[p_num] = b_num

        prv[p_num] = tail[b_num]

        if head[b_num] == 0: # 아직 원소가 없었던 경우에
            head[b_num] = p_num
            tail[b_num] = p_num
        else: # 이미 원소가 있는 경우라면 p_num을 업데이트 한다.
            nxt[tail[b_num]] = p_num
            tail[b_num] = p_num

### CASE 200 ###
def move_all_product(m_src, m_dst):
    answer = product_count[m_src] + product_count[m_dst]
    if product_count[m_src] == 0:
        print(product_count[m_dst])
        return
    product_count[m_src] = 0
    product_count[m_dst] = answer

    src_head = head[m_src]
    src_tail = tail[m_src]
    dst_head = head[m_dst]
    dst_tail = tail[m_dst]

    # 옮겨지는 물건의 belt id도 바꿔 주어야 한다.
    # start = src_head
    # while (start  != src_tail):
    #     belt_id[start] = m_dst
    #     start = nxt[start]
    # print(f"START: {start} ORIGINAL SRC TAIL: {src_tail}")
    # belt_id[start] = m_dst
    # src에 있는 모든 물건을 dst로 옮겨주기 위해서 head와 tail변경
    if dst_head == 0: # dst에 물건이 없었다면
        head[m_dst] = src_head
        tail[m_dst] = src_tail
        head[m_src] = 0
        tail[m_src] = 0
    else:
        # 앞으로 이동해 준다.
        head[m_dst] = src_head
        head[m_src] = 0
        tail[m_src] = 0
        # dst의 tail과 src의 head를 연결해 준다.
        nxt[src_tail] = dst_head
        prv[dst_head] = src_tail

    print(answer)

### CASE 300 ###
def change_first_product(m_src, m_dst):
    if product_count[m_src] == 0 and product_count[m_dst] == 0:
        print(product_count[m_dst])
        return
    elif product_count[m_src] == 0:
        # src에 물건이 없으니 src로 물건을 하나 옮긴다.
        dst_head = head[m_dst]
        tail[m_src] = dst_head
        # belt_id[dst_head] = m_src
        head[m_dst] = nxt[dst_head]
        head[m_src] = dst_head
        prv[head[m_dst]] = 0
        nxt[head[m_src]] = 0

        product_count[m_dst] -= 1
        product_count[m_src] += 1
        if product_count[m_dst] == 0:
            tail[m_dst] = 0
            head[m_dst] = 0
        print(product_count[m_dst])
        return
    elif product_count[m_dst] == 0:
        src_head = head[m_src]
        tail[m_dst] = src_head
        # belt_id[src_head] = m_dst
        head[m_src] = nxt[src_head]
        head[m_dst] = src_head
        prv[head[m_src]] = 0
        nxt[head[m_dst]] = 0

        product_count[m_dst] += 1
        product_count[m_src] -= 1
        if product_count[m_src] == 0:
            tail[m_src] = 0
            head[m_src] = 0
        print(product_count[m_dst])
        return
    else: # 둘다 물건이 있어서 교체 할 수 있는 경우
        src_head = head[m_src]
        dst_head = head[m_dst]

        head[m_dst] = src_head
        head[m_src] = dst_head

        # belt_id[src_head] = m_dst; belt_id[dst_head] = m_src

        src_temp = nxt[src_head]
        dst_temp = nxt[dst_head]

        nxt[src_head] = dst_temp
        nxt[dst_head] = src_temp

        prv[src_temp] = dst_head
        prv[dst_temp] = src_head

        if product_count[m_dst] == 1:
            tail[m_dst] = src_head
        if product_count[m_src] == 1:
            tail[m_src] = dst_head
        print(product_count[m_dst])
        return


### CASE 400 ###
def push_head(b_num, hid):
    if hid == 0:
        return
    if product_count[b_num] == 0:
        head[b_num] = tail[b_num] = hid
        product_count[b_num] = 1
    else:
        orig_head = head[b_num]
        nxt[hid]= orig_head
        prv[orig_head] = hid
        head[b_num] = hid
        product_count[b_num] += 1

def remove_head(b_num):
    if product_count[b_num] == 0:
        return 0
    if product_count[b_num] == 1:
        p_id = head[b_num]
        head[b_num] = tail[b_num] = 0
        product_count[b_num] = 0
        return p_id
    h_id  = head[b_num]
    next_head = nxt[h_id]
    nxt[h_id] = prv[next_head] = 0
    product_count[b_num] -= 1
    head[b_num] = next_head

    return h_id

def divide_product(m_src, m_dst):
    n = product_count[m_src]
    move_n = int(math.floor(n / 2))
    box_ids = []
    for _ in range(move_n):
        box_ids.append(remove_head(m_src))
    for i in range(len(box_ids)-1, -1, -1):
        push_head(m_dst, box_ids[i])
    print(product_count[m_dst])

def divide_product_debug(m_src, m_dst):
    n = product_count[m_src]
    move_n = int(math.floor(n // 2))
    answer = product_count[m_dst] + move_n
    if move_n == 0:
        print(answer)
        return

    src_head = head[m_src]
    src_tail = tail[m_src] # 불변
    dst_head = head[m_dst] # 불변
    dst_tail = tail[m_dst]




    move_ids = []
    for i in range(move_n):
        # belt_id[p_num] = m_dst # 이동하는 물건의 벨트 번로 업데이트
<<<<<<< HEAD
        hid = head[m_src] # source 벨트의 처음에 있는 물건의 ID
=======
        hid = head[m_src]
>>>>>>> origin/master
        next_head = nxt[hid]
        nxt[hid] = prv[next_head] = 0
        head[m_src] = next_head

        move_ids.append(hid)

    # product_count[m_src] -= move_n
    # product_count[m_dst] += move_n

    #
    for i in range(len(move_ids)-1,-1, -1):
        if product_count[m_dst] == 0:
            head[m_dst] = tail[m_dst] = move_ids[i]
        else:
            orig_head = head[m_dst]
            nxt[move_ids[i]] = orig_head
            prv[orig_head] = move_ids[i]
            head[m_dst] = move_ids[i]



        product_count[m_dst] += 1
        product_count[m_src] -= 1



     # src 벨트의 반절 뒷부분의 첫번째가 src 벨트의 head가 된다.


    print(answer)


### CASE 500 ###
def get_product_info(p_num):
    a = prv[p_num]
    b = nxt[p_num]
    if a == 0:
        a = -1
    if b == 0:
        b = -1
    answer = a + (2*b)
    print(answer)
### CASE 600 ###
def get_belt_info(b_num):
    a = head[b_num]
    b = tail[b_num]
    c = product_count[b_num]
    if c == 0:
        a = b = -1
    answer = a + (b*2) + (c*3)
    print(answer)


Q = int(input().strip())

for q in range(Q):
    instruction = list(map(int, input().strip().split(' ')))

    query = instruction[0]

    if query == 100:
        N, M = instruction[1], instruction[2]
        build_factory(instruction)
    elif query == 200:
        move_all_product(instruction[1]-1, instruction[2]-1)
    elif query == 300:
        change_first_product(instruction[1]-1, instruction[2]-1)
    elif query == 400:
        divide_product_debug(instruction[1]-1, instruction[2]-1)
    elif query == 500:
        get_product_info(instruction[1])
    elif query == 600:
        get_belt_info(instruction[1]-1)

    # print(f"EPOCH: {q}")
    # print(head[:N], tail[:N])
    # print(product_count[:N])
    # print(prv)
    # print(nxt)