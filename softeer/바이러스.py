import sys
input = sys.stdin.readline

K, P, N = map(int, input().strip().split(' ')) # 바이러스의 수, 증가율, 총 시간 #
div = 1000000007

'''
1초당 P배 증가.
처음에 K마리 -> N초 후에 몇마리?
'''

for n in range(N):
    