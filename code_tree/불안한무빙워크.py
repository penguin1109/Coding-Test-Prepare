import sys
sys.stdin = open('./input.txt', 'r')
readl = sys.stdin.readline

class Belt:
    def __init__(self, safety, is_person):
        super(Belt, self).__init__()
        self.safety = safety
        self.is_person = is_person
        
# [출력] 전체 과정이 종료될때 몇번의 실험을 거쳤는지 확인 #
N, K = map(int, readl().strip().split(' ')) # 무빙워크의 길이, 안정성이 0인 판의 개수(종료 조건) # 
belts = []
arr = list(map(int, readl().strip().split(' '))) # 벨트의 안전성 #
for safety in arr:
    new_belt = Belt(safety, False)
    belts.append(new_belt)

is_zero = 0

def debug():
    for belt in belts:
        print(f"SAFETY : {belt.safety} HUMAN : {belt.is_person}")
    print("*" * 40)
##### STEP 1 : 1칸 회전 #####
def move_belt():
    global belts
    last = belts[-1]
    belts = belts[:-1]
    belts.insert(0, last)
    
    mid_belt = belts[N-1]
    if mid_belt.is_person == True:
        mid_belt.is_person = False
    

##### STEP 2 : 사람이 있으면 제일 먼저 들어온 사람이 1칸 이동. (칸에 사람이 있거나 안전성이 0이면 이동 불가) #####
def move_person():
    global belts, is_zero
    # 어차피 N-1번째 칸에 도달하면 내리기 때문에 N-2부터 역순으로 확인 #

    for i in range(N-2, -1, -1):
        temp_belt = belts[i]
        if temp_belt.is_person == True:
            if belts[i+1].safety > 0 and belts[i+1].is_person == False: # 안전성이 0이 아닌 경우 & 사람이 없는 경우 # 
                belts[i].is_person = False # 사람 이동 가능 #
                belts[i+1].safety -= 1
                if belts[i+1].safety == 0:
                    is_zero += 1
                if i+1 != N-1:
                    belts[i+1].is_person = True
        
##### STEP 3 : 첫번째 칸에 사람 탑승 #####
def ride_person():
    global belts, is_zero
    first_belt = belts[0]
    if first_belt.is_person == True:
        return
    if first_belt.safety == 0:
        return
    first_belt.is_person = True
    first_belt.safety -= 1
    if first_belt.safety == 0:
        is_zero += 1
    belts[0] = first_belt

def simulate():
    move_belt()
    move_person()
    ride_person()
    debug()
    if is_zero >= K:
        return True
    return False

time = 1
while True:
    do_finish = simulate()
    if do_finish:
        break
    time += 1
    
print(time)