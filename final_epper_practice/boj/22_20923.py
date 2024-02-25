""" BOJ 20923 - 숫자 할리갈리 게임
- 도도 : do, 수연 : su, 비김 : dosu
(1) 각각 N장의 카드로 이뤄진 deque를 배분 받음. 처음에 그라운드는 비어 있음.
(2) do 부터 가장 위에 있는 카드를 내려놓음.
(3) 가장 위에 있는 카드의 합이 5 -> 수연 5가 있으면 -> 도도 
(4) 카드개수가 0이면 짐, M번 진행 한다음에는 카드 개수로 비교

"""
import sys
from collections import deque

input = sys.stdin.readline
BOTH="dosu"
DO="do"
SU="su"
N, M = map(int, input().strip().split(' ')) # 카드의 개수, 게임 진행 횟수 #
# do_card = deque([])
# su_card = deque([])

cards = [deque(), deque()]
temp = [deque(), deque()]
for n in range(N): # 아래부터 위까지 #
    a, b = map(int, input().strip().split(' ')) # 도도의 카드에 적힌 수, 수연의 카드에 적힌 수 #
    cards[0].append(a) 
    cards[1].append(b)

# do_ground = deque([])
# su_ground = deque([])
# do_ground = []
# su_ground = []


def ring(my_cards, my_ground, your_ground):
    # print('before ', my_cards)
    my_cards = deque(your_ground[::-1]) + my_cards
    my_cards = deque(my_ground[::-1]) + my_cards
    # print('after ', my_cards)
    my_ground, your_ground = [], []
    return my_cards, my_ground, your_ground

for m in range(M):
    # temp[m%2].appendleft(cards[m%2].popleft())
    temp[m%2].append(cards[m%2].pop())
    
    if not cards[m%2]: 
        break
    if temp[0] and temp[0][-1] == 5 or temp[1] and temp[1][-1] == 5:
        # dodo가 종 치는 경우 #
        '''while 문 : python3으로 pass'''
        # while temp[1]: # temp 배열에는 최근에 쌓은 카드가 처음에 위치하기 때문에 뒤집에서 밑에 쌓는다면 pop으로 뽑아서 넣기 #
        #     cards[0].append(temp[1].popleft())
        # while temp[0]:
        #     cards[0].append(temp[0].popleft())
        '''extend left 문 : pypy3으로만 pass'''
        cards[0].extendleft(temp[1])
        cards[0].extendleft(temp[0])
        '''deque <-> list 문 : 둘다 TLE'''
        # cards[0] = deque(list(temp[1]) + list(cards[0]))
        # cards[0] = deque(list(temp[0]) + list(cards[0]))
        temp[0].clear();temp[1].clear()
    if temp[0] and temp[1] and temp[0][-1] + temp[1][-1] == 5:
        # su가 종 치는 경우 #
        while temp[0]:
            cards[1].append(temp[0].pop())
        # cards[1].extendleft(temp[0])
        # cards[1] = deque(list(temp[0]) + list(cards[1]))
        while temp[1]:
            cards[1].append(temp[1].pop())
        # cards[1].extendleft(temp[1])
        # cards[1] = deque(list(temp[1]) + list(cards[1]))
        # temp = [deque(), deque()]
        temp[0].clear();temp[1].clear()
# for m in range(M):
#     if len(do_card) == 0 and len(su_card) == 0:
#         print(BOTH);exit(0)
#     elif len(do_card) == 0:
#         print(SU);exit(0)
#     elif len(su_card) == 0:
#         print(DO);exit(0)
        
#     if m % 2 == 0:
#         card = do_card.pop()
#         do_ground.append(card)
#     else:
#         card = su_card.pop()
#         su_ground.append(card)
#     if len(do_ground) > 0 and len(su_ground) > 0:
#         if do_ground[-1] == 5 or su_ground[-1] == 5:
#             do_card, do_ground, su_ground = ring(do_card, do_ground, su_ground)
#             # print(f"{m} 도도 종 침 : 수연 카드 -> {len(su_card)} 도도 카드 -> {len(do_card)} {len(do_ground)} {len(su_ground)}")
#         elif do_ground[-1] + su_ground[-1] == 5:
#             su_card, su_ground, do_ground = ring(su_card, su_ground, do_ground)
#             # print(f"{m} 수연 종 침 : 수연 카드 -> {len(su_card)} 도도 카드 -> {len(do_card)} {len(do_ground)} {len(su_ground)}")
#     # print(do_card, su_card)

if len(cards[1]) > len(cards[0]):
    print(SU)
elif len(cards[1]) < len(cards[0]):
    print(DO)
else:
    print(BOTH)