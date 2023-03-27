N = int(input())
# 인구가 가장 많은 선거구와 가장 적은 선거구의 인구 차이의 최솟값을 출력하여라.
# 모든 경우를 다 시도해 보아야 한다.
total = 0
board = [[] for _ in range(N+1)]
for n in range(N):
    arr = list(map(int, input().split(' ')))
    total += sum(arr)
    board[n+1] = [0] + arr
def count_people(ly, lx, ry, rx):
    ii, jj = ly + ry - i, lx + rx - j
    flag = [[0 for _ in range(N)] for _ in range(N)]
    nums, length = ry-i+rx-j+1, j-lx+1
    for n in range(nums):
        if n%2 == 0:
            for m in range(length-1):
                flag[(i+1) + n // 2 + m][j+n//2-m] = 5
        else:
            for m in range(length):
                flag[i+n//2+m][j+n//2-m] = 5
    top, left, right, bottom = 0, 0, 0, 0
    for y in range(N):
        for x in range(N):
            if flag[y][x] != 5:
                if (0 <= y < ly and 0 <= x < j+1):
                    top += board[y][x]
                elif (0 <= y < ry+1 and j+1 <= x < N):
                    right += board[y][x]
                elif (ly <= y < N and 0 <= x < jj):
                    left += board[y][x]
                elif (ry + 1 <= y < N and jj <= x < N):
                    bottom += board[y][x]

    return max(top, right, bottom, left, total - (top + right + bottom + left)) - min(top, right, bottom, left, total - (top +right + bottom + left))

def check_point(left_y, left_x, right_y, right_x):
    global answer
    if (left_y < 0 or left_y >= N or left_x < 0 or left_x >= N or right_y < 0 or right_y >= N or right_x < 0 or right_x >= N or left_y +right_y - i >= N):
        return
    answer = min(answer, count_people(left_y, left_x, right_y, right_x))

    check_point(left_y + 1, left_x - 1, right_y, right_x)
    check_point(left_y, left_x, right_y + 1, right_x + 1)

def check(x, y, d1, d2):
    global answer, total
    lt, rt, lb, rb, mid = 0, 0, 0, 0, 0

    flag = [[0 for _ in range(N+1)] for _ in range(N+1)]
    for i in range(d1+1):
        flag[x+i][y-i] = 5
        flag[x + d2 + i][y + d2 - i] =5
    for i in range(d2+1):
        flag[x+i][y+i] = 5
        flag[x+d1+i][y-d1+i] = 5
    for i in range(x+1, x+d1+d2):
        isMid = False
        for j in range(1, N+1):
            if flag[i][j] == 5:
                isMid = not isMid
            if isMid:
                flag[i][j] = 5

    for i in range(1, N+1):
        for j in range(1, N+1):
            if (1 <= i <= y and 1 <= j < x + d1):
                if flag[j][i] != 5:lt += board[j][i]
            elif (y < i <= N  and 1 <=  j <= x + d2):
                if flag[j][i] != 5:rt += board[j][i]
            elif (x + d1 <= j <= N and 1 <= i < y-d1 + d2):
                if flag[j][i] != 5:lb += board[j][i]
            elif (x+d2 < j <= N and y-d1+d2 <= i <= N):
                if flag[j][i]!= 5:rb += board[j][i]
    mid = total - (lt + rt + lb + rb)
    return max(mid, lt, rt, lb, rb) - min(mid, lt, rt, lb, rb)



answer = 1e+9

for x in range(1, N+1):
    for y in range(1, N+1):
        for d1 in range(1, N+1):
            for d2 in range(1, N+1):
                if (1 <= x < x + d1 + d2 <= N and 1 <= y - d1 < y < y + d2 <= N):
                    answer = min(answer, check(x, y, d1, d2))
print(answer)
