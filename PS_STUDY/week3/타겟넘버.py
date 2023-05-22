answer = 0


def dfs(numbers, current, target, idx):
    # 모든 경우를 탐색해야 하기 때문에 depth first search를 사용해야 한다.
    global answer
    if idx == len(numbers):
        if current == target:
            answer += 1
        return
    temp = numbers[idx]
    dfs(numbers, current + temp, target, idx + 1) # 재귀적으로 구현을 하기 때문에 dfs!!
    dfs(numbers, current - temp, target, idx + 1)


def solution(numbers, target):
    global answer
    dfs(numbers, 0, target, 0)

    return answer