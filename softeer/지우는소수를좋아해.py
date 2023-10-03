""" 문제 설명
- 각 체육관에는 체육관 관장이 있고, 그 관장들을 이겨야 체육관 배지를 얻을수 있다.
- 관장들보다 레벨이 높아야 이길 수 있지만, 레벨 제한도 존재함 + 같은 체육관 사이에 길이 여러개 존재할 수 있다.
- 크루스칼 알고리즘으로 해결하면 될 것 같다!
- 레벨을 prime number에 맞추어서 게임에 참여를 하면서 각각의 체육관을 넘어 마지작 장소에 도착할 수 있는 최소한의 레벨을 구하여라.
"""
import sys
import heapq
import math

# input = sys.stdin.readline()
N, M = map(int, sys.stdin.readline().split()) ## 체육관의 개수, 체육관 사이의 길의 개수
MAX_N = 1000000000
prime_check = [True] * (MAX_N + 1)

levels = []
parents = [i for i in range(N)]


def find(x):
    while x != parents[x]:
        x = parents[x]
    return x


def union(a, b):
    pa, pb = find(a), find(b)
    if pa == pb:
        return True  ## 연결을 하면 사이클이 존재할 것이라는 뜻이다.
    else:
        if pa < pb:
            parents[pb] = pa
        else:
            parents[pa] = pb

        return False


def get_all_primes():
    global prime_check
    prime_check[0] = prime_check[1] = False
    for i in range(2, int(math.sqrt(MAX_N)) + 1):
        if prime_check[i] == True:
            j = 2
            for k in range(i, MAX_N+1, i):
                prime_check[k] = False
            # while (i * j) <= MAX_N:
#                 prime_check[i * j] = False
#                 j += 1


def get_prime_level(c):
    for n in range(c + 1, MAX_N + 1):
        if prime_check[n] == True:
            return n

def check_prime(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True

def get_level(n):
    while True:
        n += 1
        if check_prime(n):
            return n


for m in range(M):
    # A, B, C = map(int, input.strip().split())  ## A 체육관과 B 체육관 사이에 필요 레벨이 C인 길이 존재한다.
    A, B, C = map(int, sys.stdin.readline().split())
    heapq.heappush(levels, (C, A - 1, B - 1))

answer = 0
# get_all_primes()  ## 전체 범위에서 소수인 경우는 True로 설정해 준다.

check = [False] * N

while levels:
    cost, a, b = heapq.heappop(levels)
    check_cycle = union(a, b)
    if check_cycle == True:  ## 사이클이 존재하면 연결을 할 수 없다.
        continue
    else:
        if answer < cost:
            answer = get_level(cost)
            check[a] = True
            check[b] = True
    if check.count(False) == 0:
        break

print(answer)