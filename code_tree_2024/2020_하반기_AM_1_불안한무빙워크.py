import sys
from collections import deque
input = sys.stdin.readline

N, K = map(int, input().strip().split(' ')) # 무빙워크 길이, 실험 종료의 기준인 안정성이 0인 판의 개수 #
safety = list(map(int, input().strip().split(' '))) # 무빙워크 각각의 칸의 안정성 #

people = deque([])
track = [False for _ in range(N)]
iter = 0
        
while True:
    # (1) 무빙 워크를 한 칸 움직임 #
    safety = [safety[-1]] + safety[:-1]
    people = deque([a + 1 for a in people])
    # print(f"PEOPLE : {people}  SAFETY : {safety}")
    track = [False] + track[:-1]
    # (2) 무빙워크에 있는 사람 한칸씩 이동 #
    new_people = deque([])
    new_track = [False for _ in range(N)]
    while people:
        ppl = people.popleft() # 가장 먼저 올라간 순서대로 #
        if ppl == N-1:
            continue
        next_idx = ppl + 1
        if safety[next_idx] == 0:
            new_people.append(ppl)
            new_track[ppl] = True
                
        else:
            if new_track[next_idx] == True:
                new_people.append(ppl)
                new_track[ppl] = True
            else:
                if next_idx != N-1:
                    new_people.append(next_idx)
                safety[next_idx] -= 1
                new_track[next_idx] = True
    
    # (3) 첫번쨰 칸에 사람이 없고 안정성이 0이 아니면 한 명 더 올림 #
    if new_track[0] == False and safety[0] != 0:
        new_track[0] = True
        safety[0] -= 1
        new_people.append(0)
    people = new_people
    track = new_track
    # (4) 안전성이 0인 칸이 K개 이상이면 종료 #
    if safety.count(0) >= K:
        iter += 1
        break
    iter += 1
print(iter)
    