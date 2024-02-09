n, m = map(int, input().strip().split(' '))
numbers = list(map(int, input().strip().split(' ')))
combinations = []
import copy
def combi(temp, idx):
    
    global combinations, m, numbers

    if len(temp) == 3:
        if sum(temp) <= m:
            combinations.append(temp)
        return
    if idx == len(numbers):
        return    
    cpy = copy.deepcopy(temp)
    cpy.append(numbers[idx])
    combi(cpy, idx+1)
    combi(temp, idx+1)

combi([], 0)
sums = list(map(lambda x : sum(x), combinations))
sums = sorted(sums, reverse = True)
if sums != []:
    print(sums[0])
else:
    print(-1)
    

