import sys
# sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline
from collections import deque

def check_valid(s:str):
    symbols = ['(', ')', '[', ']']
    s = deque([i for i in s if i in symbols])
    left = deque([])
    while s:
        a = s.popleft()
        if a == '(' or a == '[':
            left.append(a)
        else:
            if left:
                top = left.pop()
                if a == symbols[1] and top == symbols[0] or a == symbols[3] and top == symbols[2]:
                    continue
                else:
                    return False
            else:
                return False
    
    if len(left) == 0: ## left 배열이 남아있는게 없어야 완전히 모든 문자열이 완전하다고 할 수 있다. ##
        return True
    return False
while True:
    s = str(readl().rstrip())
    if s == '.':
        break
    ret = check_valid(s)
    if ret == True:
        print('yes')
    else:
        print('no')
    