import sys
from collections import defaultdict, deque
sys.setrecursionlimit(10**7)
'''출력
- S->T와 T->S까지의 경로에 모두 포함될 수 있는 정점의 개수를 출력하여라.
'''
input = sys.stdin.readline

N, M = map(int, input().strip().split(' ')) # 정점의 개수, 간선의 개수 #
graph = defaultdict(list)
rev_graph = defaultdict(list)
for m in range(M):
    x, y = map(int, input().strip().split(' ')) # 두 정점의 번호 -> 단방향 간선이 존재함 #
    graph[x].append(y)
    rev_graph[y].append(x)
S, T = map(int, input().strip().split(' ')) # 집 정점 번호, 회사 정점 번호 #
# st_nodes = set()
# ts_nodes = set()

# q = deque([S])
def rec_search(cur_node, visited, this_graph):
    '''도착 노드가 정해져 있지 않고 시작 노드에서 도달 할 수 있는, 연결된 모든 노드들을 찾는 방법이다.
    중복 도착이 허용이 되기 때문에 이렇게 해야 함.'''
    # global st_nodes, ts_nodes
    if visited[cur_node] == True:
        return
    visited[cur_node] = True
    # if dest_node == S:
    #     ts_nodes.add(cur_node)
    # else:
    #     st_nodes.add(cur_node)
    for next in this_graph[cur_node]:
        rec_search(next, visited, this_graph)
        # visited[next] = False
            
visited_ST = [False for _ in range(N+1)]
visited_ST[T] = True
rec_search(S, visited_ST, graph)
print(visited_ST)
visited_TS = [False for _ in range(N+1)]
visited_TS[S] = True
rec_search(T, visited_TS, graph)

r_visited_ST = [False for _ in range(N+1)]
rec_search(S, r_visited_ST, rev_graph)
r_visited_TS = [False for _ in range(N+1)]
rec_search(T, r_visited_TS, rev_graph)

cnt = 0
for i in range(1, N+1):
    if i == S or i == T:
        continue
    if visited_ST[i] and visited_TS[i] and r_visited_ST[i] and r_visited_TS[i]:
        cnt += 1
print(cnt)