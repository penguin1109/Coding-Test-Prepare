""" 문제 설명
- N명의 인원이 참여하고, 대회를 3개 개최하였으며, 모든 구성원이 각 대회에 참여를 하게 된다.
- 참가자는 각 대회에서 0이상 1000이하의 정수인 점수를 얻는다. (한 대회에서 둘 이상의 참가자가 동점이 나오는 경우도 있을 수 있다.)

<출력> 각 참가자의 대회별 등수 및 최종 등수를 출려하여라
"""
import sys
import heapq
from collections import defaultdict


N = int(sys.stdin.readline()) ## 참가자의 수

final_result = [0 for _ in range(3)]

def get_order(result):
    q = defaultdict(list)
    sorted_result = [(r, i) for i, r in enumerate(result)]
    sorted_result = sorted(sorted_result, reverse=True)
    order = [0 for _ in range(len(result))]
    prev = sorted_result[0][0]

    prev_ptr = 0
    for i in range(1, len(result)):
        if sorted_result[i][0] == prev:
            continue
        else:
            for ptr in range(prev_ptr, i):
                order[sorted_result[ptr][1]] = prev_ptr + 1

            prev_ptr = i
            prev = sorted_result[i][0]
    for j in range(prev_ptr, len(result)):
        order[sorted_result[j][1]] = prev_ptr + 1
    return order




for i in range(3):
    result = list(map(int, sys.stdin.readline().strip().split(' '))) ## 각 대회별 결과
    order = get_order(result)
    print(' '.join([str(o) for o in order]))
    final_result = [a+b for a,b in zip(final_result, result)]
order = get_order(final_result)
print(' '.join([str(o) for o in order]))