""" BOJ 2840 [행운의 바퀴]
- 바퀴는 시계 방향으로만 돌아감
- 연속해서 K번동안 돌리면서 글자가 변하는 횟수와 어떤 글자에서 멈췄는지를 적음. 
[출력] 어떤 글자인지 결정하지 못했으면 ? || 만족하는 바퀴가 없으면 ! || 마지막 회전에서 화살표부터 시계방향의 알파벳
"""

import sys
from collections import defaultdict
input = sys.stdin.readline


N, K = map(int, input().strip().split(' ')) # 바퀴의 칸의 수, 바퀴를 돌리는 횟수 #

wheel = ['?' for _ in range(N)] # 미리 바퀴의 예상 정보를 저장할 공간을 만들어 줌 #
answer = ''
idx = 0
duplicate_check = defaultdict(int)

for k in range(K):
    s, alph = map(str, input().strip().split(' ')) # 몇번 바뀌었는지, 회전 멈췄을 때 글자 #
    s = int(s)
    idx = idx - s + N # 시계방향으로 회전하니까 반시계방향으로 idx를 이동하면서 알파벳을 트래키해 주어야 한다. #
    idx %= N
    if wheel[idx] == '?':
        wheel[idx] = alph
        ''' 이 부분에서 은근히 반례 트래킹이 어려웠다.
        -> 생각외로 시간이 오래 걸려서 기분이 나빴음.
        -> 어쨌든 보니깐 문제가 성립하기 위해서는 "중복되는 알파벳이 전혀 없다"는 조건이 만족되어야 하기 때문에 이걸 확인해 주어야 했고,
        이미 확인한 자리면 duplicate_check[alpha] > 0이어도 문제가 없다.
        -> 그리고 "시계방향 회전"이기 때문에 변환은 "반시계방향"이었어야 했다.
        '''
        if duplicate_check[alph] > 0:
            answer = '!'
        duplicate_check[alph] += 1
    
    else:
        if wheel[idx] != alph:
            answer = '!'
            
if (answer == '!'):
    print(answer)
else:
    ret_wheel = wheel[idx:]
    ret_wheel.extend(wheel[:idx])
    answer = ''.join(ret_wheel)
    print(answer)       
# print(''.join(wheel))

    
    