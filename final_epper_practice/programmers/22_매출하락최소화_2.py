from dataclasses import dataclass, field
import functools
from itertools import combinations
import sys

@dataclass
class Node:
    sales : int
    dp_include_self : int = field(default=sys.maxsize)
    dp_exclude_self : int = field(default=sys.maxsize)
    children : list = field(default_factory=list)
    parent : int = field(default=-1)

def calculate_min_sales(include_set, exclude_set, nodes):
    sales = 0
    for node in include_set:
        sales += nodes[node].dp_include_self
    for node in exclude_set:
        sales += nodes[node].dp_exclude_self
        
    return sales
        

def dfs(v, nodes):
    if not nodes[v].children: ## IF LEAF NODE ##
        nodes[v].dp_include_self = nodes[v].sales
        nodes[v].dp_exclude_self = 0
        return 
    ## (1) 먼저 자식 노드들에 대해서 dfs로 최솟값 dp 배열을 업데이트 한다. ##
    for child in nodes[v].children:
        dfs(child, nodes)
    ## (2) child들 중에서 leaf node와 nonleaf node 구분 ##
    nonleaf_children = set([c for c in nodes[v].children if nodes[c].children != []])
    leaf_children = set(nodes[v].children) - nonleaf_children
    children = set(nodes[v].children)
    combs = []
    for i in range(len(nonleaf_children)+1):
    # for i in range(len(children)+1):
        combs += list(combinations(nonleaf_children, i)) # 이 조합에 포함된 children은 야유회에 간다는 가정 #
        # combs += list(combinations(children, i)) # 이 조합에 포함된 children은 야유회에 간다는 가정 #
        
    
    ## (3) 자신을 포함하는 경우 ##
    for comb in combs:
        exclude_set = set(nodes[v].children) - set(comb)
        include_set = comb
        ret_sales = calculate_min_sales(include_set, exclude_set, nodes)
        ret_sales += nodes[v].sales
        nodes[v].dp_include_self = min(nodes[v].dp_include_self, ret_sales)
    
    ## (4) 자신을 포함하지 않는 경우 ##
    for comb in combs:
        # if not comb:
        if comb == ():
            continue
        exclude_set = set(nodes[v].children) - set(comb)
        include_set = comb
        ret_sales = calculate_min_sales(include_set, exclude_set, nodes)
        nodes[v].dp_exclude_self = min(nodes[v].dp_exclude_self, ret_sales)
    
    # ## (5) 자신을 포함하지 않고 leaf node만 포함하는 경우 (즉, nonleaf node는 모두 제외를 하고 leaf node만 포함하는 경우) ##
    # 이게 말이 되는 이유가 1번의 자식들중 2,3,4가 있다고 할 때 2번은 leaf node이고 3,4는 non-leaf node일수 있기 때문이다. #
    # 그렇지만 굳이 나눠서 처리하는 이유는 정말 시간 초과 때문이 맞는 것 같다. #
    if leaf_children: # leaf children도 존재하는 경우 #
        leaf_children_min_sales = min((nodes[c].sales for c in leaf_children)) 
        ret_sales = sum(map(lambda x : nodes[x].dp_exclude_self, nonleaf_children)) + leaf_children_min_sales
        nodes[v].dp_exclude_self = min(ret_sales, nodes[v].dp_exclude_self)

        
    
def solution(sales, links):
    nodes = [None] + [Node(sales=sale) for sale in sales]
    for parent, child in links:
        nodes[parent].children.append(child)
        nodes[child].parent = parent
    
    dfs(1, nodes)
    # print(nodes)
    
    answer = min(nodes[1].dp_exclude_self, nodes[1].dp_include_self)
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
        
        