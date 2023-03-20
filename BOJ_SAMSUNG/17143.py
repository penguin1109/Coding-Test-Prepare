import sys
input = sys.stdin.readline

## 상어들이 동일한 위치에 있으면 안됨,


R, C, M = map(int, input().split(' '))
board = [[[] for _ in range(C)] for _ in range(R)]
sharkLoc = {}
sharkDir = {}
sharkSpeed = {}
sharkMass = {}
for m in range(M):
    r, c, s, d, z = map(int, input().split(' ')) ## 속력, 방향, 크기
    sharkLoc[m] = [r-1, c-1]
    sharkDir[m] = d
    sharkMass[m] = z
    ## speed로 인해서 넘어가는 일이 없도록 제한을 해 준다.
    if d == 1 or d == 2:
        sharkSpeed[m] = s % (R * 2 - 2)
    else:
        sharkSpeed[m] = s % (C * 2 - 2)
    board[r-1][c-1].append(m)


# 위 - 아래 - 오 - 왼
Dx, Dy = [-1, 1, 0, 0] , [0, 0, 1, -1]
def catch_shark(person):
    for i in range(R):
        if board[i][person] != []:
            sNum = board[i][person][0]
            mass = sharkMass[sNum]
            board[i][person] = []
            del sharkMass[sNum]
            del sharkDir[sNum]
            del sharkLoc[sNum]
            del sharkSpeed[sNum]

            return mass
    return 0


def shark_move():
    for sidx in list(sharkLoc.keys()):
        curX, curY = sharkLoc[sidx]
        curSpeed = sharkSpeed[sidx]

        tx = curX;ty = curY;

        while curSpeed:
            curD = sharkDir[sidx]
            if tx == 0 and curD == 1:
                curD = 2
            if tx == (R-1) and curD == 2:
                curD = 1
            if ty == (C-1) and curD == 3:
                curD = 4
            if ty == 0 and curD == 4:
                curD = 3
            ## 이미 가장자리에 도달한 상황이라면, 예를 들어서 tx == 0이지만 위를 바라보는 상황이라면 이동할 수 없이 가장자리를 벗어나게 된다.
            # 따라서 이미 가장자리에 있으면 방향을 바로 반대로 바꿔 주어야 한다.
            # 근데 중요한건 이렇게 바뀐 방향을 바로바로 업데이트를 해주어야 한다는 것이다. (이부분을 놓쳐서 틀렸다고 함)
            sharkDir[sidx] = curD
            dx, dy = Dx[curD-1], Dy[curD-1]
            nx = tx + dx;ny = ty + dy;
            if curD == 1 and nx == 0: ## 위로 이동하는 와중에 땅에 닿으면 방향 반대로 변경
                sharkDir[sidx] = 2
            elif curD == 2 and nx == (R-1):
                sharkDir[sidx] = 1
            elif curD == 3 and ny == (C-1):
                sharkDir[sidx] = 4
            elif curD == 4 and ny ==0:
                sharkDir[sidx] = 3
            tx = nx;ty = ny;
            curSpeed -= 1 ## curSpeed==0이 되면 해당 상어의 이동은 멈춰도 된다.

        sharkLoc[sidx] = [tx, ty]
        # board[curX][curY] = []
        board[curX][curY].remove(sidx)
        board[tx][ty].append(sidx)

    for i in range(R):
        for j in range(C):
            if len(board[i][j]) > 1:
                candidates = sorted([[a, sharkMass[a]] for a in board[i][j]], key = lambda x: -x[1])
                board[i][j] = [candidates[0][0]] ## 제일 부피가 큰 상어만 남겨 주도록 한다.
                for rest, _ in candidates[1:]:
                    del sharkMass[rest]
                    del sharkDir[rest]
                    del sharkLoc[rest]
                    del sharkSpeed[rest]


answer = 0
for i in range(C):
    answer += catch_shark(i)
    shark_move()
print(answer)







