""" BOJ 15663 - N과 M(9)
- N, M이 주어질때 조건을 만족하는 길이가 M인 수열을 모두 구하여라
<조건> N개의 자연수 중에서 M개를 고른 수열
"""
import sys
input = sys.stdin.readline

N, M = map(int, input().strip().split(' '))
numbers = sorted(list(map(int, input().strip().split(' '))))

answer = set()

def get_arrs(visited, temp):
    global answer
    if len(temp) == M:
        # print(' '.join(list(map(lambda x : str(x), temp))))
        '''여기서 print를 해 줘야 나중에 sort할 필요 없이 사전순 정렬된 수열이 됨'''
        if ' '.join(temp) not in answer:
            answer.add(' '.join(temp))
            print(' '.join(temp))
        '''이 부분에서 <자연수>가 두자리 자연수일수도 있는데 간과함'''
        # answer.append(' '.join(list(map(lambda x : str(x), temp))))
        # answer.add(' '.join(temp))
        return
    for i in range(N):
        if visited[i] == False:
            visited[i] = True
            get_arrs(visited, temp+[str(numbers[i])])
            visited[i] = False
visited = [False for _ in range(N)]
get_arrs(visited, [])    
# answer = list(set(answer))
'''그리고 수열을 정렬하는 것과 단순히 문자열을 정렬하는 것은 다르기 때문에 먼저 전체 numbers를 정렬 한 다음에 dfs를 해줌'''
# for i in range(N):
#     visited[i] = True
#     get_arrs(visited, [str(numbers[i])])
#     visited[i] = False
get_arrs(visited, [])