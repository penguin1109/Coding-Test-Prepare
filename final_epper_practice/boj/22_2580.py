""" BOJ 2580. 스도쿠
- 가로 세로 각각 9개씩 총 81개의 작은 칸으로 이뤄진 정사각형
- 각 가로, 세로 줄에는 1-9까지의 숫자가 한번씩만 나타나야 함
- 3x3의 정사각형에도 1-9까지의 숫자가 한번씩만 나타나야 함
[출력] 빈칸은 0으로 나타내어질 때 스도쿠 판을 채우는 방법이 여럿인 경우 하나만 출력하여라.
[풀이 방법]  보면 당연하게도 모든 경우의 수를 시도해 보는 백트래킹이 맞을 것 같다.
            근데 매번 스도쿠 판을 재귀 함수의 인자로 넣어주는게 맞을지는 모르겠다.
            그냥 무지성으로 채워 넣은 다음에 (모든 조합을 다 테스트해 볼 수는 없고 합리적인 경우의 수에 대해서 테스트를 해 볼 필요가 있을 것.)

Q1) 비트마스킹을 써서 숫자 탐색을 한다고 해도 도움이 될까?
Q2) 매번 check_valid 함수로 유효한 스도쿠판인지 확인하는게 가능할까? -> 근데 시간초과를 걱정했는데 생각보다 시간초과는 안날수도. 왜냐면 어차피 9x9로 크기는 무조건 고정이니까..

"""
import sys
input = sys.stdin.readline

board = [list(map(int, input().strip().split(' '))) for _ in range(9)]
answer = False
def print_answer(board):
    for n in range(9):
        print(' '.join(list(map(lambda x : str(x), board[n]))) ) # + "\n")
        # print('\n')
    

row_track = [[False for _ in range(10)] for _ in range(9)]
col_track = [[False for _ in range(10)] for _ in range(9)]
squ_track = [[False for _ in range(10)] for _ in range(9)]

def get_squ(x, y):
    ''' 좌표를 입력으로 받아서 몇번째 3x3 정사각형인지 index를 반환한다.
    0 1 2
    3 4 5
    6 7 8
    '''
    n_squ = (y // 3) * 3 + (x // 3)
    return n_squ

def dfs(n):
    if n == 9**2:
        print_answer(board)
        exit(0) # 완전히 exit.. #
    y, x = n // 9, n % 9 # 세로, 가로 index #
    if board[y][x] == 0: ## 0이니까 채워줘야 하는 상황이기 때문에 1부터9까지의 숫자들을 넣어보면서 back-tracking + recursive하게 탐색한다. ##
        n_squ = get_squ(x, y)
        
        for i in range(1, 10):
            if (row_track[y][i] == False and col_track[x][i] == False and squ_track[n_squ][i] == False):
                row_track[y][i] = True
                col_track[x][i] = True
                squ_track[n_squ][i] = True
                board[y][x] = i
                dfs(n+1)
                board[y][x] = 0
                squ_track[n_squ][i] = False
                col_track[x][i] = False
                row_track[y][i] = False
    else:
        dfs(n+1)
        
for y in range(9):
    for x in range(9):
        if board[y][x] != 0:
            row_track[y][board[y][x]] = True
            col_track[x][board[y][x]] = True
            squ_track[get_squ(x, y)][board[y][x]] = True

dfs(0)

def check_valid(board):
    for row in range(9):
        bit_mask = 0
        for n in board[row]:
            bit_mask |= (1 << n)
        if bit_mask != 1022:
            return False
    
    for col in range(9):
        temp_col = [board[col][i] for i in range(9)]
        bit_mask = 0
        for n in temp_col:
            bit_mask |= (1 << n)
        if bit_mask != 1022:
            return False
    
    for yi in range(3):
        for xi in range(3):
            temp = board[yi * 3:(yi+1)*3]
            temp = [t[xi*3:(xi+1)*3] for t in temp]
            temp = [item for sublist in temp for item in sublist]
            print(temp)
            bit_mask = 0
            for n in temp:
                bit_mask |= (1 << n)
            if bit_mask != 1022:
                return False
            
    return True


    

