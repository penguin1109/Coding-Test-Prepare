import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')
readl = sys.stdin.readline

A = str(readl().strip())  # 문자열 #
A = [str(i) for  i in A]
def rle(s):
    prev = s[0]
    cnt = 1
    answer = ''
    valid = False
    for i in range(1, len(s)):
        valid = True
        if s[i] == prev:
            cnt += 1
        else:
            answer += f"{prev}{cnt}"
            cnt = 1
            prev = s[i]
        if i == len(s)-1:
            answer += f"{prev}{cnt}"

    if valid != True:
        answer = f"{prev}{cnt}"
    return len(answer)

def shift_once(s):
    import copy
    end = s[-1]
    new = copy.deepcopy(s)
    new.insert(0, end)
    new = new[:-1]
    return new
def simulate():
    global A
    answer = float("INF")
    # if len(A) == 1: ## 길이가 1인 경우에 대해서 처리를 해 줬어야 했다 ##
    #     print(2)
    #     return
    for i in range(len(A)): ## 근데 한 경우를 빼놓다보니까 어쩔수 없음 ##
        A = shift_once(A)
        # print(A)
        answer = min(answer, rle(A))
    print(answer)

simulate()

