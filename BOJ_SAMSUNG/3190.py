import sys
N = int(input())
board = [[0]* N for _ in range(N)]
K = int(input())
""" 뱀
1. 처음에 뱀은 맨 위 좌측에 위치하고 길이는 1이다. (0,0)에 위치
2. 뱀은 처음에는 오른쪽을 향한다.
3. 뱀은 몸 길이를 늘려 머리를 다음 칸에 위치 시키고 이동한 칸에 사과가 있다면 그 칸에 있던 사과는 없어지고 꼬리는 움직이지 않는다.
4. 이동한 칸에 사과가 없다면 몸 길이가 줄어서 꼬리가 줄고 머리 부분만 늘어난다.
5. 뱀이 벽 또는 자기 자신과 부딪히면 게임이 끝난다.
"""
## 아래 - 오 - 위 - 왼
dx, dy = [0,1,0,-1],[1,0,-1,0]
import heapq
from heapq import heappush, heappop
for _ in range(K):
    x, y = map(int, input().split(' ')) ## 행, 열
    board[x-1][y-1] = 1 ## 사과가 존재하는 위치임을 나타내어줌


L = int(input())
from collections import deque
queue = deque()

for _ in range(L): ## 뱀의 방향 전환 정보
    X, C = input().split(' ') ## C가 D이면 왼쪽, L이면 오른쪽으로 90도 회전
    X = int(X) ## X초 이후부터 방향을 바꾸어야 한다.
    # heapq.heappush(queue, (X, C))
    queue.append((X, C))


def change_dir(cur_dir, rotate):
    if rotate == 'L': ## 왼쪽으로 90도
        cur_dir = (cur_dir - 1)  % 4
    else: ## 오른쪽으로 90도
        cur_dir = (cur_dir + 1) % 4
    return cur_dir
cnt = 0
head = (0,0);tail = (0,0); ## 머리와 꼬리의 위치 좌표를 각각 나타냄
cur_dir = 0 ## 우선 처음 방향은 오른쪽
snake = []
game_end = False
snake.append(tail)
while True:
    cnt += 1
    valid = True


    new_head_x = head[0] + dx[cur_dir]
    new_head_y = head[1] + dy[cur_dir]

    if (0 <= new_head_x < N) and (0 <= new_head_y < N):
        head = (new_head_x, new_head_y)
        if head not in snake:
            snake.append(head)

            if board[new_head_x][new_head_y] != 1: ## 사과가 해당 위치에 없다면
                board[new_head_x][new_head_y] = 2
                snake.remove(tail) ## 꼬리 좌표를 제거해 주어야 함
                tail = snake[0] ## 현재 꼬리 업데이트
            else: ## 사과를 먹었다면 사과를 없애 주어야 한다.
                board[new_head_x][new_head_y] = 0
        else: ## 자기 자신과 부딪힌 경우
            valid = False
            break
    else: ## 벽에 부딪힌 경우
        valid = False
        break
    ## 해당 시간에 이동해야 할 것을 모두 이동했어야 함
    if len(queue) > 0 and cnt == queue[0][0]:  ## 시간이 되었으면, 즉 이동한 후에 방향 변경
        cur_dir = change_dir(cur_dir, queue[0][1])  ## 방향 변경
        queue.popleft()
print(cnt)












