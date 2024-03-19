import sys
from collections import deque

input = sys.stdin.readline
'''[출력] 완료된 업무들의 번호의 합
직원들이 업무를 올린 뒤에 처리가 가능한 상황이기 때문에 Top-Down 방식으로 트리를 순회해야 한다.
'''
H, K, R = map(int, input().strip().split(' ')) # 조직도 높이, 대기 업무 개수, 진행 날짜 수 #
num_nodes = 2**(H+1)-1
Tree = [deque([]) for _ in range(num_nodes)]
Left = [deque([]) for _ in range(num_nodes)]
Right = [deque([]) for _ in range(num_nodes)]

def get_parent_node(n):
    if n == 0:
        return n
    if n%2 == 0:
        return (n-2) // 2
    else:
        return (n-1) // 2
        
for n in range(2**H-1, num_nodes):
    todo = list(map(int, input().strip().split(' '))) # 왼쪽의 말단 직원부터 대기 업무 주어짐 #
    Tree[n] = deque(todo)
    
answer = 0
for r in range(1, R+1):
# for r in range(R):
    # (1) 업무 처리 하고 상단에 올려주기 #
    for n in range(2**H-1): 
        if r % 2 == 0: # 짝수 -> 오른쪽 부하 #
            if Right[n]:
                if n == 0:
                    answer += Right[n].popleft()
                else:
                    parent = get_parent_node(n)
                    if n%2 == 0:
                        Right[parent].append(Right[n].popleft()) # 왼쪽 노드는 홀수 오른쪽 노드는 짝수 #
                    else:
                        Left[parent].append(Right[n].popleft())
        else:
            if Left[n]:
                if n == 0:
                    answer += Left[n].popleft()
                else:
                    parent = get_parent_node(n)
                    if n%2 == 0: # n, 즉 내가 짝수니까 상사의 Right 배열에 일을 올려주고 홀수 번째 날이니까 왼쪽 부하가 올린 업무 수행 #
                        Right[parent].append(Left[n].popleft()) # 왼쪽 노드는 홀수 오른쪽 노드는 짝수 #
                    else:
                        Left[parent].append(Left[n].popleft())
    # (2) 말단 노드들 처리하기 #
    for n in range(2 ** H-1, num_nodes):
        if Tree[n]:
            parent = get_parent_node(n)
            if n % 2 == 0:
                Right[parent].append(Tree[n].popleft())
            else:
                Left[parent].append(Tree[n].popleft())
print(answer)