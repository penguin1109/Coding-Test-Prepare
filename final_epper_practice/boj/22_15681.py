""" BOJ 15681 - 트리와 쿼리
"""
from collections import defaultdict
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**8)
# 트리의 정점의 개수, 루트의 번호, 쿼리의 수 #
N, R, Q = map(int, input().strip().split(' '))
tree = defaultdict(list)
child = defaultdict(list)
parent = [i for i in range(N+1)]

def make_tree(cur_node, parent_node):
    global parent, child, tree
    for node in tree[cur_node]:
        if node != parent_node:
            child[cur_node].append(node)
            parent[node] = cur_node
            make_tree(node, cur_node)
            
def count_subtree_nodes(cur_node):
    global subtree_size
    if visited[cur_node] == True:
        return
    visited[cur_node] = True
    subtree_size[cur_node] = 1 # subtree의 크기에 자기자신을 추가해줌 #
    for node in child[cur_node]:
        count_subtree_nodes(node)
        subtree_size[cur_node] += subtree_size[node]
        
for n in range(N-1):
    u, v = map(int, input().strip().split(' ')) 
    tree[u].append(v)
    tree[v].append(u)
    
make_tree(cur_node=R, parent_node=-1) ## 재귀적으로 간선 정보 지키면서 트리 만들기 ##
cases = []
visited = [False for _ in range(N+1)]

for q in range(Q):
    case_u = int(input().strip())
    cases.append(case_u)
    
'''
(1) 문제를 제대로 읽자. 처음에는 어떤 root를 기준으로 전체 트리를 만들어야 하는지 (왜냐면 방향이 없는 트리이기 때문에 무조건 root가 정해져야 그 하위 parent, child, subtree등을 정할 수 있기 때문이다.)
그래서 보니 첫줄에 Root를 입력으롲 주는 것을 알 수 있었음
(2) 이 문제가 DP를 활용해야 했던 이융해야 했고, 그렇기 떄문에 각각의 노드에 대한 subtree의 크기 배열을 DP의 memoization을 이용하여 시간초과 없이 구할 수 있었다.

'''
subtree_size = [0 for _ in range(N+1)] 
for case in cases:
    # subtree_size = [0 for _ in range(N+1)]
    count_subtree_nodes(case)
    print(subtree_size[case])