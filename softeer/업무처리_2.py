import sys
from collections import deque
input = sys.stdin.readline

H, K, R = map(int, input().split(' ')) # 조직도 높이, 말단 업무 개수, 업무 진행 날짜 수
## 완전 이진 트리인 경우에는 1부터 시작했을 때 parent node를 n//2로 정할 수 있다. ##
## 하위 직원들이 업무를 위로 올린 다음날에 상사가 처리가 가능하기 때문에 Top-Down 방식으로 처리를 해 주어야 한다. ##
## 트리 순회, 탐색 문제는 이왕이면 재귀 함수로 구현을 해 주는 것이 좋다. ##
## 1부터 시작하면 짝수가 왼쪽 자식, 홀수가 오른쪽 자식이다. ##

num_nodes = 2 ** (H+1)
class Node:
    def __init__(self):
        self.left = deque([])
        self.right = deque([])
        self.task = deque([])
        self.depth = 0

Tree = [Node() for _ in range(num_nodes)]
for r in range(2 ** (H), num_nodes):
    todo = list(map(int, input().strip().split(' ')))
    Tree[r].task = deque(todo)

def init_depth(index, depth):
    global Tree
    if depth > H:
        return
    Tree[index].depth = depth
    init_depth(index*2, depth+1)
    init_depth(index*2+1, depth+1)

init_depth(1, 0)

answer= 0
def work(index, depth, day):
    global answer, Tree
    if depth > H:
        return
    if depth == H and Tree[index].task:
        job = Tree[index].task.popleft()
        if index % 2 == 0: #왼쪽부하인경우#
            Tree[index//2].left.append(job)
        else:
            Tree[index//2].right.append(job)
    elif depth < H:
        if day % 2 == 0 and Tree[index].right: #짝수번째날#
            job = Tree[index].right.popleft()
            if index == 1:
                answer += job
            elif index%2 == 0: #왼쪽부하인경우->parent인 index//2의 left deque에 넣어줌#
                Tree[index//2].left.append(job)
            else:
                Tree[index//2].right.append(job)
            
        elif day % 2 == 1 and Tree[index].left:
            job = Tree[index].left.popleft()
            if index == 1:
                answer += job
            elif index % 2 == 0: #왼쪽부하인경우#
                Tree[index//2].left.append(job)
            else:
                Tree[index//2].right.append(job)

    work(index*2, depth+1, day)
    work(index*2+1, depth+1, day)
    
for r in range(1, R+1):
    work(1, 0, r)
    
print(answer)