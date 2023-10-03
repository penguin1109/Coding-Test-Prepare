import heapq
from collections import defaultdict, deque
"""
- 처음에는 <add_first_tree> 함수에서 만약에 나무의 나이가 더 어린 애를 뒤에 push하면 어쩌나 걱정했는데
- 생각해보니 "동일한 영역에 있을 때"에만 겹치면 안되는 것이기 때문에 걱정할 필요가 없었다.
"""

class Land:
    def __init__(self, N, M, K):
        super().__init__()
        self.N = N ## 전체 땅의 가로, 세로의 크기
        self.M = M ## 심은 나무의 개수
        self.K = K ## 지나는 해의 수
        self.nutrition = [[5 for _ in range(N)] for _ in range(N)]
        self.added = [[0 for _ in range(N)] for _ in range(N)]
        #self.tree = defaultdict(list)
        self.tree = [deque() for _ in range(self.N * self.N)]
        self.tree_cnt = 0 ## 땅에 있는 나무의 개수


    def add_first_tree(self, x, y, z):
        self.tree[(x-1) * self.N + (y-1)].append(z)
        # heapq.heappush(self.tree[(x-1) * self.N + (y-1)], z)## 나무의 나이로 추가해줌
        self.tree_cnt += 1

    def winter(self):
        for i in range(self.N):
            for j in range(self.N):
                self.nutrition[i][j] += self.added[i][j] ## 양분을 땅에 추가해 주기
    
    def spring(self): ## 나무들이 나이만큼 양분을 얻은 뒤에 각각의 나이가 1만큼 증가하게 된다.
        for i in range(self.N):
            for j in range(self.N):
                idx = (i*N) + j
                left_nu = self.nutrition[i][j]
                need_to_add = []
                dead = []
                while self.tree[idx]:
                    # temp = heapq.heappop(self.tree[idx])
                    temp = self.tree[idx].popleft()
                    if temp <= left_nu:
                        left_nu -= temp
                        need_to_add.append(temp+1)
                    else:
                        dead.append(temp)
                self.nutrition[i][j] = left_nu
                for tree in need_to_add:
                    self.tree[idx].append(tree)
                    # heapq.heappush(self.tree[idx], tree)
                for tree in dead:
                    self.tree_cnt -= 1
                    self.nutrition[i][j] += tree//2 ## 여름에 벌어지는일까지 같이 해 줌

    def fall(self): ## 나무들이 나이가 5의 배수이면 번식을 한다.
        dx, dy = [-1,-1,-1,1,1,1,0,0], [-1,1,0,1,-1,0,-1,1]
        for i in range(self.N):
            for j in range(self.N):
                idx = (i*self.N) + j
                for tree in self.tree[idx]:
                    if tree % 5 == 0: ## 번식이 가능하면
                        for dirX, dirY in zip(dx, dy):
                            nX, nY = i+dirX, j + dirY
                            if (0 <= nX < self.N) and (0 <= nY < self.N):
                                self.tree[nX * self.N + nY].appendleft(1) ## 나이 어린, 새롭게 생긴 나무들은 앞에 넣어준다.
                                # heapq.heappush(self.tree[nX * self.N + nY], 1)
                                self.tree_cnt += 1


if __name__ == "__main__":
    N, M, K = list(map(int, input().split(' ')))
    board = Land(N, M, K)

    for i in range(N):
        board.added[i] = list(map(int, input().split(' ')))

    for _ in range(M):
        x,y,z = list(map(int, input().split(' ')))
        board.add_first_tree(x, y, z)

    
    for year in range(K):
        board.spring()
        board.fall()
        board.winter()
    
    print(board.tree_cnt)