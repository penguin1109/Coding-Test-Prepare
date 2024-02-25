""" BOJ 10799 - 쇠막대기
- 괄호의 조합들이 입력으로 주어지면 총장여진 쇠 막대기 조각의 개수를 구해야 한다.
- 레이저는 인접한 괄호
"""

import sys
input = sys.stdin.readline

arr = str(input().strip())
arr = arr.replace('()', 'l')
q = []
answer = 0
for a in arr:
    if a == 'l': # 레이저가 있을 때마다 아직 존재하는 막대기가 전부 한 조각씩 더 생김 #
        answer += len(q)
    elif a == '(': # 새로운 막대기 시작 # 
        q.append(a)
    else: # 막대기가 끝나는 경우에는 1만 더해줌 #
        q.pop()
        answer += 1
print(answer)
# while q:
#     temp = q.popleft()
#     if temp == '(':
#         stack.append(temp)
#     else:
#         # 레이저 발견 #
#         stack = stack.pop()
#         answer += len(stack)
    