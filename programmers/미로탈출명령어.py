D, DX, DY = ["d", "l", "r", "u"], [1,0,0,-1], [0,-1,1,0] # (x,y) -> (r,c) #
answer = ""
import copy
import sys
sys.setrecursionlimit(10 ** 7)

def check_range(n, m, r, c):
    if (0 < r <= n and 0 < c <= m):
        return True
    return False

def l1_dist(r1,c1,r2,c2):
    return abs(r1-r2) + abs(c1-c2)

def dfs(n, m, r1,c1, r, c, k, dist, move):
    global answer, D, DX, DY
    if answer != "":
        return
    left_dist = l1_dist(r1,c1,r,c)
    if left_dist + dist > k:
        return
    if dist == k:
        if r1==r and c1==c:
            answer = "".join(move)
            # print("answer ", answer)
            # print("".join(move))
        return
    for d, dx, dy in zip(D, DX, DY):
        nr, nc = r1 + dx, c1 + dy
        if check_range(n,m,nr,nc) == True:
            temp = copy.deepcopy(move)
            temp.append(d)
            # print("temp ", temp)
            dfs(n,m,nr,nc,r,c,k, dist+1, temp)
        
def bfs(n,m,r1,c1,r,c,k):
    # import queue
    from collections import deque
    global answer
    # q = queue.Queue([[r1,c1,""]])
    q = deque([[r1,c1,""]])
    answers = []
    while q:
        temp_r, temp_c, temp_move = q.popleft()
        # print("temp ", temp_move)
        if len(temp_move) == k:
            if temp_r == r and temp_c == c:
                answers.append(temp_move)
            continue
        for d, dx, dy in zip(D, DX, DY):
            nx, ny = temp_r + dx, temp_c + dy
            if check_range(n,m,nx,ny) == True:
                q.append([nx, ny, temp_move + d])
    answer = sorted(answers)[0] if len(answers) > 0 else ""
    return
         
def solution(n, m, x, y, r, c, k):
    """
    (n,m) : 격자의 크기
    (x,y) : 출발 위치 
    (r,c) : 탈출 위치
    k : 탈출까지 이동해야 하는 거리
    """
    global answer
    # dfs(n,m,x,y,r,c,k, 0, [])
    bfs(n,m,x,y,r,c,k)
    if answer == "":
        return "impossible"
    
    return answer

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
        