""" 20055 - 컨베이어 벨트 위의 로봇
<문제 설명>
- 1번 칸: 올리는 위치
- N번 칸: 내리는 위치
- 딱 로봇은 지정된 1번, N번위치에서 각각 올리고 내리는게 가능하다.
- 로봇은 하나씩 올린다.
- 로봇은 벨트 위에서 스스로 이동할 수 있으며, 로봇이 위치한 칸의 내구도는 도착 즉시 1만큼 감소한다.

<로봇 이동 조건>
1. 벨트가 각 칸 위의 로봇과 함께 한 칸씩 회전한다.
2. 먼저 올라간 로봇부터 회전하는 방향으로 한칸 이동 가능하면 1칸 이동한다.
    - 이동하려는 칸에 로봇이 없거나 내구도 >= 1이어야 한다.
3. 내구도가 0인 칸의 개수가 K개 이상이면 종료하고 아님 1번으로 돌아간다.

<출력>
- 몇번째 단계가 진행 중일 때 종료되는지 출력하여라
"""
from collections import deque
## 입력 받기 ##
N, K = map(int, input().split(' '))
belt = list(map(int, input().split(' ')))
up, down = 0, N-1
robots = [0 for _ in range(N)] # deque([0 for _ in range(2*N)])
track = 0
def rotate_one_step():
    global belt, robots
    ## 1번 단게: 벨트와 로봇이 함께 회전한다.
    a = belt[-1]
    belt = [a] + belt[:(2*N)-1]

    a = robots[-1]
    robots = [a] + robots[:N-1]

    if robots[down] == 1: # 로봇이 내리는 위치에 도달함
        robots[down] = 0 # 즉시 로봇을 내려야 함




def check_stable(n):
    ## 로봇이 없고 내구성이 1이상일 때
    if belt[n] >= 1 and robots[n] == 0:
        return True

    return False

def move_robot():
    global track
    ## 2. 로봇이 한칸 앞으로 움직일 수 있다면 한칸 이동하게 한다.
    for n in range(N-2, 0, -1):
        place = (n + 1) % (2*N)
        if robots[n] == 1 and check_stable(place):
            robots[n] = 0
            robots[place] = 1
            belt[place] -= 1 # 도달하는 순간 내구성 감소
    if robots[down] == 1: # 내리는 위치에 로봇이 있으면 즉시 로봇을 내려줌
        robots[down] = 0

def upload_robot():
    global track
    ## 3. 올리는 자리에 로봇을 올려준다.
    if belt[up] >= 1:
        belt[up] -= 1 # 올리는 위치의 내구성 감소
        robots[up] = 1


time = 0
# upload_robot()
while True:
    time += 1
    rotate_one_step()
    move_robot()
    upload_robot()
    if belt.count(0) >= K:
        break

print(time)





