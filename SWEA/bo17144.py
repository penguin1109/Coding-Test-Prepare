import sys, copy
#input = sys.stdin.readline

dx, dy = [-1, 1, 0, 0], [0, 0, -1, 1]

def expand(board, R, C):
  new_board = [[0 for _ in range(C)] for _ in range(R)]
  #print(new_board)
  for r in range(R):
    for c in range(C):
      if board[r][c] == -1 or board[r][c] == 0:
        continue
      cur_x, cur_y = c, r
      cnt = 0
      for dir in range(4):
        nx, ny = cur_x + dx[dir], cur_y + dy[dir]
        if (0 <= nx < C and 0 <= ny < R):
          if board[ny][nx] == -1: ## 공기 청정기가 있으면 확산 불가능
            continue
          new_board[ny][nx] += board[r][c] // 5
          #new_board[ny][nx] = max(0, new_board[ny][nx])
          cnt += 1
      new_board[r][c] -= (board[r][c] // 5) * cnt
      #new_board[r][c] = max(0, new_board[r][c])

  for r in range(R):
    for c in range(C):
        new_board[r][c] += board[r][c]
  return new_board
  

def clean(board, R, C, cleaner):
  top,bot = cleaner-1, cleaner
  ## 말 그대로 밀어버린다는 것은 0으로 바꾸는게 아니라 미세먼지의 위치를 해당 방향으로 shift 해 주는 것이었다.
  new_board = copy.deepcopy(board)
  new_board[top][1] = 0
  new_board[bot][1] = 0

  for c in range(1, C-1):
    new_board[top][c+1] = board[top][c]
    new_board[bot][c+1] = board[bot][c]
  for c in range(C-1, 0, -1):
    new_board[0][c-1] = board[0][c]
    new_board[-1][c-1] = board[-1][c]
  for r in range(top, 0, -1):
    new_board[r-1][-1] = board[r][-1]
  for r in range(bot, R-1):
    new_board[r+1][-1] = board[r][-1]
  for r in range(top-1):
    new_board[r+1][0] = board[r][0]
  for r in range(R-1, bot+1, -1):
    new_board[r-1][0] = board[r][0]
  
  
  return new_board




if __name__ == "__main__":
  R, C, T = map(int, input().split(' '))

  board = [[] for _ in range(R)]
  cleaner = -1
  for r in range(R):
    board[r] = list(map(int, input().split(' ')))
    if board[r][0] == -1:
      cleaner = max(cleaner, r)
  for t in range(T):
    board = expand(board, R, C)
    board = clean(board, R, C, cleaner)
  for b in board:
    print(b)
  answer = [sum(b) for b in board]
  answer = sum(answer) + 2
  print(answer)
  
