import sys
input = sys.stdin.readline
import copy
'''
- 반지름이 1,2,..,n으로 차례로 커지는 원판으로 게임판을 만들어줌
[출력] 인접한 위치의 숫자가 같으면 지우고, 지웠을 때 남는 수의 총 합
지워지는 수가 없으면 정규화한 수의 총합 (평군보다 크면 -1, 평귬보다 작으면 +1)
'''
N, M, Q = map(int, input().strip().split(' ')) # 원판의 개수, 숫자의 개수, 회전 횟수 #
board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 각 원판마다 M개의 숫자들을 알려줌 #

def normalize(arr, mean):
    for n in range(N):
        for m in range(M):
            if arr[n][m] == 0:
                continue
            if arr[n][m] < mean:
                arr[n][m] += 1
            elif arr[n][m] > mean:
                arr[n][m] -= 1
    return arr

def check_same(board):
    # erased = copy.deepcopy(board)
    erased = [[False for _ in range(M)] for _ in range(N)]
    did_erase = False
    for n in range(N):
        for m in range(M):
            target = board[n][m]
            if target == 0:
                continue
            if target == board[n][m-1]:
                erased[n][m-1] = True;erased[n][m] = True;did_erase = True
            next = m + 1 if m != M-1 else 0
            if target == board[n][next]:
                erased[n][next] = True;erased[n][m] = True;did_erase=True
            if n < N-1:
                if target == board[n+1][m]:
                    erased[n+1][m] = True;erased[n][m] = True;did_erase=True
            if n > 0:
                if target == board[n-1][m]:
                    erased[n-1][m] = True;erased[n][m] = True;did_erase = True
    for n in range(N):
        for m in range(M):
            if erased[n][m] == True:
                board[n][m] = 0
    # return erased, did_erase
    return board, did_erase
                
def spin_clock(x, k):
    global board
    k = (M-k) % M
    for i in range(x, N+1, x):
        # print(f"X : {x} Idx : {i}")
        temp = board[i-1] # 현재 돌려야 하는 원판 #
        # top = temp[:M-k]
        top = temp[:k]
        # print(f"temp : {temp}   top : {top}")
        # del temp[:M-k]
        del temp[:k]
        temp.extend(top)
        board[i-1] = temp
    return board

def spin_anti_clock(x, k):
    k %= M
    global board
    for i in range(x, N+1, x):
        # print(f"X : {x} Idx : {i}")
        temp = board[i-1]
        top = temp[:k]
        del temp[:k]
        temp.extend(top)
        board[i-1] = temp
    return board

for q in range(Q):
    x, d, k = map(int, input().strip().split(' '))
    if d == 0: # 시계 방향 #
        board = spin_clock(x, k)
    else:
        board = spin_anti_clock(x, k)
    # print(board)
    board, did_erase = check_same(board)
    '''매번 회전 할 때마다 지워지는 숫자가 있는지 확인을 해 주어야 했음.'''
    if did_erase == False:
        total_sum = [board[n][m] for n in range(N) for m in range(M) if board[n][m] != 0]
        total_mean = sum(total_sum) // len(total_sum)
        board = normalize(board, total_mean)

answer = sum([board[n][m] for n in range(N) for m in range(M) if board[n][m] != 0])
print(answer)
# erased, did_erase = check_same(board)
# print(erased)
# # print(did_erase)
# if did_erase == False:
#     total_sum = sum([sum(a) for a in board])
#     board = normalize(board, int(total_sum / (N*M)))
#     total_sum = sum([sum(a) for a in board])
#     print(total_sum)
# else:
#     total_sum = sum([sum(a) for a in erased])
#     print(total_sum)

    