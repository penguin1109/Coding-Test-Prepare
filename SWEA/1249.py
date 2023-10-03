```
- 분명히 문제 카테고리는 <heap>으로 구분이 되어있었지만, <heap>을 사용해야 하는 필요성은 없어 보였다.
- 결국에는 <출발점에서 도착점까지 가는 값>을 구하는 문제였기 때문에 순차적으로 출발점에서부터의 거리를 구해야 한다. 
  - 당연히 생각한 것은 BFS를 사용해서 현 지점에서 4방으로의 위치에 맞는 곳으로 이동하는 방법이었는데, 모든 경우을 다 시도하는 것은 너무 오래걸릴 것이라고 생각했다.
  - 근데 결과적으로 출발점이 정해져 있는 상황이기 때문에 <다익스트라 알고리즘>을 떠올렸다.
  - 그래서 queue에 출발점부터 넣고 dist_arr의 출발점에서 각 지점까지의 거리를 저장하는 배열을 만든다. 이렇게 하고 dist_arr[nx][ny] > dist[x][y] + cost[nx][ny]이면 업데이트 하고 queue에 (nx, ny)를 넣는다. 
```
if __name__ == "__main__":
  from collections import deque
  T = int(input())
  INF = float(10 ** 9)
  for test_case in range(T):
    N = int(input())
    board = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
      temp = input()
      for j in range(N):
        board[i][j] = int(temp[j])
    
    dx, dy = [-1,1,0,0], [0,0,-1,1]
    dist_arr = [[INF for _ in range(N)] for _ in range(N)]
    dist_arr[0][0] = 0
    q = deque([(0,0)])
    while (q):
      curr = q.popleft()
      for dir in range(4):
        nx = curr[0] + dx[dir]
        ny = curr[1] + dy[dir]
        if (0 <= nx < N and 0 <= ny < N):
          new_dir = dist_arr[curr[1]][curr[0]] + board[ny][nx]
          if (new_dir < dist_arr[ny][nx]):
            dist_arr[ny][nx] = new_dir
            q.append((nx, ny))
    answer = dist_arr[N-1][N-1]
    print(f"#{test_case+1} {answer}")




