import sys
input = sys.stdin.readline

moves = list(map(int, input().strip().split(' '))) # 이동 칸 수 10개 #
'''
- 원하는 때 어떤 이동 칸 수가 나올지 예상 가능
- 매 회차마다 주어진 이동 횟수에 나갈 말의 종류를 조합해서 얻을 수 있는 점수의 최댓값
- 
[출력] 입력으로 주어지는 이동 칸수를 조합해 얻을 수 있는 점수의 최댓값
'''
board = [
    0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 0,  # [0번째 ~ 20번째] -> 5, 10, 15번째 
    13, 16, 19, 0, 0, # [21번째 ~ 25번째]
    22, 24, 0, 0, 0, # [26번째 ~ 30번째]
    28, 27, 26, 0, 0, # [31번쨰 ~ 35번째]
    0, 0, 0, 0, 0,  # [36번째 ~ 40번째]
    25, 30, 35, 40, # [41번째 ~ 44번째]
]
START = 0
END = 20
curr_pos = [START, START, START, START]
         
def check_overlap():
    '''시작과 도착 지점을 제외하고는 동일한 위치에 놓일 수 없다.'''
    return any([
        curr_pos[i] == curr_pos[j] and curr_pos[i] != START and curr_pos[i] != END 
        for i in range(4) for j in range(i+1, 4)
    ])

def check_blue(pos):
    return pos != START and pos % 5 == 0

def get_next_pos(pos, move):
    if pos == END:
        return END
    if move == 0:
        return pos
    next_pos = pos + 1
    
    if pos in [23, 27, 33]:
        next_pos = 41
    elif pos == 44:
        next_pos = END
    elif pos == 19:
        next_pos = 44
    return get_next_pos(next_pos, move-1)
    
def simulate(idx, score):
    global answer
    
    # answer = max(answer, score)
    if idx == 10:
        answer = max(answer, score)
        return
    
    for pi in range(4):
        pos = curr_pos[pi]
        if pos == END:
            continue
            
        if check_blue(pos) == True: # 이동 시작 시점의 위치가 파란색이면 #
                # if pos == 5:
                #     pos = 21
                # elif pos == 10:
                #     pos = 26
                # elif pos == 15:
                #     pos = 31
            curr_pos[pi] = get_next_pos(curr_pos[pi] + 16, moves[idx] - 1)
        else:
            curr_pos[pi] = get_next_pos(curr_pos[pi], moves[idx])
        
        if check_overlap() == False:
            simulate(idx+1, score + board[curr_pos[pi]])
        
        curr_pos[pi] = pos # DFS로 simulate를 하였을 테니 다시 위치 배열은 원상 복구를 해 주어야 한다. #

answer = 0
simulate(0, 0)
print(answer)
          