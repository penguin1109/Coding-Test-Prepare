""" 21608 - 상어 초등학교
<문제 설명>
- 교실을 NxN의 크기의 격자로 나타낸다.
- (r, c) = r행 c열 => 여기서 r은 y, c는 x이다.
- 두 좌표의 euclidian distance가 1인 경우에 두 칸이 인접하다고 한다. == 사방에 있는 좌표만 해당함

<조건>
1. 비어있는 칸 중 좋아하는 학생이 인접한 칸에 가장 많은 칸을 자리로 선정
    -> 이 조건에 의해서 사실상 처음에 선택되는 자리는 가운데임
2. 앞 조건을 만족하는 칸이 많으면 인접한 칸에 비어있는 칸이 제일 많은 자리를 선정
3. 앞 조건들을 만족하는 칸도 여러개이면 번호가 y값이 작은 행을 먼저(위에 있는 칸), 그러고도 남으면 x값이 작은 (왼쪽에 있는 칸)을 선택
4. 학생의 만족도는 자리배치가 **모두** 끝난 뒤에 그 학생과 인접한 칸에 앉은 좋아하는 학생의 수를 구해야 한다.

<풀이 방법>
- 우선 배치를 마음대로 하게 될텐데, 모든 경우에 대해서 학생들의 만족도의 총 합을 구해야 한다.
    - 대신 매 순간 최적의 선택을 (할 수 있나)?
<출력>
- 학생의 만족도의 총 합을 출력하여라.

"""
import heapq

N = int(input())
board = [[0 for _ in range(N)] for _ in range(N)] # 학생들의 자리를 저장해 줄 맵
seat_info = [[-1, -1] for _ in range(N**2+1)] # 학생의 번호별로 지정된 자리 정보를 저장해 줄 배열
visited = [False for _ in range(N**2+1)] # 학생들의 번호를 기반으로 자리가 배치 되었는지 확인해 주기 위한 check 배열

def nearby_empty(x, y):
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    cnt = 0
    for dx, dy in zip(DX, DY):
        nx, ny = x + dx, y + dy
        if (0 <= nx < N and 0 <= ny < N) and board[ny][nx] == 0:
            cnt += 1
    return cnt

def find_student(student_no):
    """학생의 번호를 바탕으로 학생의 좌표 전달 """
    for i in range(N):
        for j in range(N):
            if board[j][i] == student_no:
                return j, i # (y, x)


def nearby_best(student_order):
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    from collections import defaultdict
    student_info = besties[student_order]
    student_no = student_info[0]
    necessary_seats = defaultdict(int)


    for fav in student_info[1:]:
        if visited[fav] == True: # 좋아하는 학생의 자리 배치가 된 상태라면
            y, x = find_student(fav)
            for dx, dy in zip(DX, DY):
                nx, ny = x + dx, y + dy
                if (0<= nx <N and 0 <= ny <N) and board[ny][nx] == 0:
                    necessary_seats[(ny, nx)] += 1

    if len(necessary_seats) == 0: #
        seat_meta_info = init()
        nearby, y, x = heapq.heappop(seat_meta_info)
        return y, x

    seats = list(necessary_seats.keys())
    cnts = list(necessary_seats.values())

    check = []
    for seat, cnt in zip(seats, cnts):
        y, x = seat
        nearby = nearby_empty(x, y)
        heapq.heappush(check, (-cnt, -nearby,  y, x))

    cnt, nearby, y, x = heapq.heappop(check)
    # seat_meta_info.remove((nearby, y, x))

    return y, x






def calc_satisfaction():
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    satisfaction = 0
    for bestie in besties:
        temp = 0
        n, a, b, c, d = bestie
        y, x = seat_info[n]
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx,  y + dy
            if (0 <= nx <N and 0 <= ny <N):
                sn = board[ny][nx]
                if sn in bestie[1:]:
                    temp += 1
        if temp == 1:satisfaction += 1
        elif temp == 2:satisfaction += 10
        elif temp == 3:satisfaction += 100
        elif temp == 4:satisfaction += 1000

    return satisfaction

def init():
    seat_meta_info = []
    for x in range(N):
        for y in range(N):
            if board[y][x] == 0:
                nearby = nearby_empty(x, y) # 이웃에 비어 있는 자리의 수
                heapq.heappush(seat_meta_info, (-nearby, y, x))
    return seat_meta_info
def update(y, x, student_no):
    visited[student_no] = True
    board[y][x] = student_no
    seat_info[student_no] = [y, x]



besties = [] # 각 학생들이 좋아하는
for i in range(N**2): # 자리를 지정할 순서대로 입력이 되어 있음.
    arr = list(map(int, input().split(' '))) # 학생의 번호, 학생이 좋아하는 4명의 번호
    besties.append(arr)


for idx, student_info in enumerate(besties):
    n, a, b, c, d = student_info
    y, x = nearby_best(idx)
    update(y, x, n)

answer = calc_satisfaction()
print(answer)









