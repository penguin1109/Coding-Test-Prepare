N = int(input())
"""
1. 제일 마지막의 점을 기준으로 나머지 획들을 시계 방향으로 90도를 회전 시켜야 하는 상황이다.
2. 원래 직선과 수직인 점을 찾으면 된다.
"""
def check_square(board):
    cnt = 0
    mover = ((1, 0), (0,1), (-1,0), (0,-1))
    for x in range(100):
        for y in range(100):
            valid = False
            x_, y_ = x, y
            if board[y][x] == 1:
                #print(x,y)
                valid = True
                for j in range(4):
                    if board[y_ + mover[j][1]][x_ + mover[j][0]] != 1:
                        valid = False
                        break
                    else:
                        x_ += mover[j][0]
                        y_ += mover[j][1]
            if valid:
                #print(x, y)
                cnt += 1
    return cnt


def rotate_90(cx, cy, tx, ty):
    """
    :param board:
    :param cx: Center x
    :param cy: Center y
    :param tx: Target x
    :param ty: Target y
    :return: The x, y point value of the clock-wise rotated target point
    """
    diff_h = (cy-ty)
    diff_w = (cx-tx)
    if (diff_h > 0) and (diff_w > 0):
        new_x = cx + abs(diff_h)
        new_y = cy - abs(diff_w)
    elif (diff_h > 0) and (diff_w < 0):
        new_x = cx + abs(diff_h)
        new_y = cy + abs(diff_w)
    elif (diff_h < 0) and (diff_w < 0):
        new_x = cx - abs(diff_h)
        new_y = cy + abs(diff_w)
    elif (diff_h < 0) and (diff_w > 0):
        new_x = cx - abs(diff_h)
        new_y = cy - abs(diff_w)
    elif (diff_h == 0):
        new_y = cy - diff_w
        new_x = cx
    elif (diff_w == 0):
        new_x = cx + diff_h
        new_y = cy
    return new_x, new_y

mover = ((1,0), (0,-1), (-1,0), (0,1))
board = [[0]*101 for _ in range(101)]
def dist(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2

for _ in range(N):
    x, y, d, g = map(int, input().split(' ')) ## 시작 x좌표, 시작 y좌표, 시작 방향, 세대
    points = [(x, y)]
    last_x, last_y = x + mover[d][0], y + mover[d][1]
    if g == 0:
        points.append((last_x, last_y))
    for order in range(g):
        new_points = []
        for idx, p in enumerate(points):
            if last_x == p[0] and last_y == p[1]:
                continue
            #print(last_x, last_y, p[0], p[1])
            new_x, new_y = rotate_90(last_x, last_y, p[0], p[1])
            #print(last_x, last_y, p[0], p[1],new_x, new_y)
            if idx != len(points)-1:
                new_points.append((new_x, new_y))
            else:
                new_points.append((new_x, new_y))
                new_points.append((last_x, last_y))

        #print(new_points)
        #print(points)

        last_x, last_y = rotate_90(last_x, last_y, x,y)
        points += new_points
    for p in points:
        board[p[1]][p[0]] = 1

print(check_square(board))








