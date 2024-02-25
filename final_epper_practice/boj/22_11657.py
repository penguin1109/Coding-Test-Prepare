""" BOJ 11657 - 타임머신
[출력] 1번 도시에서 출발해서 나머지 도시로 가는 제일 빠른 시간 
"""
import sys
from collections import defaultdict
import heapq

input = sys.stdin.readline

N, M = map(int, input().strip().split(' ')) # 도시의 개수, 버스 노선의 개수 #
board = [{} for _ in range(N+1)]
# check = [[-1 for _ in range(N)] for _ in range(N)]
 
for m in range(M):
    a, b, c = map(int, input().strip().split(' ')) # 버스 노선의 정보 
    if b in board[a] and board[a][b] <= c: # 이미 
        pass
    else:
        board[a][b] = c
    
    # board[b].append([a, c])
# print(board)
# q = [[0,[1]]]
# q = [([1], 0)]
'''여기서 44%에서 계속 멈췄던 이유가 heapq에 tuple의 형태냐 list의 형태로 넣냐에 따라 다른게 아니라 
stack에서 list.append, list.pop을 사용했던 것처럼 비슷하게 사용할 수 있는데,
pop(0)을 하면 시간 복잡도가 O(N)이기 때문에 deque를 사용할때 list는 사용하지 않는다.

O(VE) = 최대 500 * 6000 = 3000000 -> 시간 제한 1초
V번의 반복에 대해서 해당 정점과 연결되어 있는 모든 간선(E)를 탐색한다.

다익스트라 알고리즘을 음의 가중치가 있어도 사용가능하지만,
음의 순환이 있는 경우에는 무조건 벨만 포드 알고리즘을 사용하여야 한다.
벨만 포드의 경우에는 무조건 "새로운 간선을 사용할 때 cost가 주는 경우에"만 배열 업데이트를 한다.

시간제한이 1초인 문제를 만났을 때, 일반적인 기준은 다음과 같습니다.

입력이 10,000,000 개의 경우: O(N) 알고리즘

입력이 50,000 개인 경우: O(N * log N) 알고리즘

입력이 10,000 개인 경우: O(N * N) 알고리즘

입력이 400개: O(N * N * N) 알고리즘


if 문제 2개 이상의 조건이 주어질 때 False값이 많은 condition을 앞에 오도록!
몰랐는데 if 문도 많으면 시간 복잡도에 영향을 미친다.

배열 돌릴때 for loop를 돌리는 것보다 multiplication을 하는 것이 더 빠르다.
이를테면 visited = [False for _ in range(N)] 보다 [[False] * N]이 더 빠르다는 것이다.
'''
# q = [[[1], 0]]
# q = [(0, [1])]
## STEP 1 : 
import math
answer = [math.inf for _ in range(N+1)]
answer[1] = 0
### Belman-Ford Algorithm ###
for i in range(N): # 노드의 개수 -> 노드의 개수마다 모든 간선 확인 #
    for neigh, edge_cost in board[i].items():
        if answer[neigh] > answer[i] + edge_cost:
            answer[neigh] = answer[i] + edge_cost
            if i == N-1:
                print(-1)
                exit(0)
# while q:
#     # path, dist = heapq.heappop(q)
#     dist, path = heapq.heappop(q)
#     # dist, path = heapq.heappop(q)
#     # visited[node] = True
#     node = path[-1]
#     # if answer[node] == -1:
#     #     answer[node] = dist
#     # else:
#     #     answer[node] = min(answer[node], dist)
#     if answer[node] >= dist:
#         # for neigh, cost in board[node]:
#         for neigh, cost in board[node].items():
#             if answer[neigh] > cost + dist: # 한번 cycle을 돌았는데도 시간이 짧아지는 경우 #
#                 if neigh in path: # Cycle이 존재하는 경우에 #
#                     print(-1)
#                     exit(0)
#                 else:
#                     # heapq.heappush(q,( path + [neigh], dist+cost))
#                     # heapq.heappush(q,[ path + [neigh], dist+cost])
#                     heapq.heappush(q, (cost+dist, path+[neigh]))
                    
#                     # heapq.heappush(q, [dist + cost, path + [neigh]])
#                     answer[neigh] = dist + cost
#                 # visited[neigh] = False
for ans in answer[2:]:
    if ans == math.inf:
        print(-1)
    else:
        print(ans)
