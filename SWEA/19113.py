import sys
sys.stdin = open("../input.txt", "r")

T = int(input())

def get_discount_price(n):
    disc = n // 4
    disc *= 3
    return disc

# def find_num(arr, idx):
def find_num(arr):
    # left, right = 0, idx
    left, right = 0, len(arr)
    num = arr[-1]
    discount_price = get_discount_price(num)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == discount_price:
            return mid
        elif arr[mid] < discount_price:
            left = mid + 1
        else: 
            right = mid

            

for test_case in range(1, T+1):
    N = int(input()) # 상점의 품목 수 #
    p_list = list(map(int, input().strip().split(' '))) # 인쇄한 정수 2N개 #
    # visited = [False for _ in range(N*2)]
    answer = []
    
    for n in range(N):
        # if visited[n] == True:
        #     continue
        # visited[n] = True
        # idx = find_num(p_list, n)
        idx = find_num(p_list)
        # print(idx, p_list)
        if idx != None:
            disc = p_list[idx]
            p_list.remove(p_list[idx])
            answer.append(disc)
        # print(f"found : {get_discount_price(p_list[n])} discounted -> {idx}")        
    # print("answer", answer)
        p_list = p_list[:-1]
    answer = [str(s) for s in answer]
    print(f"#{test_case} {' '.join(answer[::-1])}")
    