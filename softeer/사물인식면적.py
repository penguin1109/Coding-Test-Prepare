""" 문제 설명
<문제 조건>
- 레이더를 통해 인식된 정보의 입력값은 평면에 N개의 점으로 주어짐
- 각각의 점은 총 K개의 색 중 하나를 가지며, 1~K중의 한 정수로 표현.
- 각 색을 가지는 점들을 적어도 하나씩 포함하면서 가장 넓이가 작은 사물의 넓이를 출력
- 직사각형의 가로 | 세로가 0이 되어서 선분이나 점으로 나타는 경우의 넓이는 0
- 사물로 인식이 되기 위해서는 당연히 직사각형의 4변이 모두 수평/수직 이어야 함

"""
from collections import defaultdict
N, K = map(int, input().split(' '))

def one_side_dist(a, b):
    # 가로, 세로 한 쪽에 대한 좌표가 주어졌을때 거리 return
    return a - b if a > b else b - a

def check_size(points):
    X = sorted([p[0] for p in points])
    Y = sorted([p[1] for p in points])
    mx, Mx = X[0], X[-1]
    my, My = Y[0], Y[-1]
    row, col = one_side_dist(mx, Mx), one_side_dist(my, My)
    return row * col
    
point_dict = defaultdict(list)
for _ in range(N):
    x, y, c = map(int, input().split(' ')) # (x,y) coordinate, color information
    point_dict[c].append((x, y))


min_size = float('inf') # 무한대의 수로 먼저 정답을 초기화

def backtrack(color:int, mx, my, Mx, My):#, points:list):
    global min_size
    size = (Mx-mx) * (My-my)
    if size >= min_size:
        return
    
    if color == K+1:
        if size < min_size:
            min_size = size
    else:
        hubo_points = point_dict[color]
        for p in hubo_points:
            x, y = p
            backtrack(color+1, min(mx, x), min(my, y), max(x, Mx), max(My, y))

# backtrack(1, [])
backtrack(1, 1000, 1000, -1000, -1000)
print(min_size)
            