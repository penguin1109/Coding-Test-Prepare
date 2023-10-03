"""
- 우승자는 주어진 숫자판 중에서 2개를 선택해서 정해진 횟수만큼 서로의 자리의 위치 교환 가능
- 상금은 숫자판의 위치에 부여된 가중치에 의해서 계산
- 가중치는 오른쪽 끝이 1원, 왼쪽으로 갈수록 10의 배수만큼 커짐 => 결국에는 있는 그대로 10진수로 계산하면 됨
[출력] 정해진 횟수만큼 교환 후 받을 수 있는 가장 큰 금액
[풀이 방법] 2개를 선택하는 모든 조합을 계산해서 그 중에서 trial의 개수만큼 중복해서 선택 한 다음에 최댓값 구하기
    -> 근데 이제 중복되는 선택을 짝수번 하는 경우에는 그게 불가능함
    -> 최대 자리수가 6자리이기 때문에 2개씩의 조합을 모두 구하는게 가능
    -> 교환 횟수가 1,2번까지는 상관이 없는데 그 이상으로 넘어가면 조합이 겹치는게 생길 수 있기 때문에 그 부분도 막아 주어야 한다.
    
    ======= NEW SOLUTION ========
    1. 만들어질 수 있는 제일 큰 수부터 해서 주어진 trials안에 만드는게 가능한 것인지 확인해 보기
"""

answer = 0
T = int(input().strip()) # 테스트케이스 개수

def _make_comb(N):
    s = str(N)
    N = len(s)
    combs= []
    
    for n in range(N):
        for k in range(n+1, N):
            combs.append(f"{n}{k}")

    return combs

def _swap(s, i, j):
    a, b = s[i], s[j]
    temp = s[:i] + b + s[i+1:j] + a + s[j+1:]
    return temp

def _search_max(trial_left, prev_s, target):
    global valid
    if trial_left == 0:
        if str(target) ==prev_s:
            valid=True
        return
    # for comb in combs: ## 이렇게 모든 경우를 다 한다면 (nC2 ^ 10)이 최대 시간 복잡도이기 때문에 TLE가 발생할 수 밖에 없다.
    #     i, j = comb[0], comb[1]
    #     i, j = int(i), int(j)
    #     new_s = _swap(prev_s, i, j)
    #     _search_max(comb_dict, trial_left-1, new_s, target)
    #     comb_dict[key] = value
    N = len(str(target))
    for i in range(N):
        for j in range(i+1, N):
            new_s = _swap(prev_s, i, j)
            _search_max(trial_left-1, new_s, target)
    
        
def _make_nums(visited, s, tot_length, init_s):
    global nums
    if len(s) == tot_length:
        nums.append(int(s))
        return
    for n in range(tot_length):
        if visited[n] == False:
            visited[n] = True
            _make_nums(visited, s + init_s[n], tot_length, init_s)
            visited[n] = False

def _run_change(nums, left_trial):
    global answer, track_dict
    # print(track_dict)
    first= ''.join(nums)
    if left_trial == 0:
        s = ''.join(nums)
        # print(s)
        answer = max(answer, int(s))
        return
        
    else:
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                nums[i], nums[j] = nums[j], nums[i]
                ns = ''.join(nums)
                if ns in track_dict:
                    if first==ns: ## 이전이랑 동일한게 나왔으면 또 똑같은게 나올 가능성이 있다는 뜻이기 때문에 여기서 그냥 남은 횟수를 0으로 보내 주어야 한다.
                        _run_change(nums, 0)
                    elif track_dict[ns] < left_trial: ## 이미 만들어본적이 있는 문자열에 대해서는 관여를 하지 않는다
                        track_dict[ns] = left_trial
                        _run_change(nums, left_trial-1)
                else: ## 처음 만들어지는 숫자인 경우에
                    track_dict[ns] = left_trial
                    _run_change(nums, left_trial-1)
                    
                nums[i], nums[j] = nums[j], nums[i]

for t in range(T):
    answer = 0
    init, trial = map(int, input().strip().split(' '))
    track_dict = {}
    nums = [str(s) for s in str(init)]
    """
    - 여기서 교환 횟수와 전체 문자열의 길이 중에서 더 짧은 것을 선택하는 것이 시간 초과를 줄이는 핵심이었다.
    """
    _run_change(nums, trial)
    # _run_change(nums, min(trial, len(nums)))
    # _run_change(nums, min(trial, len(nums)), 0)
    print(f"#{t+1} {answer}")
# for t in range(T):
#     answer = 0;nums=[]
#     init, trial = map(int, input().strip().split(' ')) # 초기에 입력 받은 숫자판, 교환 횟수
#     visited = [False for _ in range(len(str(init)))]
#     _make_nums(visited, '', len(str(init)), init_s=str(init))
#     nums = sorted(nums, reverse=True) # 만들어 질 수 있는 큰 수부터 확인하기 
#     valid = False
#     for n in nums:
#         _search_max(trial, str(init), target=n)
#         if valid == True:
#             answer = n
#             break
#     print(f"#{t+1} {answer}")
    