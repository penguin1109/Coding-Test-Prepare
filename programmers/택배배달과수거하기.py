""" 택배 배달과 수거하기
- 어쨌든 돌아오는 트럭은 상자를 싣고 있으면 안된다.
- 가장 긴 집에 가야 하기 때문에 뒤에서부터, 즉 제일 멀리 있는 집에서부터 출발해야 한다.
- pickups, delivers에서 최적의 위치를 찾기 위해서 배송 짐칸, 회수 짐칸을 따로 만들어
비운 상태에서 처음 짐을 싣을 경우의 위치를 두 배열에서 각각 찾아 각각의 큐에 넣고 계속 택배 차량에 넣으면서 차면 비우고 시작까지 오게 한다.
- 큐에서 같이 꺼낼 때 그 위치중에 큰 거리를 왕복 거리로 한다.
"""
from collections import deque
def solution(cap, n, deliveries, pickups):
    answer = 0

    deliveries_end = deque(); pickups_end = deque();
    d_idx = len(deliveries)-1
    p_idx = len(pickups)-1
    load = [0, 0]

    while (d_idx >= 0):
        diff = cap-(load[0] + deliveries[d_idx])  # 현재 배달하려고 싣은 개수와 배달 받아야 하는 양에서 최대 싣는게 가능한 개수 빼기
        if (load[0] == 0 and deliveries[d_idx] > 0):
            deliveries_end.append(d_idx)
        if (diff >= 0): # 현재 index를 배달 가능
            load[0] += deliveries[d_idx]
            deliveries[d_idx] = 0
        elif (diff < 0): # 전부 배달은 불가능
            deliveries[d_idx] -= (cap - load[0]) # 배달 가능한 양만 빼주기
            load[0] = 0
            continue
        d_idx -= 1

    while (p_idx >= 0):
        diff = cap - (load[1] + pickups[p_idx])
        if (load[1] == 0 and pickups[p_idx] > 0):
            pickups_end.append(p_idx)
        if (diff >= 0):
            load[1] += pickups[p_idx]
            pickups[p_idx] = 0
        elif (diff < 0):
            pickups[p_idx] -= (cap - load[1])
            load[1] = 0
            continue
        p_idx -= 1 ## 배달 창고에서 가까운 곳으로 이동

    if (len(deliveries_end) > 0 and len(pickups_end) > 0):
        min_len = len(deliveries_end) if len(deliveries_end) < len(pickups_end) else len(pickups_end)
        for _ in range(min_len):
            d_last = deliveries_end.popleft()
            p_last = pickups_end.popleft()
            answer += 2 * (p_last + 1 if p_last > d_last else d_last + 1) ## 큐에서 같이 꺼낼 때는 거리가 더 먼 집과의 거리를 왕복 거리로 간주한다.
        while len(deliveries_end) > 0:
            answer += 2 * (deliveries_end.popleft() + 1)
        while len(pickups_end) > 0:
            answer += 2 * (pickups_end.popleft() + 1)
    return answer


if __name__ == "__main__":
    caps = [4, 2]
    N = [5, 7]
    deliv = [
        [1, 0, 3, 1, 2], [1, 0, 2, 0, 1, 0, 2]
    ]
    pickup = [
        [0,3,0,4,0],[0,2,0,1,0,2,0]
    ]
    # results = [16, 30]

    for cap, n, deliveries, pickups in zip(caps, N, deliv, pickup):
        print(solution(cap, n, deliveries, pickups))