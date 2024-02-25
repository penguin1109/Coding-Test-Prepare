""" BOJ 5639 - 이진 검색 트리
- 전위 순회한 결과를 바탕으로 후위 순회를 한 결과를 출력하여라.
"""

import sys
from collections import deque

input = sys.stdin.readline
pre_order_num = deque([])
tree = []
sys.setrecursionlimit(10**9)

class Node:
    def __init__(self, num):
        self.num = num
        self.left = None
        self.right = None
        
    def _check_child(self, n):
        if n < self.num: # 오른쪽 child #
            return 1
        elif n > self.num: # 왼쪽 child #
            return 2

class BinaryTree:
    def __init__(self):
        self.root = None
        
    def insert(self, num):
        if self.root is None:
            self.root = Node(num)
        else:
            self._insert_recursive(self.root, num)
            
    def _insert_recursive(self, root, num):
        if num < root.num: # if left child #
            if root.left is None:
                root.left = Node(num)
            else:
                self._insert_recursive(root.left, num)
        else: # if right child #
            if root.right is None:
                root.right = Node(num)
            else:
                self._insert_recursive(root.right, num)
    
    def delete(self, num):
        self.root = self._delete_recursive(self.root, num)
    
    def _delete_recursive(self, root, num):
        if root is None:
            return root
        if num < root.num: # if left node #
            root.left = self._delete_recursive(root.left, num)
        elif num > root.num: # if right node #
            root.right = self._delete_recursive(root.right, num)
        else: # 이 노드를 삭제해야 하는 경우 #
            if root.left is None: # leaf node인 경우 # (완전 이진 트리의 경우에는 left node가 없으면 무조건 right node도 없음)
                return root.right
            elif root.right is None: # leaf node인 경우 #
                return root.left
            '''left, right 자식이 모두 있는 경우
            방법 1 : 오른쪽 자식 중에서 가장 작은 값을 delete한 자리로 옮김
            방법 2 : 왼쪽 자식 중에서 가장 큰 값을 delet한 자리로 옮김
            '''
            root.num = self._get_min_value(root.right)
            root.right = self._delete_recursive(root.right, root.num)
        return root
    ## 후위 순회 ##
    def _postorder(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, root, result):
        if root is not None:
            self._postorder_recursive(root.left, result)
            self._postorder_recursive(root.right, result)
            result.append(root.num) # root를 제일 마지막에 #
    
    ## 전위 순회 ##
    def _preorder(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result 
    
    def _preorder_recursive(self, root, result):
        if root is not None:
            result.append(root.num)
            self._preorder_recursive(root.left, result)
            self._preorder_recursive(root.right, result)

    def _get_min_value(self, root):
        while root.left is not None:
            root = root.left
        return root.num

tree = BinaryTree()
while True:
    try:
        n = int(input())
    except:
        break
    pre_order_num.append(n)
#     tree.insert(n)
# # print(tree._preorder())
# # print("후위 순회 :", tree._postorder())
# postorder = tree._postorder()
# for n in postorder:
#     print(n)
# 전위 순회에서 처음은 무조건 root일수밖에 없음. #

def post_order_search(start_idx, end_idx):
    if start_idx > end_idx:
        return
    div = end_idx + 1
    for i in range(start_idx + 1, end_idx + 1):
        if pre_order_num[start_idx] < pre_order_num[i]: # start가 더 왼쪽 sub tree에 들어가 있는 경우에, 즉 마지막 left node이면서 sub tree들의 분기 지점이 되는 경우 #
            div = i
            break
    post_order_search(start_idx + 1, div - 1) # 왼쪽 sub tree부터 탐색 #
    post_order_search(div, end_idx) # 오른쪽 sub tree 탐색 #
    print(pre_order_num[start_idx]) # 최종 root 출력 #
            
post_order_search(0, len(pre_order_num)-1)
