D, DX, DY = ["d", "l", "r", "u"], [1,0,0,-1], [0,-1,1,0] # (x,y) -> (r,c) #
answer = ""
import heapq # priority queue #
from heapq import heappop, heappush

def l1_dist(r1,c1,r2,c2):
    return abs(r1-r2) + abs(c1-c2)

def in_range(x, y, r, c):
    if (1 <= x <= r and 1 <= y <= c):
        return True
    return False

def a_find(n,m,x,y,r,c,k):
    pq = [('', l1_dist(x,y,r,c), x, y)]
    while pq:
        temp_dir, _, r1, c1 = heappop(pq)
        if (r1 == r) and (c1 == c):
            if len(temp_dir) == k:
                return temp_dir
            if (k - len(temp_dir)) % 2:
                break
        for d, dx, dy in zip(D, DX, DY):
            nx, ny = r1 + dx, c1 + dy
            if in_range(nx, ny, n,m) == False:
                continue
            fn = len(temp_dir) + 1 + l1_dist(nx, ny, r, c)
            if fn > k:
                continue
            heappush(pq, (temp_dir + d, fn, nx, ny))
    return "impossible"
         
def solution(n, m, x, y, r, c, k):
    """
    (n,m) : 격자의 크기
    (x,y) : 출발 위치 
    (r,c) : 탈출 위치
    k : 탈출까지 이동해야 하는 거리
    """
    global answer
    # dfs(n,m,x,y,r,c,k, 0, [])
    # bfs(n,m,x,y,r,c,k)
    answer = a_find(n,m,x,y,r,c,k)
    return answer
    # if answer == "":
    #     return "impossible"
    
    # return answer

if __name__ == "__main__":
    cases = [
        [3,4,2,3,3,1,5],
        [2,2,1,1,2,2,2],
        [3,3,1,2,3,3,4]
    ]
    for case in cases:
        answer = solution(*case)
        print(answer)
        answer = ""
    # print("".join([]))
        