""" 21611 마법사 상어와 블리자드
<문제 설명>
- NxN의 격자 (r,c)는 r행 c열을 의미 -> arr[r][c]로 사용하면 된다. --> arr[y][x]와 동일..
- 격자의 가장 왼쪽 위는 (1,1)
- 격자의 가장 오른쪽 아래는 (N,N)
- 마법사 상어는 ((N+1)/2, (N+1)/2)에 위치
- 블리자드 마법을 주어진 횟수 M번 만큼 수행한 이후에 -> 1 x (폭발한 1번 구슬의 수) + 2 x (폭발한 2번 구슬의 수) + 3 x (폭발한 3번 구슬의 수)를 출력하여라.

<조건 설명>
1. 처음 상어가 있는 칸 외에는 구슬이 들어가고, 같은 번호를 가진 구슬이 "번호가" 연속하는 칸에 있으면 그 구슬을 연속하는 구슬이라고 한다.
2. 지정된 방향 d와 거리 s에 대해서 d 방향으로 s이하인 모든 칸에 있는 구슬을 모두 파괴한다.
3. 어떤 칸 A의 번호보다 번호가 작은 칸이 비었으면 A에 있던 구슬은 그 빈칸으로, 더이상 이동할 수 없을 때까지 반복한다. --> 여기서 회오리 모양으로 회전하는 것을 구현해야 함..
4. 구슬은 4개 이상 연속하는 구슬이 있을 때 폭발하고, 폭발한 이후에도 역시나 구슬이 이동을 하는데, 이때는 폭발하는 구슬이 없을 때까지 반복한다. --> 이렇게 폭발 시키는 것은 5번과정을 거친 후에도 구슬의 번호가 3이하를 유지해야 하기 때문이다.
5. 연속하는 구슬은 하나의 그룹이고, 각 그룹에서 구슬의 개수가 A, 구슬의 번호를 B로 두고 그룹의 순서대로 1번부터 A, B의 순서로 칸에 들어간다.

"""
import sys
import heapq

## 먼저 direction을 기록하는 배열을 만들어보자
## 아니면 각 구슬의 칸의 번호를 기록해 놓는 것도 좋을 것이다.

DX, DY = [0, 0, -1, 1], [-1, 1, 0, 0] ## 위, 아래, 왼, 오

input = sys.stdin.readline
N, M = map(int, input().split(' ')) ## 격자의 개수, 이동의 횟수
# to_shark = [[0 for _ in range(N)] for _ in range(N)] ## 상어가 있는 중앙으로 이동하기 위한 각 위치에서의 방향
from_shark = [[0 for _ in range(N)] for _ in range(N)] ## 상어가 있는 중앙으로부터 이동하기 위한 각 위치에서의 방향
number_board = [[0 for _ in range(N)] for _ in range(N)] ## 각 칸의 번호를 저장하는 board
def make_initial_direction():
    ## 미리 각 칸에서 이동해야 하는 방향을 저장해 둔다. 일종의 길 안내 지도라고 생각해도 될 것이다.
    global to_shark, from_shark
    ## (2, 1) -> (3, 0) -> (2, 1) -> (3, 0) -> ,,
    ## to_shark를 먼저 만들어 놓으면 from_shark는 그 위치의 정 반대로 이동하도록 하면 된다.
    cur_move = 1
    move_cnt = 0
    sx, sy = (N-1)//2, (N-1)//2
    # from_shark[sy][sx] = 2
    while move_cnt < N ** 2:
        if cur_move % 2 == 0: # (3, 0)
            for d in [3, 0]:
                # from_shark[sy][sx] = d
                for mv in range(cur_move):
                    # sx += DX[d];sy += DY[d];
                    if check_range(sx, sy) == False:
                        return
                    from_shark[sy][sx] = d
                    sx += DX[d];sy += DY[d];
                    # to_shark[sy][sx] = 2 if d == 3 else 1
                    number_board[sy][sx] = move_cnt + 1
                    move_cnt += 1
        else: # (2, 1)
            for d in [2, 1]:
                for mv in range(cur_move):
                    if check_range(sx, sy) == False:
                        return
                    from_shark[sy][sx] = d
                    sx += DX[d];sy += DY[d];
                    # to_shark[sy][sx] = 3 if d == 2 else 0
                    number_board[sy][sx] = move_cnt + 1
                    move_cnt += 1
        cur_move += 1

    print(from_shark)


board = []

answer = 0 ## 구슬이 폭발하는 4번 단계마다 각 번호별 폭발 개수를 트래킹한다.

for y in range(N):
    arr = list(map(int, input().split())) ## 구슬의 정보이다.
    board.append(arr)
board[(N-1)//2][(N-1)//2] = 4 #  상어임을 나타냄

def check_range(x, y):
    return 0 <= x < N and  0 <= y < N

def destroy(d, s):
    # 방향과 거리를 입력 받아서 d방향으로 s이하의 모든 구슬을 0으로 바꾸자.
    global DX, DY
    dx, dy = DX[d], DY[d]
    fx = fy = (N-1)//2

    # destroied = []
    for S in range(1, s+1):
        nx, ny = fx + dx, fy + dy
        if check_range(nx, ny):
            board[ny][nx] = 0 # 구슬 파괴
            # heapq.heappush(destroied, [number_board[ny][nx], nx, ny])
        fx, fy = nx, ny

def move():
    # 구슬을 제거한 다음에는 구슬이 더이상 이동할 수 없을 때까지 빈공간을 채우면서 이동한다.
    x, y = (N-1)//2, (N-1)//2
    while True:
        if check_range(x, y) == False:
            break

        if board[y][x] != 0:
            dir = from_shark[y][x]
            dx, dy = DX[dir], DY[dir]
            x, y = dx + x, dy + y
        else:
            blanks = []
            while board[y][x] == 0:
                heapq.heappush(blanks, [number_board[y][x], x, y])
                dir = from_shark[y][x]
                dx, dy = DX[dir], DY[dir]
                nx, ny = x + dx, y + dy
                # x, y = nx, ny
                if check_range(nx, ny) == False:
                    break
                else:
                    x, y = nx, ny

                # if check_range(nx, ny) and board[ny][nx] == 0:
                  #   heapq.heappush(blanks, [number_board[ny][nx], nx, ny])
#                    x, y = nx, ny
 #               else:
  #                  x, y = nx, ny
#                 break
            while blanks:
                _, bx, by = heapq.heappop(blanks)
                if check_range(x, y) == False:
                    break
                dir = from_shark[y][x]
                nx, ny = x + DX[dir], y + DY[dir]
                if check_range(nx, ny) and board[ny][nx] != 0:
                    board[by][bx] = board[ny][nx]
                    board[ny][nx] = 0
                    x, y = nx, ny
                else:
                    x, y = nx, ny
                    break



def explode():
    global answer
    ## 4개 이상으로 연속하는 구슬이 있을 때 발생한다.
    nx, ny = (N-1)//2, (N-1)//2
    prev_color = None
    group_n = 1
    did_explode = False
    groups = []

    to_explode = []
    while True:
        dir = from_shark[ny][nx]
        nx, ny = nx + DX[dir], ny + DY[dir]

        if check_range(nx, ny):
            if prev_color is None:
                to_explode.append([nx, ny])
                prev_color = board[ny][nx]
            else:
                if prev_color == board[ny][nx]:
                    to_explode.append([nx, ny])
                    group_n += 1
                else: ## 다른 색인 경우에는
                    if group_n >= 4: ##  폭발해야 하는 경우 -> 어차피 다시 움직여야 하기 때문에 그냥 groups 배열도 갱신을 하지 않는다.
                        did_explode = True
                        answer += prev_color * group_n
                        for (X, Y) in to_explode:
                            board[Y][X] = 0
                        to_explode = []
                        to_explode.append([nx, ny])


                    else: ## 폭발하지 않아도 되는 경우
                        A, B = group_n, prev_color
                        groups.append([A, B]) ## 이전 꺼를 넣어줌.
                        to_explode = []
                        to_explode.append([nx, ny])
                    prev_color = board[ny][nx]
                    group_n = 1
        else:
            if group_n >= 4:  ##  폭발해야 하는 경우 -> 어차피 다시 움직여야 하기 때문에 그냥 groups 배열도 갱신을 하지 않는다.
                did_explode = True
                answer += prev_color * group_n
                for (X, Y) in to_explode:
                    board[Y][X] = 0
                to_explode = []
                to_explode.append([nx, ny])

            else:  ## 폭발하지 않아도 되는 경우
                A, B = group_n, prev_color
                groups.append([A, B])  ## 이전 꺼를 넣어줌.
                to_explode = []
                to_explode.append([nx, ny])

            break

    return did_explode, groups


def update_board(groups):
    new_board = [[0 for _ in range(N)] for _ in range(N)]
    sx, sy = (N-1)//2, (N-1)//2
    new_board[sy][sx] = 4 ## 상어는 무조건 4로 저장한다.
    for group in groups:
        for i in range(2):
            dir = from_shark[sy][sx]
            nx, ny = sx + DX[dir], sy + DY[dir]
            if check_range(nx, ny) == False:
                return

            new_board[ny][nx] = group[i]
            sx, sy = nx, ny



make_initial_direction()
print(from_shark)
for m in range(M): ## 마법을 시전하는 횟수마다
    d, s = map(int, input().split(' '))
    d -= 1 ## 방향은 0부터 처리를 할 생각임
    destroy(d, s)
    print(board)
    move()
    print(board)
    while True:
        did_explode, groups = explode()

        if did_explode:
            move()
        else:
            update_board(groups)
            break
print(from_shark)
print(number_board)
print(answer)