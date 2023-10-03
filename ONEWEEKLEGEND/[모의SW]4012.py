""" 요리사
<조건>
- 2명의 손님. N개의 식재료
- 식재료를 N//2개로 나누어서 2개의 음식 A, B를 하고자 한다.
- 비슷한 맛의 음식을 만들기 위해서 A, B의 음식 맛의 차이가 최소가 되도록 재료가 배분 되어야 한다.
- 식재료 i, j는 같이 요리하면 시너지 S_{ij}가 발생한다.
- 각 음식의 맛은 음식을 구성하는 식재료들간의 시너지의 합이다.

<문제>
N개의 식재료로 만든 음식 A, B의 맛의 차이가 최소가 되는 경우의 최솟값을 출력하여라.

<제약>
4 <= N <= 16의 짝수
1 <= S_{ij} <= 20000
"""

from itertools import combinations

def single_taste(arr, synergy):
    taste = 0
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            taste += synergy[arr[i]][arr[j]]
            taste += synergy[arr[j]][arr[i]]
    return taste
def calc_taste(synergy):
    min_taste_diff = 1e+10 # 각각의 음식의 맛을 저장하기 위한 변수

    foodN = len(synergy)
    allFood = [int(i) for i in range(foodN)]
    hubos = list(combinations([int(i) for i in range(foodN)], foodN//2))

    tot = sum([sum(s) for s in synergy])
    for hubo in hubos:
        A = hubo
        B = list(set(allFood) - set(hubo))
        ta = single_taste(A, synergy)
        tb = single_taste(B, synergy)
        min_taste_diff = min(min_taste_diff, abs(ta-tb))
    return min_taste_diff


def recursive_taste(synergy,i, a, b):
    global answer
    n = len(synergy)
    A, B = len(a), len(b)
    if A > n//2:
        return

    if B > n//2:
        return
    if i == len(synergy) and len(a) == len(synergy) // 2 and len(b) == len(synergy) // 2:
        ta = single_taste(a, synergy)
        tb = single_taste(b, synergy)
        answer = min(answer, abs(ta-tb))
        return

    recursive_taste(synergy, i+1, a + [i], b)
    recursive_taste(synergy, i+1, a, b+[i])

T = int(input())
for tc in range(T):
    N = int(input()) # 식재료의 개수
    synergy = []
    for n in range(N):
        synergy.append(list(map(int, input().strip().split(' '))))
    answer = 1e+10 ## MIN TASTE DIFF
    recursive_taste(synergy, 0, [], [])
    print(f"#{tc+1} {answer}")