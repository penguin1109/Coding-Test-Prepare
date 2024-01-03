import sys
input = sys.stdin.readline

W, N = map(int, input().strip().split(' ')) # 배낭 무게, 귀금속 종류 #

golds = []

for n in range(N):
    m, p = map(int, input().strip().split(' '))
    golds.append([p, m])
golds.sort(key = lambda x: -x[0])

"""
sol1 : greedy -> 2/5
sol2 : greedy 맞는데 실수를 했음 left = valid로 valid == 0일 때도 갱신을 했어야 했는데
안해서... 당연히 시간초과가 아니고서도 틀린 답이 구해짐
"""
left = W
answer = 0
for i, (price, mass) in enumerate(golds):
    valid = max(0, left-mass)
    if valid == 0:
        answer += price * left
        left = valid
    else:
        answer += price * mass
        left = valid
    if left == 0:
        break
    
print(answer)