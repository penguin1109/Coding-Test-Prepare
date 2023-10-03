"""
- 두 위치 사이의 거리는 euclidian distance로 계산이 됨
- 회사에서 출발하여 N명의 고객을 모두 방문하고 집으로 돌아오는 최단 경로를 찾고자 한다.
"""


T = int(input().strip()) # 테스트케이스의 수

def _calc_dist(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def _move(sx, sy, hx, hy, customer, visited, dist):
    global answer, N
    if sum(visited) == N:
        temp = dist + _calc_dist(sx, sy, hx, hy)
        answer = min(answer, temp)
        return
    
    for i in range(len(visited)):
        if visited[i] == 0:
            visited[i] = 1
            nx, ny = customer[i][0], customer[i][1]
            temp = dist + _calc_dist(sx, sy, nx, ny)
            if temp <= answer:
                _move(nx, ny, hx, hy, customer, visited, temp)
            visited[i] = 0
            
for t in range(T):
    N = int(input().strip()) # 고객의 수
    answer = float("INF")
    info = list(map(int, input().strip().split(' ')))
    cx, cy = info[0], info[1] # 회사의 좌표
    hx, hy = info[2], info[3] # 집의 좌표
    customer = [[info[i*2], info[i*2+1]] for i in range(2, 2+N)] # 고객의 좌표 
    visited = [0 for _ in range(N)]
    _move(cx, cy, hx, hy, customer, visited, 0)
    
    print(f"#{t+1} {answer}")
    
    
