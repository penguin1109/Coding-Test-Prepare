import sys
import heapq
import copy
input = sys.stdin.readline

N, B = map(int, input().strip().split(' '))
qual = sorted(list(map(int, input().strip().split(' '))))

'''성능을 d만큼 향상시키는데 드는 비용 -> d**2
한 컴퓨터에 두번 이상 업그레이드를 할 수는 없음
B원이 총 예산이고, B원 이하의 총 비용으로 업그레이드를 하여 성능이 가장 낮은 컴퓨터의 성능을 최대화 해야 함
[풀이] 미리 최대 비용을 정해 놓고 가능한지 확인해보기?
'''
answer = 0

def check_valid(min_qual_tobe):
    '''작은 수부터 순차적으로 min_qual_tobe가 되도록 하여서 B가 모자라면 끝'''
    leftover = B
    for ai, a in enumerate(qual):
        if a < min_qual_tobe:
            need = min_qual_tobe - a
            if leftover >= need ** 2:
                leftover -= need**2
            else:
                return False
        else:
            return True
    return True

def binary_search(left, right):
    # print(left, right)
    if left == right:
        valid = check_valid(left)
        if valid == False:
            print(left-1)
        else:
            print(left)
        return
    mid = (left + right) // 2
    valid = check_valid(mid)
    if valid == True: # 가능하니까 target을 키워보자! #
        binary_search(mid+1, right)
    else:
        binary_search(left, mid)
    
max_amount = max(qual) + int(B**0.5)
binary_search(min(qual), max_amount)
# for min_qual_tobe in range(min(qual), max_amount):
#     valid = check_valid(min_qual_tobe)
#     if valid == True:
#         continue
#     else:
#         print(min_qual_tobe-1)
#         exit(0)