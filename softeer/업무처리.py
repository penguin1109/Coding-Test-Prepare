""" 업무 처리
<문제 설명>
- 완전 이진 트리 모양의 부서 업무 조직
    -> 여기서 조직도의 모양이 **완전 이진 트리**라는 점이 제일 중요하다.
- 조직도 트리의 높이는 H
- 부하 직원이 없으면 말단 직원 (완전 이진 트리이기 때문에 모두 root까지 올라가는 거리가 동일)
- R일동안 업무가 진행이 되고, 말단 직원만 처음에 K개의 순서가 정해진 업무를 갖고 있다.
- 홀수번 날짜에는 왼쪽, 짝수번 날짜에는 오른쪽 직원이 올린 업무를 부사장이 처리
<출력>
: 처리가 완료된 업무들의 번호의 합
"""
from collections import deque

H, K, R = map(int, input().split(' ')) # 조직도 높이, 말단 업무 개수, 업무 진행 날짜 수

def work(index, depth, day):
    global answer
    if depth > H:
        return

    ## 말단 노드라면 task 하나를 위로 올려야 한다.
    if depth == H and tree[index].task:
        job = tree[index].task.popleft()
        if index % 2 == 0: # 왼쪽 부하인 경우
            tree[index // 2].left.append(job)
        else: # 오른쪽 부하인 경우
            tree[index // 2].right.append(job)
    ## 부하 직원이 있다면 작업물을 상사에게 전달
    elif depth < H:
        if day % 2 != 0 and tree[index].left:
            job = tree[index].left.popleft()
            if index == 1: ## 제일 위에 있는 노드인 경우
                answer += job # 업무 완전 처리 상황
            else:
                if index % 2 == 0: # 왼쪽 부하
                    tree[index // 2].left.append(job)
                else: # 오른쪽 부하
                    tree[index // 2].right.append(job)
        if day % 2 == 0 and tree[index].right: # 짝수 -> 오른쪽
            job = tree[index].right.popleft()
            if index == 1:
                answer += job
            else:
                if index % 2 == 0:
                    tree[index // 2].left.append(job)
                else:
                    tree[index // 2].right.append(job)
    work(index * 2, depth + 1, day)
    work(index * 2 + 1, depth+1, day)
    

def init(index, depth):
    global tree, N, H
    if depth > H:
        return
    tree[index].depth = depth
    init(index * 2, depth+1)
    init(index *2+1, depth+1)
    
class Node:
    def __init__(self):
        super(Node, self).__init__()
        self.depth = 0
        self.left = deque([]) # 현재 노드의 왼쪽 말단 부하가 보내준 작업물
        self.right = deque([]) # 현재 노드의 오른쪽 말단 부하가 보내준 작업물
        self.task = deque([])
    
tree = [Node() for _ in range(2 ** (H+1))]
init(1, 0)

for i in range(2 ** H, 2 ** (H+1)):
    tree[i].task = deque(list(map(int, input().split(' ')))) # 말단 노드에 수행해야 하는 업무의 번호 입력

answer = 0

for r in range(R):
    work(1, 0, r+1)

print(answer)