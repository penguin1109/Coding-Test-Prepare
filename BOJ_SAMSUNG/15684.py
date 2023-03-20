""" 15684: 사다리 조작
- N개의 세로선과 M개의 가로선으로 이루어져 있다.
- 세로선 사이에는 가로선을 놓을 수 있는데, 각각의 세로선마다 가로선을 놓을 수 있는 위치는 H이고, 모든 세로선이 같은 위치이다.
- 사다리에 가로선을 추가해서 사다리 게임의 결과를 조작하려 하는데, 이때 i번째 세로선의 결과가 i번이 나와야 한다. 추가해야 하는 가로선 개수의 최솟값은?
- 단, 추가해야 하는 가로선의 최솟값의 개수가 3보다 큰 값이면 -1을 출력하고 불가능한 경우에도 -1을 출력한다.
"""
import sys
from copy import deepcopy

def check(ladder):
    ## i - i 세로줄끼리 연결이 되는지 확인
    for i in range(N):
        col = i
        for row in range(H):
            if ladder[row][col]:
                col += 1
            elif 0 < col and ladder[row][col-1]:
                col -= 1
        if col != i:
            return False
    return True

def dfs(idx, cnt, max_cnt, ladder):
    if cnt == max_cnt:
        if check(ladder):
            print(max_cnt)
            exit(0)
        return
    for i in range(H): ## 가로 
        for j in range(idx, N-1): ## 세로 (저번에 탐색했던 세로선 탐색에서부터 다시 이어서 시작할 수 있도록 해야 한다.)
            if ladder[i][j] != 1: ## 연결이 안 되어 있으면
                if 0 < j and ladder[i][j-1] == 1: ## 왼쪽이 연결 된 경우
                    continue
                if j < N-1 and ladder[i][j+1] == 1: ## 오른쪽이 연결된 경우
                    continue
                ladder[i][j] = 1
                dfs(j, cnt+1, max_cnt, ladder) 
                ladder[i][j] = 0

if __name__ == "__main__":
    N, M, H = map(int, input().split(' ')) ## 세로선, 가로선, 각각의 세로선마다 그을 수 있는 가로선의 개수
    ladder = [[0] * N for _ in range(H)]
    for _ in range(M):
        a, b = map(int, input().split(' '))
        ladder[a-1][b-1] = 1
    for h in range(4):
        dfs(0, 0, h, deepcopy(ladder))
    print(-1)
"""
풀이 과정
1. 처음에는 단순히 모든 세로선 사이에 연결된 가로선의 개수가 짝수개가 되도록 해야 한다고 생각 했었다. 그래서 홀수개의 개수가 3개보다 많으면 -1을, 나머지는 개수대로 출력하도록 했다.
그러나 오답이라고 거의 1%만에 결과가 나왔기 때문에 방법을 바꾸기로 했다.
2. 어쨌든 문제 자체는 백트래킹 문제라고 했으니 방법을 더 복잡하게 생각해 보기로 했다.
"""