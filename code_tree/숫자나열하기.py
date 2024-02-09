from collections import defaultdict, deque

def top_sort(graph, indegree):
    result = []
    q = deque()
    
    for node in graph:
        if indegree[node] == 0:
            q.append(node)
    
    while q:
        cur = q.popleft()
        result.append(cur)
        
        for next in graph[cur]:
            indegree[next] -= 1
            if indegree[next] == 0:
                q.append(next)
    return result


N, M = map(int, input().strip().split(' '))
graph = defaultdict(list)
indegree = defaultdict(int)

for _ in range(M):
    a,b = map(int, input().strip().split(' '))
    graph[a].append(b)
    indegree[b] += 1

result = top_sort(graph, indegree)
print(*result)