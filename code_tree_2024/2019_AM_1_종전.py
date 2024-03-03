import sys

MAX = sys.maxsize
input = sys.stdin.readline

N = int(input().strip())
board = [list(map(int, input().strip().split(' '))) for _ in range(N)]
border = [[False for _ in range(N)] for _ in range(N)]
total_sum = sum([sum(a) for a in board])
'''각 부족장이 관리하는 인구 수의 최댓값과 최솟값의 차이가 가장 적을 떄의 값을 계산하여라.
- 기울어진 직사각형 : 격자 내에 있는 한 지점으로부터 대각선으로 움직이며 반시계 순회를 할 때 지나온 지점들의 집합
- 5개의 부족이 땅을 나눠 갖기로 함.

[풀이방법] 풀이 방법이 이렇게 무식할줄 몰랐는데 정말로 오든 경우를 simulation으로 다 계산해서 확인해야 하는 문제였다. 이게 맞나..
'''

DX, DY = [1, -1, -1, 1], [-1, -1, 1, 1]

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def check_valid(x, y, k, l):
    return in_range(x+k, y-k) and in_range(x+k-l, y-k-l) and in_range(x-l, y-l)

def draw_border(x, y, k, l):
    global border
    move_nums = [k, l, k, l]
    border = [[False for _ in range(N)] for _ in range(N)]

    for dx, dy, move_num in zip(DX, DY, move_nums):
        for _ in range(move_num):
            x, y = x + dx, y + dy
            border[y][x] = True

def get_answer(x, y, k, l):
    draw_border(x, y, k, l)
    answer = [0 for _ in range(5)]
    ## 좌축 상단 ##
    for yy in range(y-l):
        for xx in range(x+k-l+1):
            if border[yy][xx]:
                break
            answer[0] += board[yy][xx]
    ## 우측 상단 ##
    for yy in range(y-k+1):
        for xx in range(N-1, x+k-l, -1):
            if border[yy][xx]:
                break
            answer[1] += board[yy][xx]
    ## 우측 하단 ##
    for yy in range(y-k+1, N, 1):
        for xx in range(N-1, x-1, -1):
            if border[yy][xx]:
                break
            answer[2] += board[yy][xx]
    ## 좌측 하단 ##
    for yy in range(y-l, N):
        for xx in range(x):
            if border[yy][xx]:
                break
            answer[3] += board[yy][xx]
    
    answer[4] = total_sum - sum(answer)
    return max(answer) - min(answer)

answer = MAX
for y in range(N):
    for x in range(N):
        for k in range(1, N):
            for l in range(1, N):
                if check_valid(x, y, k, l):
                    # print(x, y, k, l)
                    ret = get_answer(x, y, k, l)
                    answer = min(answer, ret)
print(answer)
            