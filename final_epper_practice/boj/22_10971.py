import sys
from collections import defaultdict
input = sys.stdin.readline

""" BOJ 10971 [문제 설명]
- 가장 적은 비용을 들이면서 N개의 모든 도시를 거쳐서 다시 원래 도시로 돌아오는 순회 여행
- 양방향 그래프인데, 양방향의 그래프의 가중치가 서로 다르다.
[출력] 순회에 필요한 최소 비용
"""

N = int(input().strip()) # 도시의 수 #
# cost_graph = [list(map(int, input().strip().split(' '))) for _ in range(N)]
cost_board = []
cost_graph = defaultdict(list)
for n in range(N):
    arr = list(map(int, input().strip().split(' ')))
    cost_board.append(arr)
    for ai, a in enumerate(arr):
        if a != 0:
            cost_graph[n].append([ai, a])
    

answer = -1

def back_track(start_node, visited, cur_node, dist):
    global answer
    if dist >= answer and answer != -1:
        return
    if sum(visited) == N:
        cost = cost_board[cur_node][start_node]
        if cost != 0:
            if answer == -1:
                answer = dist + cost
            else:
                answer = min(answer, dist + cost)
        return
    for (n, cost) in cost_graph[cur_node]:
        # if visited[n] == 0 and cost_graph[cur_node][n] != 0:
        if visited[n] == 0 and cost != 0:
            visited[n] = 1
            back_track(start_node, visited, n, dist + cost)
            visited[n] = 0

for n in range(N):
    visited = [0 for _ in range(N)]
    visited[n] = 1
    back_track(n, visited, n, 0)

print(answer)
    

            
            