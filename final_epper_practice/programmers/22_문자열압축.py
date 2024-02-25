""" 프로그래머스 - 문자열 압축
- 문자열에서 같은 값이 연속해서 나타나는 경우에 그 문자의 개수와 반복되는 값으로 나타내어 더 짧은 문자열로 줄여서 표현
[풀이 방법] 백트래킹으로 모든 경우에 대해서 다 길이를 구해서 비교를 하는 방법밖에 없다.
**파이썬에서는 deque(덱)이 popleft()가 됨. `from collections import deque` 기억해 둬야 함**
"""
from collections import deque
def check(s, n):
    q = deque([])
    for i in range(0, len(s), n):
        q.append(s[i:i+n])
    # print(q)
    prev = q.popleft()
    answer = ''
    track = 1
    while q:
        temp = q.popleft()
        if temp == prev:
            track += 1
        else:
            if track != 1:
                answer += f"{track}{prev}"
            else:
                answer += prev
            prev = temp
            track = 1
    if track == 1:
        answer += prev
    else:
        answer += f"{track}{prev}"
        
    return answer
    
    
    
    
def solution(s):
    answer = len(s)
    for i in range(1, len(s)):
        temp = check(s, i)
        answer = min(answer, len(temp))
    return answer

if __name__ == "__main__":
    s = "ababcdcdababcdcd"
    print(solution(s))