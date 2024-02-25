""" 프로그래머스 - 매출하락최소화
- 트리에 저장된 직원의 정보는 (직원번호, 하루 평균 매출액)

<워크샵 참가 조건>
- 모든 팀은 최소 1명 이상으로 참가를 해야 함.
- 매출 손실을 최소화해야 하기 때문에 하루 평균 매출액의 합이 최소여야 함.

[입력]
- 직원들의 하루 평균 매출액을 저장한 배열 sales
- 팀장-팀원의 관계를 나타내는 2차원 배열 links

[출력]
- 최소화된 매출액의 합

[해결방법]
(1) 무지성으로 모든 경우에 대해서 sum_sales를 dfs로 구해서 최솟값 찾기 -> 시간초과랑 런타임 에러 발생 (41.9 / 100)
(2) 정답 방법은 해설을 조금은 참고할 수밖에 없었다.
    - 우선 기본적으로 DFS에다가 DP를 함께 적용해서 풀어야 하는 문제였다.
    - 계산 결과를 DP에 계속 저장해서 DP의 어느 부분에 결괏값이 저장되도록 해야 한다.
    -> 이 풀이 방법 대로 문제를 해결 했는데 계속 10~20 번까지 시간초과가 발생하는 문제가 있었다.
    - 각 팀장이 참석 하는 경우 / 하지 않는 경우로 나누어서 문제를 풀어야 한다.
"""
import copy
from collections import defaultdict
sales = []
visited = []
dp = []

def get_parent(node, parent):
    pn = parent[node]
    if node == pn:
        return node
    else:
        return get_parent(pn, parent)
    
def union(a, b, parent):
    pa = get_parent(a, parent)
    pb = get_parent(b, parent)
    
    if pa == pb:
        return
    else:
        if pa < pb:
            parent[b] = a
        else:
            parent[a] = b

def debug_tree(tree:dict):
    for key, value in tree.items():
        print(f"팀장 {key} => {value}")

class Tree:
    def __init__(self, N):
        super(Tree, self).__init__()
        self.leaf_node = [i for i in range(1, N)]
        # self.teams = {}
        self.teams = defaultdict(list)
        self.parent = [i for i in range(N)]
    
    def _add_node(self, leader, member):
        # if leader not in self.teams:
        #     self.teams[leader] = [leader]
        self.teams[leader].append(member)
        if leader in self.leaf_node:
            self.leaf_node.remove(leader)
        self.parent[member] = leader
    
def dfs(node, tree):
    global dp
    global visited
    global sales
    track = 0
    team_select = 0
    # visited[node] = True
    if visited[node] == True:
        return
    visited[node] = True
    for child in tree[node]:
        dfs(child, tree)
        # if visited[child] == False:
        #     dfs(child, tree,) #  dp, sales, visited)
        #     # visited[child] = True
        # if dp[child][1] < dp[child][0]:
        #     track += dp[child][1]
        #     team_select += 1
        # else:
        #     track += dp[child][0]
    
    ## CASE1 : 팀장이 워크샵에 참여하는 경우 ##
    dp[node][1] = track + sales[node]
    ## CASE2 : 팀장은 워크샵에 참여하지 않지만 팀원 중 한명이라도 참석을 한 경우 ##
    if team_select != 0: # 같은 팀에 최솟값이 되는 경우에 참여하는 사람이 있는 경우 #
        dp[node][0] = track
    ## CASE3 : 팀장이 워크샵에 참여하지 않고 팀원 중 한명도 최솟값 경우에 참석을 하지 않는 경우 ##
    else: # 같은 팀에 참여하는 사람이 하나도 없는 경우 #
        list_arr = [dp[c][1] - dp[c][0] for c in tree[node]] # 다른 노드 c에 대해서 c를 포함하였을 때의 cost를 더하고 포함하지 않은 dp[c][0]을 빼야 하기 때문 #
        if list_arr:
            dp[node][0] = track + min(list_arr)
        else: # leaf node child인 경우 #
            dp[node][0] = track
answer = 0
def solution(s, links):
    global dp
    global visited
    global sales
    sales = s
    sales.insert(0, -1)
    global answer

    # parent = [i for i in range(len(sales))] # 속한 팀의 팀장 구하기 #
    # tree, member_tree = make_tree(links)
    # tree, childs = make_tree(links)
    tree = Tree(len(sales))
    for link in links:
        tree._add_node(*link)
    
        
    
    dp = [[0, 0] for _ in range(len(sales))] # (현재 노드가 포함되지 않을 때 최소 , 현재 노드가 포함될 때 최소) #
    visited = [False for _ in range(len(sales))]
    # print("Leaf " , tree.leaf_node)
    for child in tree.leaf_node:
        dp[child][1] = sales[child]
        # visited[child] = True 
    # q = deque(tree.leaf_node)
    
    # while q:
    #     node = q.popleft()
    #     parent = tree.parent[node]
    #     if visited[parent] == False:
    #         dfs(parent, tree.teams, dp, sales, visited)
    #         visited[parent] = True
    #         q.append(parent)
    
    
    dfs(1, tree.teams,) #  dp, sales, visited)
        # print(q)
    print(dp)
    # dfs(1, tree, dp, sales)
    
    # print(dp)
    answer = min(dp[1])
    # debug_tree(tree)
    # visited = [False for _ in range(len(sales)+1)]
    # visited_member = [False for _ in range(len(sales)+1)]
    # dfs(visited, visited_member, 0, 0, tree, member_tree, sales)
    
    return answer

if __name__ == "__main__":
    SALES = [
        [14, 17, 15, 18, 19, 14, 13, 16, 28, 17],
        [5, 6, 5, 3, 4],
        [5, 6, 5, 1, 4],
        [10, 10, 1, 1]
    ]
    
    LINKS = [
        [[10, 8], [1, 9], [9, 7], [5, 4], [1, 5], [5, 10], [10, 6], [1, 3], [10, 2]],
        [[2,3], [1,4], [2,5], [1,2]],
        [[2,3], [1,4], [2,5], [1,2]],
        [[3,2], [4,3], [1,4]]
    ]
    
    for sales, links in zip(SALES, LINKS):
        print(solution(sales, links))
        
        