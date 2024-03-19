import sys
import heapq
input = sys.stdin.readline
DX, DY = [-1,1,0,0], [0,0,-1,1]

'''[출력] 모든 학생이 탑승한 후의 최종 점수
최종 점수는 인접한 곳에 앉아있는 좋아하는 친구의 수로 결정이 됨'''
N = int(input().strip())
board = [[0 for _ in range(N)] for _ in range(N)]
like_dict = {} # 과연 각 학생의 선호도를 dictionary의 형태로 나타내는게 맞는 선택일까? #
student_order = []
for _ in range(N**2):
    a, b, c, d, e = map(int, input().strip().split(' '))
    like_dict[a] = [b, c, d, e]
    student_order.append(a)

def in_range(x, y):
    return 0 <= x < N and 0 <= y < N

def count_like_friend(idx, x, y):
    cnt = 0
    empty_cnt = 0
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy
        if in_range(nx, ny):
            if board[ny][nx] != 0:
                ppl = board[ny][nx]
                if ppl in like_dict[idx]:
                    cnt += 1
            else:
                empty_cnt += 1
    return cnt, empty_cnt

def find_best_seat(idx):
    seat = []
    global board
    for y in range(N):
        for x in range(N):
            if board[y][x] == 0:
                cnt, empty_cnt = count_like_friend(idx, x, y)
                heapq.heappush(seat, (-cnt, -empty_cnt, y, x))
    _, _, y, x = heapq.heappop(seat)
    board[y][x] = idx

def get_score():
    global answer
    for y in range(N):
        for x in range(N):
            n, _ = count_like_friend(board[y][x], x, y)
            if n > 0:
                answer += 10 ** (n-1)

        
for i in range(1, N**2+1):
    find_best_seat(idx=student_order[i-1])
# print(board)
answer = 0
get_score()
print(answer)