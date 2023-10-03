import sys
N = int(input())
board = []
for _ in range(N):
    board.append(list(map(int, input().split(' '))))

answer = 0 ## 최대 5번 이동을 한 뒤에 제일 큰 보드의 값
def DFS(dir, board, cnt):
    global answer
    new = []
    if dir == 0 or dir == 1:
        board = list(map(list, zip(*board)))
    for i in range(len(board)):
        row = board[i]
        not_zero = [tile for tile in row if tile != 0]
        if dir == 0 or dir == 3:
            for i in range(1, len(not_zero)):
                if not_zero[i] == not_zero[i-1]:
                    not_zero[i-1] *= 2
                    not_zero[i] = 0
            not_zero =  [tile for tile in not_zero if tile != 0]
            for i in range(len(row) - len(not_zero)):
                not_zero.append(0)
        elif dir == 1 or dir == 2:
            for i in range(len(not_zero)-1, 0, -1):
                if not_zero[i] == not_zero[i-1]:
                    not_zero[i] *= 2
                    not_zero[i-1] = 0
            not_zero = [tile for tile in not_zero if tile != 0]
            not_zero = not_zero[::-1]
            for i in range(len(row) - len(not_zero)):
                not_zero.append(0) ## 원래 row만큼의 길이가 되도록 0을 추가
            not_zero = not_zero[::-1]
        new.append(not_zero)

    if dir == 0 or dir == 1: ## 이런 식으로 4방향으로 이동을,
        new = list(map(list, zip(*new)))
    if cnt == 5:
        answer = max(answer, max(sum(new, [])))
        return
    for k in range(4):
        DFS(k, new, cnt + 1)
for i in range(4):
    DFS(i, board, 1)
print(answer)

