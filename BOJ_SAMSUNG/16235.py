from collections import deque

N, M, K = map(int, input().split(' '))
A = [] # 각 땅의 위치에 추가 공급이 되는 영양의 양
nutrition = [[5 for _ in range(N)] for _ in range(N)] # 저장되어 있는 영양분의 양
trees = [[deque() for _ in range(N)] for _ in range(N)] # 각 땅의 위치에 저장이 되어 있는 나무들의 나이
tree_count = M # 우선은 살아있는 나무의 수가 입력으로 정보가 주어지는 M이다.

for n in range(N):
    A.append(list(map(int, input().split(' '))))

for m in range(M):
    x, y, z = map(int, input().split(' ')) # 나무의 위치, 나무의 나이
    trees[x-1][y-1].append(z) # 나무를 저장하는 배열에 나이 z를 갖는 나무를 넣어 준다.

def spring(tree_count):
    for x in range(N):
        for y in range(N):
            nu_left = nutrition[x][y]
            dead = []
            alive = []
            while trees[x][y]:
                temp = trees[x][y].popleft()
                if temp <= nu_left:
                    nu_left -= temp
                    alive.append(temp + 1) # 자신의 나이만큼 양분을 먹으면 나이가 1만큼 증가한다.
                elif temp > nu_left:
                    dead.append(temp)
            nutrition[x][y] = nu_left # 남아있는 양분의 양을 다시 갱신해 준다.
            for tree_age in alive:
                trees[x][y].append(tree_age)
            for tree_age in dead:
                nutrition[x][y] += tree_age//2
                tree_count -= 1
    return tree_count

def fall(tree_count):
    dx, dy = [-1,-1, -1, 1, 1, 1, 0, 0], [-1, 1, 0, -1, 1, 0, -1, 1]

    for x in range(N):
        for y in range(N):
            for tree_age in trees[x][y]:
                if (tree_age % 5 == 0):
                    for dir in range(8):
                        nx = x + dx[dir];ny = y + dy[dir]
                        if (0 <= nx < N) and (0 <= ny < N):
                            trees[nx][ny].appendleft(1)
                            tree_count += 1
    return tree_count

def winter():
    for x in range(N):
        for y in range(N):
            nutrition[x][y] += A[x][y]


for k in range(K):
    tree_count = spring(tree_count)
    tree_count = fall(tree_count)
    winter()

print(tree_count)



