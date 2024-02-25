""" BOJ 1213 - 팰린드롬 만들기
- 영어 이름 -> 팰린드롬으로 만들기 (순서를 바꿔서)
- 여러 방법이 있으면 사전 순으로 앞서는 것을 선택

[풀이 방법] 순서 그 자체가 그렇게 중요한 것은 아님. 그냥 잘 조합해서 문자열만 구하면 됨.
"""

import sys
input = sys.stdin.readline

name = str(input().strip())

def make_palindrome(name, is_odd:bool=False):
    from collections import defaultdict
    cnt_dict = defaultdict(int)
    for a in name:
        cnt_dict[a] += 1
        
    middle = []
    others = []
    ''' 실수 하지 말자 !!
    -> 생각보다 실버 레벨이어도 한 큐에 정확하게 맞추는게 쉽지만은 않은 것 같다.
    -> 음,, 어쨌든 여기서 name의 길이가 홀수일때, 짝수일때 모두 palindrome을 만들 수 있기 때문에 이 부분을 헷갈려선 안됬었고,
    홀수일때나 짝수일때 모두 개수가 홀수개인 알파벳이 2개 이상이면 만들 수 없다.
    '''
    for alph, n in cnt_dict.items():
        if n % 2 == 1:
            middle.append(alph)
        else:
            others.append(alph)

    if len(middle) > 1:
        return False
    
    answer = []
    center = '' if len(middle) == 0 else middle[0]
    for a in others:
        answer.append(a * (cnt_dict[a] // 2))
    
    if is_odd:
        if cnt_dict[center] != 1:
            answer.append(center * (cnt_dict[center] // 2))
    answer = sorted(answer)
    prefix = ''.join(answer)
    palindrome = prefix
    palindrome += center
    palindrome += prefix[::-1]
    
    return palindrome
        
    
answer = make_palindrome(name, is_odd = len(name) % 2 == 1)

if answer == False:
    print("I'm Sorry Hansoo")
else:
    print(answer)
    