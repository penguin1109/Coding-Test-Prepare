def move(x, y, dir, board):
    """
    :return: boolean (if the ball gets in the hole or not)
            [x index, y index] (where the ball is newly located at)
    """
    global N, M, hole
    moved = 0
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]  ## 왼쪽 - 아래 - 오른쪽 - 위
    new_x, new_y = x, y
    while True:
        if (0 < new_x + dx[dir] < M) and (0 < new_y + dy[dir] < N):
            if board[new_y + dy[dir]][new_x + dx[dir]] == 'O':
                moved += 1
                return [new_x + dx[dir], new_y + dy[dir]], True, moved
            elif board[new_y +dy[dir]][new_x + dx[dir]] == '.':  ## 계속 동일 방향으로 이동이 가능하면
                new_x += dx[dir]
                new_y += dy[dir]
                moved += 1
            elif board[new_y +dy[dir]][new_x + dx[dir]] == '#':
                return [new_x, new_y], False, moved
        else:  ## 이동이 계속 불가능하면 새 좌표 return
            return [new_x, new_y], False, moved

    return [new_x, new_y], False, moved

def check(x, y):
    if (0 < x < M) and (0 < y < N):
        if board[x][y] == '#':
            return -1
        elif board[x][y] == 'O':
            return 0
        elif board[x][y] == '.':
            return 1



N, M = map(int, input().split(' ')) ## 세로, 가로
board = [[] for _ in range(N)]
red, blue, hole = [0,0],[0,0],[0,0]
for r in range(N):
    row = str(input())
    """ Bug Fix
    - 이 부분에서 빨간 구슬, 파란 구슬, 구멍의 위치를 각각 찾는데 같은 열에 있을 수도 있는데 if-else문을 잘못 사용해서
    각각의 위치가 반영이 되지 않은 경우가 있었다.
    """
    if 'R' in row:
        red[0] = row.index('R')
        red[1] = r
    if 'B' in row:
        blue[0] = row.index('B')
        blue[1] = r
    if 'O' in row:
        hole[0] = row.index('O')
        hole[1] = r

    row = row.replace('R', '.')
    row = row.replace('B', '.')
    board[r] = ' '.join(row).split(' ')

answer = 10**5
def simulate(red, blue, cnt):
    global answer
    if cnt > 10:
        return -1
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]  ## 왼쪽 - 아래 - 오른쪽 - 위

    for i in range(4):

        new_red, red_hole, red_moved = move(red[0], red[1],i, board)
        new_blue, blue_hole, blue_moved = move(blue[0], blue[1], i, board)
        if red_moved == 0 and blue_moved == 0:
            continue
        if red_hole == blue_hole == True:
            continue
        if new_red == new_blue: ## 동일하면 이동 불가능
            if red_moved > blue_moved:
                new_red[0] -= dx[i]
                new_red[1] -= dy[i]
            else:
                new_blue[0] -= dx[i]
                new_blue[1] -= dy[i]

        if red_hole == True: ## 빨간 구슬이 구멍에 들어갔다면
            answer = min(answer, cnt)
            return
        elif blue_hole == True: ## 파란 구슬이 구멍에 들어갔다면
            continue
        else: ## 계속 이어서 다른 방향으로 이동이 가능하면
            # print(new_red, new_blue)
            simulate(new_red, new_blue, cnt + 1)
# print(board)
simulate(red, blue,1)


if answer == 10**5:
    print(-1)
else:
    print(answer)



