import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N, M = map(int, readl().strip().split(' '))
board = [int(readl().strip()) for _ in range(N)] # 위에서부터 아래로 폭탄의 숫자 #

def gravity(arr):
    new_arr = [0 for _ in range(N)];temp = []
    cnt = 0
    for idx,a  in enumerate(arr):
        if a != 0:
            cnt += 1
            temp.append(a)
    new_arr[N-cnt:] = temp
    return new_arr, cnt
def find_and_explode():
    global board
    for i in range(N):
        if board[i] != 0:
            start = i
            break
    prev = board[start]
    cnt = 0;found = False

    for i in range(start,N):
        if prev == board[i]:
            cnt += 1
        else:
            if cnt >= M:
                found = True
                for j in range(i-1, -1, -1): # 위에서부터 밑으로 #
                    if board[j] == prev:
                        board[j] = 0
                    else:
                        break
            prev = board[i]
            cnt = 1 # 다시 초기 변수값으로 바꿈 #
        if i == N-1:
            if cnt >= M:
                found = True
                for j in range(i, -1, -1): # 위에서부터 밑으로 #
                    if board[j] == prev:
                        board[j] = 0
                    else:
                        break
    print(board)
    board, cnt = gravity(board)
    print(board)
    return cnt, found


while True:
    cnt, found = find_and_explode()
    if found == False or cnt == 0:
        break


if cnt == 0:
    print(0)
else:
    print(cnt)
    for i in range(N):
        if board[i] != 0:
            print(board[i])
