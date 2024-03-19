import sys
input = sys.stdin.readline

N = int(input().strip())
nums = list(map(int, input().strip().split(' ')))
answer = 0
for i in range(N-2):
    target = nums[i]
    J = []
    for next in range(i+1, N):
        if target > nums[next]:
            answer += len(J)
        elif target < nums[next] and next < N-1:
            J.append(next)
print(answer)