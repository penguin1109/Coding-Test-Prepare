import copy
from collections import defaultdict

def solution(topping):
    answer = 0
    forward = set()
    backward = defaultdict(int)
    for top in topping:
        backward[top] += 1
    for top in topping:
        forward.add(top)
        backward[top] -= 1
        if backward[top] == 0:
            del backward[top]
        if len(forward) == len(backward):
            answer += 1

    """ TLE
    ing_types = sorted(list(set(topping)))
    ing_dict = {value:key for key, value in enumerate(ing_types)}
    
    memory = []
    prev_cnt = [0 for _ in range(len(ing_types))]
    memory = [[0] *  len(ing_types) for _ in range(len(topping))]
    for idx, top in enumerate(topping):
        prev_cnt[ing_dict[top]]  += 1
        memory[idx] = copy.deepcopy(prev_cnt)
        #memory[idx][ing_dict[top]]  += 1
        #prev_cnt = new_cnt

    for idx, mem in enumerate(memory):
        # print(mem)
        cnt = sum([x != 0 for x in mem])
        diff = len([a-b for a,b in zip(memory[-1], mem) if (a-b)!=0])
        # print(cnt, diff)
        if cnt == diff:
            answer += 1
    """

    return answer

if __name__ == "__main__":
    inputs = [
        [1, 2, 1, 3, 1, 4, 1, 2],
        [1, 2, 3, 1, 4]
    ]
    for topping in inputs:
        print(solution(topping))
