""" 2819: 격자판의 숫자 이어 붙이기

"""
class _board:
    def __init__(self):
        super().__init__()
        self.board = [[] for _ in range(4)]
        self.answer = set()
    
    def run(self):
        for i in range(4):
            for j in range(4):
                self.dfs(1, self.board[i][j], i, j)

    def dfs(self, cnt, temp, x, y):
        if cnt == 7:
            self.answer.add(temp)
        else:
            dx, dy = [-1, 1, 0, 0], [0, 0, -1, 1]
            for i in range(4):
                nx, ny = x + dx[i], y+ dy[i]
                if (0<= nx<4) and (0 <= ny < 4):
                    self.dfs(cnt + 1, temp + self.board[nx][ny], nx, ny)




if __name__ == "__main__":
    T = int(input())
    for t in range(1, T+1):
        board = _board()
        for i in range(4):
            board.board[i] = list(map(str, input().split(' ')))
        board.run()
        print(f"#{t} {len(board.answer)}")
        

