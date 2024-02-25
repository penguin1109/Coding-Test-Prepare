""" BOJ 11000. 강의실 배정
- S_i에서 시작해서 T_i에 끝나는 N개의 수업이 주어질 때, 최소의 강의실을 사용해서 모든 수업 가능하게
- 무조건 수업이 끝난 직후에 다음 수업을 시작할 수 있다.
- 강의실의 개수를 출력하여라.
"""
import sys
import heapq

input = sys.stdin.readline

N = int(input().strip())
class_time = []
# for _ in range(N):
#     heapq.heappush(class_time, list(map(int, input().strip().split(' '))))
class_time = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 시작 시간, 종료 시간 #

## (1) (시작 시간, 종료 시간)을 각각 순서대로 우선순위를 두고 정렬 ## 
## (2) 정렬한 다음에는 priority queue에다가 종료 시점을 입력으로 넣어준다. ##
# (2)-1. Top에 있는 종료시점보다 다음 시작 시간이 더 나중이면 Top에 있는 종료시점 pop, 그리고 새로운 종료 시점 append ##

sorted_class_time = sorted(class_time, key = lambda x : (x[0], x[1]))


q = []
for i, (st, et) in enumerate(sorted_class_time):
# while class_time:
#     st, et = heapq.heappop(class_time)
    if len(q) == 0:
        heapq.heappush(q, et)
    else:
        earliest_end_time = q[0]
        if earliest_end_time <= st:
            heapq.heappop(q)
            heapq.heappush(q, et)
        else:
            heapq.heappush(q, et)

print(len(q))