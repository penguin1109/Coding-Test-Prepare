import sys
sys.stdin = open("input.txt", "r")

import math
import heapq
T = int(input())
DY = [-1,-1,0,0,1,1]
DX = [-1,0,-1,1,0,1]

def get_idx(y, x):
    idx = ((y-1)*y) // 2
    idx += x
    return idx

def get_xy(n):
    diff = 1
    while n:
        temp = n - diff
        if temp > 0:
            diff += 1
            n = temp
        else:
            y = diff
            x = n 
            return y, x

# def bfs(tree, s, e):
def bfs(s, e):
    # ey, ex = tree[e-1]
    # sy, sx = tree[s-1]
    # print(ex, ey, sx, sy)
    ey, ex = get_xy(e)
    sy, sx = get_xy(s)
    print(ex, ey, sx, sy)
    q = [[0, sy, sx]]
    visited = [False for _ in range(e+1)]
    visited[s] = True
    while q:
        cnt, y, x = heapq.heappop(q)
        if y == ey and x == ex:
            return cnt
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if nx <= 0 or ny <= 0:
                continue
            if nx > ny:
                continue
            if ny > ey:
                continue
            idx = get_idx(ny, nx)
            if idx > e:
                continue
            
            if visited[idx] == False:
                visited[idx] = True
                heapq.heappush(q, [cnt+1, ny, nx])


    
def get_max_height(n):
    for i in range(n+1):
        num = (i*(i+1)) // 2
        if n <= num:
            return i

def min_dist(s, e):
    ey, ex = get_xy(e)
    sy, sx = get_xy(s)
    print("End : ", ey, ex)
    print("Start : ", sy, sx)
    mv_y = ey - sy
    
    if (ex == sx):
        return mv_y
    
    elif (ex > sx):
        diff_x = ex - sx
        if (diff_x > mv_y):
            return diff_x
        else:
            return mv_y
        
    else:
        diff_x = sx - ex
        return mv_y + diff_x
    
for test_case in range(1, T+1):
    s, e = map(int, input().strip().split(' '))
    if s > e:
        temp = s
        s = e
        e = temp
    # print(f"Start : {s} End : {e}")
    # (1) tree 구조로 블럭 번호에 맞춰서 쌓아주기 #
    tree = []
    y, x = 1, 1
    # max_height = int(math.sqrt(e)) + 1
    # max_height = get_max_height(e)
    # print("max height ", max_height)
    # for height in range(1, max_height+1):
    #     for row in range(1, height+1):
    #         tree.append([height, row])
    # print(tree)
    # (2) bfs를 사용해서 최단 거리 찾아주기 #
    # answer = bfs(tree, s, e)
    # answer = bfs(s, e)
    answer = min_dist(s, e)
    print(f"#{test_case} {answer}")

