""" 프로그래머스 - 가장 큰 정사각형 찾기
[출력] 1과 0으로 채워진 표에서 가장 큰 정사각형을 찾아서 넓이 구하기
"""
import copy
import math

def check_range(x, y, h, w):
    return (0 <= x < w and 0 <= y < h)

def solution(board):
    answer = 1234
    H, W = len(board), len(board[0])
    # 가로, 세로 각각의 DP를 먼저 구해야 한다. DP의 핵심은 memoization이기 때문에 반복되는 계산을 방지하기 위해서 미리 구해 놓는다. #
    # 특히 한 변의 최대 길이가 1000이기 때문에 매번 for i in range(N)이런식으로 반복하면 N^2개에 대해서 O(N^4)의 시간 복잡도를 갖게 될수도 있다. #
    row_dp = [[0 for _ in range(W)] for _ in range(H)]
    col_dp = [[0 for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if board[y][x] == 1:
                if x == 0:
                    row_dp[y][x] = 1
                else:
                    row_dp[y][x] = row_dp[y][x-1] + 1
                if y == 0:
                    col_dp[y][x] = 1
                else:
                    col_dp[y][x] = col_dp[y-1][x] + 1
            
    dp = copy.deepcopy(board)
    for y in range(H):
        for x in range(W):
            if check_range(x-1, y-1, H, W):
                prev_size = dp[y-1][x-1]
                side_size = int(math.sqrt(prev_size))
                max_col = col_dp[y][x];max_row = row_dp[y][x]
                square_size = min([side_size + 1, max_col, max_row])
                dp[y][x] = square_size * square_size
    # print(dp)
    answer = max([max(a) for a in dp])
    return answer

if __name__ == "__main__":
    boards = [
        [[0,1,1,1],[1,1,1,1],[1,1,1,1],[0,0,1,0]],
        [[0,0,1,1],[1,1,1,1]]
    ]
    # for board in boards:
    for bi, board in enumerate(boards):
        print(f"# {bi}")
        print(solution(board))
    