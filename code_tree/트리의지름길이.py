N = int(input().strip()) # 트리의 노드의 개수 #
from collections import defaultdict
import heapq
import sys
sys.setrecursionlimit(10**8)
maxN = 100001
visited = [False for _ in range(maxN)]

tree = defaultdict(list)
for n in range(N-1):
    a, b, dist = map(int, input().strip().split(' ')) # 두 노드의 번호, 간선의 길이 #
    tree[a].append([b, dist])
    tree[b].append([a, dist])

# [출력] 트리의 지름의 길이 #
""" 생각나는 풀이 방법
1. BFS -> 근데 보통 BFS는 최단거리 탐색에 사용이 되긴 하는데 음수로 바꾸면 똑같으니까..
2. DP -> 이것도 비슷하긴 하겠는데 어떻게 점화식을 세우는게 맞을지 떠오르지 않음
3. DFS -> 어차피 어떤 시작 노드를 정하던 그 시작노드에서 최장 거리로 이동을 하고 그 도착 노드에서 최장 거리로 다시 이동을 하면 된다.
"""
def bfs(start):
    from collections import deque
    global max_node, max_dist
    q = deque([])
    q.append([start, 0])
    visited = [False for _ in range(maxN)]
    visited[start] = True
    while q:
        cur_node, cur_dist = q.popleft()
        if max_dist < cur_dist:
            max_dist = cur_dist
            max_node = cur_node
        for next_node, next_dist in tree[cur_node]:
            if visited[next_node] == False:
                q.append([next_node, next_dist + cur_dist])
                visited[next_node] = True
    
def dfs(cur_node, cur_dist):
    """ dfs의 방법을 사용하면 재귀 함수의 호출이 너무 많기 때문에 메모리 초과가 발생해 버린다.
    """
    global tree, maxN, visited
    global max_dist, max_node
    visited[cur_node] = True
    if max_dist < cur_dist:
        max_dist = cur_dist
        max_node = cur_node
    
    for con in tree[cur_node]:
        next_node, next_dist = con
        if visited[next_node] == False:
            visited[next_node] = True
            dfs(next_node, cur_dist + next_dist)
            visited[next_node] = False

max_dist = 0
max_node = 0


# dfs(list(tree.keys())[0], 0)
bfs(list(tree.keys())[0])
# print(f"MAX DIST : {max_dist}   MAX NODE : {max_node}")
max_dist = 0
visited = [False for _ in range(maxN)]
# dfs(max_node, 0)
bfs(max_node)
# print(f"MAX DIST : {max_dist}   MAX NODE : {max_node}")

print(max_dist)
