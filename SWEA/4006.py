``` 해결 방법
- 사용한 알고리즘: 크루스칼 알고리즘즘
- 알고리즘 소개:
  MST를 기반으로 하는 최단거리 알고리즘이다. 
  보통 전체 간선이 포함되는 경로의 최단 거리를 구할 때에 많이 사용한다.
  Union-Find의 개념을 사용하는데, 그리디 기반이기도 하기 때문에 우선 간선의 가중치에 맞게 오름차순으로 정렬을 하고, MST에서 cycle을 만들지 않는 간선을 우선적으로 선택한다.
  1. Find연산에서는 두 노드의 parent가 동일한지 확인함
  2. Union 연산에서는 두 노드가 cycle을 이루지 않으면 연결을 해주기 위해서 parent 배열을 갱신한다.
```
def get_root(parent, a):
  if (parent[a] == a):
    return a
  parent[a] = get_root(parent, parent[a])
  return parent[a]

def union_parent(a, b, parent):
  pa = get_root(parent, a)
  pb = get_root(parent, b)
  if (pa < pb):
    parent[b] = a ## b의 부모가 a
  else:
    parent[a] = b

def find_parent(a, b, parent):
  pa = get_root(parent, a)
  pb = get_root(parent,b)
  if (pa == pb):
    return True
  else:
    return False

from queue import PriorityQueue
if __name__ == "__main__":
  T = int(input())
  for test_case in range(T):
    N = int(input()) ## 도시의 수
    M = int(input()) ## 도로 후보의 수

    parent = [int(i) for i in range(N+5)] # 부모 배열 정의 -> 처음에는 자기 자신이 부모

    q = [] # PriorityQueue()
    for m in range(M):
      s, e, c = map(int, input().split(' ')) ## 도로 후보의 각 도시의 번호, c는 도로를 건설하는데 드는 비용
      q.append((c, s, e)) # q.put((c, s, e)) # 단방향이긴 한데 한쪽만 넣어주는 상황 (왜냐면 모든 방향으로의 간선의 가중치가 동일하기 때문)
    
    answer = 0
    cnt = 0
    idx = 0
    q = sorted(q)
    while (len(q) > 0):
      if (cnt == N-1):
        break
      dist, a, b = q[idx] # q.get() 
      idx += 1
      if find_parent(a, b, parent) == False:
        union_parent(a, b, parent)
        answer += dist
        cnt += 1
      
    print(f"#{test_case+1} {answer}")
