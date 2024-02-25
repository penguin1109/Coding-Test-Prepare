""" BOJ 10773 - 제로
- 잘못된 수를 부를 때마다 0을 외쳐서, 최근에 쓴 수를 지우게 시킨다.
[출력]
모든 수를 받아 적은 후 그 수의 합
"""
import sys
from collections import deque

input = sys.stdin.readline

K = int(input().strip()) 
q = deque([])

for k in range(K):
    called = str(input().strip())
    if called == '0':
        q.pop()
    else:
        q.append(int(called))
print(sum(q))
    