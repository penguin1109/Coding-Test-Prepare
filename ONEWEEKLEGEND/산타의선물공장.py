## 이 문제가 요즘, 즉 2022년 하반기 들어서 점점 등장하기 시작하는 문제의 유형이다.
## 4~6개의 API 형태의 명세서를 주고 각각의 로직을 구현하도록 하는 것이다.
## 약간 진화한 SIMULATION임과 동시에 자료구조 선택이 관건이 되는 듯 하다.
## 이 문제의 경우에는 특히나 **시간 초과**에 유의 해야 한다.
## 특히나 역량 강화 교육 할 때에도 **연결 리스트**등의 자료구조를 적극적으로 사용한 경우에 시간초과 없이 풀렸었다.

""" 산타의 선물 공장
<일의 종류>
1. 공장 설립
- 공장에 M개의 벨트를 설치하고 각 벨트 위에 N/M개의 물건을 놓아 총 N개의 물건을 준비
- 주어진 순서대로 벨트에 배정해 준다.
- 각 물건마다 <고유 ID, 고유 무게>가 존재

2. 물건 하차
- 1번부터 M번까지의 벹트의 맨 앞에 있는 물건의 무게가 주어진 최대 무게인 <W_MAX>보다 작으면 하차. 더 크다면 벨트 뒤로 보냄.
- 벨트에 있는 상자가 빠지면 **한 칸씩 앞으로 내려와야함**
[출력]: 하차된 상자의 무게의 합

3. 물건 제거
- 주어진 물건의 고유 번호를 기반으로 물건을 제거한다.
- 역시나 제거된 물건 뒤의 물건들은 앞으로 한칸씩 내려온다.
[출력]: 찾는 물건이 있다면 고유 번호를, 아니면 -1

4. 물건 확인
- 물건을 찾으면 그 뒤에 있던 물건은 모두 <순서를 유지한 채로> 앞으로 이동하게 한다.
[출력]: 해당 물건이 있는 벨트의 번호, 없으면 -1

5. 벨트 고장
- 고장이 발생한 벨트의 번호가 주어지면 그 벨트는 더이상 사용할 수 없고, 그 벨트의 오른쪽 벨트부터 순서대로 보먄서 고장이 나지 않은 최초의 벨트
위에 고장난 벨트에 놓여 있던 상자들을 아래부터 순서대로 넣어준다.
- M번 벨트까지 보았음에도 정상 벨트가 없으면 1번부터 확인.
[출력]: 이미 해당 벨트가 망가져 있었다면 -1, 아니면 벨트의 번호를 그대로 반환 (=정상적으로 고장을 처리했단 뜻)

<문제>
산타가 Q번에 걸쳐서 명령을 순차적으로 진행하며 원하는 결과를 출력하도록 하여라.
"""

belts = []
BROKEN = [[-1, -1]]
## INSTRUCTION ID: 100 ##
def make_factory(info):
    global belts
    # 초기 공장 설립하는 단계
    N, M = info[1], info[2]
    ID = info[3:3 + N]
    W = info[3 + N:len(info) + 1]

    belts = [[] for _ in range(M)]
    idx = 0
    for m in range(M):
        for i in range(N // M):
            belts[m].append([ID[idx], W[idx]])
            idx+=1
    return belts


## INSTRUCTION ID: 200 ##
def lower_product(w_max):
    global belts
    add = 0
    # print(belts)
    for idx in range(M):
        belt = belts[idx]
        if belt == BROKEN or belt == [[]] or belt == []:
            continue
        # 처음에 있는 물건만 확인하면 된다.
        first = belt[0]  # (ID, WEIGHT)
        if first[1] > w_max:  # 맨 뒤로 보낸다.
            new_belt = belt[1:] + [belt[0]] # 새로운 belt는
        else:  # 하차 시킴
            add += first[1]
            new_belt = belt[1:]
        belts[idx] = new_belt
    return add, belts


## INSTRUCTION ID: 300 ##
def remove_product(r_id):
    global belts
    # print(belts)
    exist = False
    for idx in range(M):
        belt = belts[idx]
        if belt == BROKEN or belt == [[]]:
            continue
        new_belt = []
        for i, prod in enumerate(belt):
            if prod[0] == r_id:
                exist = True
                # 물건을 제거하고 뒤에 있는 상자들은 한 칸씩 앞으로 내려온다.
            else:
                new_belt.append(prod)
        if new_belt == []:
            belts[idx] = [[]]
        else:
            belts[idx] = new_belt
    if exist:
        return r_id, belts
    else:
        return -1, belts


## INSTRUCTION ID: 400 ##
def check_product(f_id):
    global belts

    exist_belt_n = -1
    # exist_n = -1
    for idx in range(M):
        exist_n = -1
        belt = belts[idx]
        if belt == BROKEN or belt == [[]]: # 비어 있는 belt라면
            continue
        to_front = []
        to_back = []
        for i, prod in enumerate(belt):
            # f_id에 해당하는 상자를 찾은 이후에는 계속 그 상자를 벨트의 앞에 위치 시켜야 한다.
            if prod[0] == f_id or exist_n != -1:
                exist_belt_n = idx
                exist_n = i
                to_front.append(prod)
            else:
                to_back.append(prod)

        # to_front = belt[exist_n:]
        # to_back = belt[:exist_n]
        # print(to_front, to_back)
        new_belt = to_front + to_back
        # print(new_belt)
        belts[idx] = new_belt
    if exist_belt_n == -1:
        return exist_belt_n, belts
    else:
        return exist_belt_n+1, belts


## INSTRUCTION ID: 500 ##
def broken_belt(b_num):
    global belts
    check_belt = belts[b_num]
    if check_belt == BROKEN:
        return -1, belts

    for i in range(b_num + 1, M):
        print(belts[i])
        if belts[i] != BROKEN:
            belts[i] += check_belt
            belts[b_num] = BROKEN
            return b_num + 1, belts
    for i in range(b_num):
        if belts[i] != BROKEN:
            belts[i] += check_belt
            belts[b_num] = BROKEN
            return b_num + 1, belts


Q = int(input().strip())
init_info = list(map(int, input().strip().split(' ')))
N = init_info[1]
M = init_info[2]
belts = make_factory(init_info)

for q in range(Q-1):
    # 공장 설립 -> 첫 명령은 무조건 이래야 함.
    # print(belts)

    instruct_id, instruct_info = map(int, input().strip().split(' '))  # 명령 아이디에 따라서 다름

    if (instruct_id == 200):  # 물건 하차
        lowered_weight_sum, belts = lower_product(instruct_info)
        print(lowered_weight_sum)
    elif (instruct_id == 300):  # 물건 제거
        remove_ret, belts = remove_product(instruct_info)
        print(remove_ret)
    elif (instruct_id == 400):  # 물건 확인
        exist_belt_n, belts = check_product(instruct_info)
        print(exist_belt_n)
    elif (instruct_id == 500):  # 벨트 고장
        belt_broken, belts = broken_belt(instruct_info - 1)
        print(belt_broken)




