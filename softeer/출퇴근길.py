""" 출퇴근길
<문제 설명>
- N개의 정점, M개의 간선으로 이루어진 단방향 그래프로 출퇴근길을 나타냄
- 출근길에는 S가, 퇴근길에는 T가 여러번 등장해도 됨
<문제 출력>
: 출근길과 퇴근길에 모두 포함 가능한 정점의 개수를 세어라
"""
import sys
sys.setrecursionlimit(10 ** 6) ## 파이썬은 1000개까지 밖에 재귀 함수 호출이 안되서 호출 제한을 늘려주어야 한다.
N, M = map(int, input().split(' ')) # 정점 개수, 간선 개수
adj = [[] for _ in range(N)]
adjR = [[] for _ in range(N)]
for m in range(M):
    x, y = map(int, input().split(' '))
    adj[x-1].append(y-1)
    adjRh[y-1].append(x-1)

home, work = map(int, input().split(' '))
home -= 1;work -= 1;

def dfs(now, dest, graph, visited):
    if visited[now] == 1:
        return
    else:
        visited[now] = 1
        for next_node in graph[now]:
            dfs(next_node, dest, graph, visited)

from_s, from_s_inv = [0] * N, [0] * N
from_t, from_t_inv = [0] * N, [0] * N
from_s[work] = 1
dfs(home, work, adj, from_s)
dfs(home,work,adjR, from_s_inv)

from_t[home] = 1
dfs(work,home, adj, from_t)
dfs(work,home, adjR, from_t_inv)

answer = 0

## 여기 loop에서 은근히 오래 걸릴수도 있을 것 같음
for idx, (t, f, ti, fi) in enumerate(zip(from_s, from_t, from_s_inv, from_t_inv)):
    if idx != work and idx != home:
        if t == True and f == True and ti==True and fi == True:
            answer += 1
print(answer)
    
            
