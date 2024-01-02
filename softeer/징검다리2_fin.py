import sys

input = sys.stdin.readline
N = int(input().strip())
rocks = list(map(int, input().strip().split(' ')))

def binary_search(arr, num):
    # 배열에서 몇번쨰 index에 num이 들어갈 수 있는지 #
    left, right = 0, len(arr)
    mid = (left+right)//2
    while left < right:
        mid = (left+right)//2
        if arr[mid] < num: # 오른쪽에서 탐색이 필요 #
            left = mid+1
        else: # 왼쪽에서 탐색이 필요 #
            right = mid
    return right # the index that <num> can be placed in the array arr #

def bin_search_lis(arr):
    global N
    dp = [1 for _ in range(N)]
    x = [arr[0]] ## X 배열은 dp[i]의 최장 수열의 길이일때 마지막 숫자들의 최솟값을 저장한다. ##
    dp_inv = [1 for _ in range(N)]
    x_inv = [arr[-1]]
    
    for i in range(1, N):
        num = arr[i]
        if num > x[-1]:
            x.append(num)
            # dp.append(max(dp)+1)
        else:
            idx = binary_search(x, num)
            x[idx] = num
        
        num = arr[N-1-i]
        if num > x_inv[-1]:
            x_inv.append(num)
            # dp_inv.append(max(dp_inv)+1)
        else:
            idx = binary_search(x_inv, num)
            x_inv[idx] = num

        dp[i] = len(x)
        dp_inv[i] = len(x_inv)
    answer = 0
    # print("dp : ", dp)
    # print("X : ", x)
    # print("dp inv : ", dp_inv)
    # print("X inv : ", x_inv)
    for i in range(N):
        answer = max(answer, dp_inv[N-1-i] + dp[i])
    return answer - 1

answer = bin_search_lis(rocks)
print(answer)
    
    
    


    