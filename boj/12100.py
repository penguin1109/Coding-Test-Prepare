""" 2048 (Easy)
- NxN 크기의 보드.
- 전체 블록을 상하좌우 4 방향 중 하나로 이동시킴
- 같은 값을 갖는 두 블록이 충돌하면 두 블록은 하나로 합쳐지고, 한번 이동에서 이미 합쳐진 블록은 다른 블록과 합칠 수 없다.

[문제]: 최대 5번을 이동시켜서 얻을 수 있는 가장 큰 블록
"""

N = int(input().strip()) # 보드의 크기

board = [list(map(int, input().strip().split(' '))) for _ in range(N)] # 초기 보드의 상태

def move_left(board):
    # x축은 -1, y축은 그대로
    # 왼쪽부터 stack에 쌓아줌
    global N
    ret_board = []
    for n in range(N):
        arr = board[n]
        temp = []
        for i in arr:
            if i != 0:
                temp.append(i)
        added = []
        i = 0
        while (i < len(temp)):
            if i == len(temp)-1:
                added.append(temp[i])
                i += 1
                break
            left, right = i, i + 1
            if temp[left] == temp[right]:
                added.append(temp[left] * 2)
                i = right + 1
            else:
                added.append(temp[i])
                i += 1
        added.extend([0 for _ in range(N - len(added))])
        ret_board.append(added)
    return ret_board

def move_right(board):
    # x축은 +1, y축은 그대로
    # 왼쪽부터 stack에 쌓아줌
    global N
    ret_board = []
    for n in range(N):
        arr = board[n]
        temp = []
        for i in arr:
            if i != 0:
                temp.append(i)
        
        added = []
        i = len(temp)-1
        while (i >= 0):
            if i == 0:
                added.append(temp[i])
                break
            left, right = i-1, i
            if temp[left] == temp[right]:
                added.append(temp[left] * 2)
                i = left - 1
            else:
                added.append(temp[i])
                i -= 1
        added = added[::-1]
        temp = [0 for _ in range(N-len(added))]
        temp.extend(added)
        ret_board.append(temp)
    return ret_board

def move_up(board):
    global N
    reverse_board = [[board[i][j] for i in range(N)] for j in range(N)]
    reverse_board = move_left(reverse_board)
    ret_board = [[reverse_board[i][j] for i in range(N)] for j in range(N)]
    return ret_board

def move_down(board):
    global N
    reverse_board = [[board[i][j] for i in range(N)] for j in range(N)]
    reverse_board = move_right(reverse_board)
    # print(reverse_board)
    ret_board = [[reverse_board[i][j] for i in range(N)] for j in range(N)]
    return ret_board

def run(cnt, board):
    global answer
    if cnt == 5:
        temp_max = max([max(a) for a in board])
        answer = max(answer, temp_max)
        return
    else:
        run(cnt + 1, move_up(board))
        run(cnt + 1, move_down(board))
        run(cnt + 1, move_left(board))
        run(cnt + 1, move_right(board))

answer = 0
run(0, board)
print(answer)
  
# if __name__ == "__main__":
#     board = [
#         [2, 0, 2, 8], [0, 0, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0]
#     ]
#     print(move_left(board))
#     print(move_right(board))
#     print(move_up(board))
#     print(move_down(board))
            