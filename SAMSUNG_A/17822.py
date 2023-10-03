""" 17822 - 원판 돌리기
<문제 설명>
- 반지름이 1, 2, .. N인 원찬이 크기가 작아지는 순으로 바닥에 있고, 원판의 중심은 모두 같다.
- 반지름이 i이면 i번째 원판이라고 할 수 있다.

1. 원판 initialize
    - (i,1)은 (i,2), (i, M)과 인접
    - (i,M)은 (i,M-1), (i,1)과 인접
    - (i,j)는 (i,j-1), (i,j+1)과 인접
    - (1,j)는 (2,j)와 인접  => 이건 첫번째, 두번째 원판에서 j번째 수만 인접하다는 뜻이다.
    - (N,j)는 (N-1,j)와 인접
    - (i,j)는 (i-1,j), (i+1,j)와 인접

2. 원판 rotate
    - 번호가 x(i)의 배수인 원판을 d(i) 방향으로 k(i)칸 회전시킨다. d(i) = 0이면 시계, 1이면 반시계
    - 원판에 수가 남아 있으면 인접하면서 같은 수를 모두 찾는다.
        - 그런 수가 있으면 원판에 인접하면서 같은 수를 모두 지운다.
        - 없으면 원판에 적힌 수의 평균을 구하고, 평균보다 큰 수는 -1, 작은 수는 +1

<출력>
원판을 T번 회전 시킨 후 원판에 적힌 수의 합을 구하여라.

"""

from collections import deque
N, M, T = map(int, input().split(' ')) # 원판의 개수, 원판에 적힌 정수의 개수, 회전 횟수

board = [list(map(int, input().split(' '))) for _ in range(N)] # 원판에 적힌 수 # (i,j)는 반지름이 i인 원판의 j번째 수이다.

class Rotater(object):
    def __init__(self, board, M):
        super(Rotater, self).__init__()
        self.board = board
        self.M = M
        self.N = len(self.board)
        self.zeros = 0
        self.removed = [[False for _ in range(M)] for _ in range(self.N)]
        self.sum = sum([sum(a) for  a in board])

    def rotate(self, x, d, k):
        if d == 0:
            self.clockwise(x, k)
        elif d == 1:
            self.anti_clockwise(x, k)
        else:
            raise UserWarning
    def anti_clockwise(self, x, k):
        board = self.board
        removed = self.removed
        for n in range(x, self.N+1, x):
            q = deque(board[n-1])
            p = deque(removed[n-1])
            for _ in range(k):
                a = q.popleft();b = p.popleft()
                q.append(a);p.append(b)
            board[n-1] = list(q)
            removed[n-1] = list(p)
        self.board = board
        self.removed = removed


    def clockwise(self, x, k):
        board = self.board
        removed = self.removed
        for n in range(x, self.N+1, x):
            q = board[n-1];p=removed[n-1]
            for _ in range(k):
                a = q.pop();b=p.pop()
                q.insert(0, a);p.insert(0, b)
            board[n-1] = q
            removed[n-1] = p
        self.board = board
        self.removed = removed

    def delete(self):
        N, M = self.N, self.M
        board = self.board

        erased = False
        arr = []
        ## 인접한 수를 BFS를 사용하여 탐색했어야 했다.
        for i in range(N):
            for j in range(M):
                if board[i][j] == 0:
                    continue
                q = deque([[board[i][j], i, j]])
                val = board[i][j]
                while q:
                    val, x, y = q.popleft()

                    for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                        nx, ny = x+dx, y + dy #   (y + dy) % M
                        if ny == M:
                            ny = 0
                        elif ny == -1:
                            ny = M-1
                        if 0 <= nx < N and 0 <= ny < M:
                            if board[nx][ny] > 0 and board[nx][ny] == val:
                                erased = True
                                board[nx][ny] = 0
                                board[x][y] = 0
                                q.append([val, nx, ny])
        cnt = 0
        for i in range(N):
            for j in range(M):
                if board[i][j] != 0:
                    cnt += 1
        if erased == False:
            # avg = sum([sum(a) for a in board]) / (M*M - self.zeros)
            avg = sum([sum(a) for a in board]) / cnt if cnt != 0 else 0
            # avg = self.sum / (M*M - self.zeros)
            # print(f"AVG : {avg}")
            for i in range(N):
                for j in range(M):
                    if board[i][j] < avg and board[i][j] > 0:
                        board[i][j] += 1
                    elif board[i][j] > avg:
                        board[i][j] -= 1 ## 이부분에서 제거된 숫자와 빼서 0이 된 숫자를 구분하지 못해서 9%에서 틀렸었던 것으로 확인이 된다.

        self.board = board

rotater = Rotater(board, M)
for t in range(T):
    x, d, k = map(int, input().split(' '))
    rotater.rotate(x, d, k)
    # print(rotater.board)
    rotater.delete()
    # print(rotater.board)
    # print(rotater.removed)

answer = sum([sum(a) for a in rotater.board])
print(answer)



