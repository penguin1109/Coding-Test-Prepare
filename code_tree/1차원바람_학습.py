import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

N, M, Q = map(int, readl().strip().split(' ')) # 세로 길이, 가로 길이, 바람이 불어온 횟수 #
board = [list(map(int, readl().strip().split(' '))) for _ in range(N)]
"""[출력] Q개의 바람을 거친 이후의 건물의 상태 (N줄 모두 출력)"""

def shift_left(arr):
    # print(arr)
    new = [0 for _ in range(len(arr))]
    for i in range(1, len(arr)):
        new[i-1] = arr[i]
    new[-1] = arr[0]
    # print(new)
    return new
def shift_right(arr):
    # print(arr)
    new = [0 for _ in range(len(arr))]
    for i in range(len(arr)-1):
        new[i+1] = arr[i]
    new[0] = arr[-1]
    # print(new)
    return new
def simulate(r, d):
    global board
    # r번째로부터 위, 아래로 내려가면서 한칸씩 shift를 해 주어야 한다. #
    # (1) 우선 주어진 행에 대해서 shifting 연산을 수행 #
    if d == 1:
        new_arr = shift_left(board[r])
    else:
        new_arr = shift_right(board[r])
    board[r] = new_arr
    # (2) 위로 전파 진행
    up_dir = (d+1)%2
    for up in range(r-1, -1, -1):
        do_shift = False
        for x in range(M):
            if board[up][x] == board[up+1][x]:
                do_shift = True
        if do_shift:
            new_arr = shift_left(board[up]) if up_dir == 1 else shift_right(board[up])
            board[up] = new_arr
            up_dir = (up_dir+1)%2
        else:
            break
    # (3) 아래로 전파 진행 #
    down_dir = (d+1)%2
    for down in range(r+1, N):
        do_shift = False
        for x in range(M):
            if board[down][x] == board[down-1][x]:
                do_shift = True
        if do_shift:
            new_arr = shift_left(board[down]) if down_dir == 1 else shift_right(board[down])
            board[down] = new_arr
            down_dir = (down_dir+1)%2
        else:
            break
for q in range(Q):
    r, d = map(str, readl().strip().split(' ')) # 바람의 영향을 받는 행 번호, 바람이 불어오는 방향 #
    d = 0 if d == 'L' else 1
    simulate(int(r)-1, d)

for y in range(N):
    board[y] = [str(x) for x in board[y]]
    print_str = ' '.join(board[y])
    print(print_str)