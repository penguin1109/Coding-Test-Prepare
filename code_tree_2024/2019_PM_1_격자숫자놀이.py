import sys
input = sys.stdin.readline
import heapq
from collections import defaultdict
''' 
[출력] A[r][c]의 값이 k가 되기 위한 최소 시간을 출력하여라.
- 목표 숫자에 도달하는 것이 불가능하거나 100초를 초과하면 -1 출력

사각형이 안되면 가장 큰 길이를 기준으로 맞추고 나머지는 0으로 채워 주어야 함.
'''
# r번째 행, c번째 열 (r, c) = (y, x) #
r, c, k = map(int, input().strip().split(' ')) # 목표 위치, 목표 숫자 #
A = [list(map(int, input().strip().split(' '))) for _ in range(3)] # 3x3 배열 #

row, col = 3, 3 # 초기 행, 열의 길이 #

def play():
    global row, col, A
    if row >= col: # 각 행에 대해서 정렬 #
        new_col = col;
        new_A = []
        for y in range(row):
            temp = A[y]
            count_dict = defaultdict(int)
            for num in temp:
                if num!= 0:
                    count_dict[num] += 1
            q = []
            for key, value in count_dict.items():
                heapq.heappush(q, [value, key])
            new_col = max(new_col, len(q) * 2)
            cur = []
            while q:
                v, k = heapq.heappop(q)
                cur.extend([k, v])
            new_A.append(cur)
        col = new_col
        new_A = [arr + [0 for _ in range(new_col - len(arr))] for arr in new_A]
        A = new_A
        
    elif row < col: # 각 열에 대해서 정렬 #
        new_row = row;
        new_A = []
        for x in range(col):
            temp = [A[i][x] for i in range(row)]
            count_dict = defaultdict(int)
            for num in temp:
                if num != 0:
                    count_dict[num] += 1
            q = []
            for key, value in count_dict.items():
                heapq.heappush(q, [value, key])
            new_row = max(new_row, len(q) * 2)
            cur = []
            while q:
                v, k = heapq.heappop(q)
                cur.extend([k, v])
            new_A.append(cur)
        arr = [[0 for _ in range(col)] for _ in range(new_row)]
        for y in range(col):
            for x, n in enumerate(new_A[y]):
                arr[x][y] = n
        A = arr
        row = new_row
    else:
        A = A[:100, :100]
'''애당초 처음부터 (r, c)의 위치가 값이 k인 경우도 체크를 해 줘야 함.''' 
if r <= row and c <= col:
    if A[r-1][c-1] == k:
        print(0)
        exit(0) 
for time in range(1, 101):
    play()
    # print(A)
    
    # print(f"ROW : {row} COL : {col}")
    # if time == 5:
    #     exit(0)
    if r <= row and c <= col:
        # print(f"NUM : {A[r-1][c-1]}")
        if A[r-1][c-1] == k:
            print(time)
            exit(0)
print(-1)
            
        
                

