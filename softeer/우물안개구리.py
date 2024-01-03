import sys
from collections import defaultdict

input = sys.stdin.readline
N, M = map(int, input().strip().split(' ')) # 사람수, 친분관계 수 #
weights = list(map(int, input().strip().split(' '))) # 각 회원이 들수 있는 무게 #

friend_dict = defaultdict(list)

for _ in range(M):
    a, b = map(int, input().strip().split(' ')) # 친분관계의 두 회원 번호 #
    a-=1;b-=1
    friend_dict[a].append(b)
    friend_dict[b].append(a)

# P = [i for i in range(N)]
# visited = [False for _ in range(N)]
check = [True for _ in range(N)]

def bfs(a):
    # global friend_dict, P, visited
    global friend_dict, check
    for p in friend_dict[a]:
        if weights[a] > weights[p]:
            check[p] = False
        else:
            check[a] = False
            return

for i in range(N):
    if check[i] == True:
        bfs(i)

# print("Parent ", check)
print(check.count(True))
        
        
                
                
    

    

