import sys
import heapq

"""
- 강의실 1개에 최대한 많은 강의 배정이 목표
- 겹침 X (단, 시작시간과 종료시간은 겹쳐도 됨)
[문제 풀이]
결과적으로 끝나는 시간이 빠르다는 건 강의를 배정할 수 있는 시간이 많이 남는다는 뜻이기 때문에
종료 시간이 빠르면서 동시에 배정이 가능한 강의를 순차적으로 배정하면 된다.
"""
# sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline
N = int(readl().strip()) # 강의의 개수 #
q = []

dp = [0 for _ in range(N)]

for i in range(N):
    s, f = map(int, readl().strip().split(' ')) # 강의 시작 시간, 종료 시간 #
    # heapq.heappush(q, [f, s])
    q.append([f, s])
q.sort(key = lambda x: x[0]) # 종료 시간에 대해서 오름차순으로 정렬 #
# print(q)
start_time, end_time = -1, -1
answer = 0

for _ in range(N):
    temp_end, temp_start = q[_]
    # print(temp_start, temp_end)
    if start_time == -1:
        start_time, end_time = temp_start, temp_end
        answer += 1
    else:
        if end_time <= temp_start:
            start_time, end_time = temp_start, temp_end
            answer += 1

print(answer)

