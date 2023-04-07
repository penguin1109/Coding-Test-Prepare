""" 원자 소멸 시뮬레이션
<조건>
- 원자들이 2개 이상 충돌할 경우 충돌한 원자들은 각자 보유한 에너지를 모두 방출하고 소멸된다.
- 처음에 -1000 <= x,y <= 1000이다.
1. 각자 고유의 움직이는 방향을 갖고 있다.
2. 모든 원자들의 이동 속도는 1초에 1로 동일하다.
3. 모든 원자들은 최초의 위치에서 동시에 이동을 시작한다.
4. 2개 이상의 원자가 동시에 충돌하면 원자들은 **보유한 에너지를 모두** 방출하고 소멸된다.

<주의>
- 원자들은 정수 시간에만 충돌하는게 아니라, 1.5초에도 충돌이 가능하다.
    => 근데 여기서 더 생각해 보면 1.3, 1.7초는 절대 아니고 딱 0.5의 배수로 만난다.
    => 이런 소수가 생기는 이유는 마주보고 다가가는 원소들 사이의 거리의 절반의 시간이 걸릴 수 있기 때문이다.

- 시간이 흘러도 영원히 충돌하지 않는 원자가 있을 수 있다.
- 원자들이 움직일 수 있는 좌표의 범위에는 제한이 없다.
- 원자들의 이동 방향은 처음 주어진 방향에서 바뀌지 않는다. => 이 조건이 추가됨으로서 문제가 한결 간단해 질 수 있다.

<문제>
방출되는 에너지의 총 합을 출력하여라.

<풀이 방법>
- 우선 원자들이 충돌했을 떄의 방출 에너지 합은 구하기가 매우 쉽다.
- 각 원자들이 각자 제일 먼저 충돌하는 상황을 구한다.
- 각 위치에서의 시간별 원자들의 개수를 트래킹하는 것이 제일 중요했다.

**원자들이 서로 만날 수 있는 조건**
1. A는 오른쪽, B는 왼쪽으로 이동하면서 Y좌표가 동일하고 X좌표는 A가 더 큰 경우
2. A는 위, B는 아래로 이동하면서 X좌표가 동일하고 Y좌표는 A가 더 큰 경우
3. A는 오른쪽, B는 위|아래로 이동하면서 abs(delta_{x}) == abs(delta_{y}) 인 경우
"""

import heapq

DX, DY = [0, 0, -1, 1], [1, -1, 0, 0]  # 상하좌우

T = int(input().strip())

def check_crash():
    used_pt = []
    for n in range(N):
        mol = molecule[n]
        mx, my, md, mk = mol
        # 같은 방향으로 이동하는 원소는 절대 만날 수 없다.



def check_range(x, y):
    return (0 <= x < 4000 and 0 <= y < 4000)

MAXSIZE = 4001
board = [[0 for _ in range(MAXSIZE)] for _ in range(MAXSIZE)]

for tc in range(T):
    N = int(input().strip()) # 원자들의 수
    answer = 0 # 총 충돌하면서 방출하는 에너지의 합
    molecule = []


    for n in range(N):
        x, y, d, k = map(int, input().strip().split()) # 원자들의 위치, 이동 방향, 보유 에너지
        # 음수 인덱스의 처리가 까다로워서 양수로 보정을 해주고, 소수 시간 문제로 인해서 0.5를 1로 처리하기 위해서 2를 곱해준다.
        # 이렇게 할 수 있는 이유는 사실상 시간의 <정확한 정보가 중요하지 않기> 때문이다.
        x = (x + 1000) * 2
        y = (y + 1000) * 2
        molecule.append([x, y, d, k])
        board[y][x] += 1 # 좌표에 존재하는 개수를 세어준다.
        pop_list = []
    remove_list = set()

    while molecule:
        for i in range(len(molecule)):
            x, y, d, k = molecule[i]
            nx = x + DX[d]
            ny = y + DY[d]
            # 배열에서 벗어나면 제외 -> 근데 조건에서는 좌표에 제한이 없다고 했는데? -> 그치만 중요한건 이 영역에서 벗어날때까지 충돌한 적이 없으면 결국에는 영원히 못 만난다는 뜻이다.
            if not check_range(nx, ny):
                pop_list.append(i)
                continue
            board[y][x] -= 1 # 이전 위치에서 삭제
            board[ny][nx] += 1 # 새로운 위치에 추가
            molecule[i][0] = nx;molecule[i][1] = ny;

        if pop_list:
            for _ in range(len(pop_list)):
                idx = pop_list.pop()
                tx, ty = molecule[idx][0], molecule[idx][1]
                board[ty][tx] -= 1
                molecule.pop(idx)

        for mol in molecule:
            x, y = mol[0], mol[1]
            if board[y][x] > 1: # 1개 이상의 원소가 포함되어 있기 때문에 충돌했다는 뜻이고, 따라서 제거해 준다.
                remove_list.add((x, y)) # 제거 해야 하는 원소들이 충돌한 좌표를 remove_list에 넣어주고, 중복을 피하기 위해서 set를 사용한다.

        if remove_list: # 충돌했기 때문에 제거해야 하는 원소가 있는 경우에
            for x, y in remove_list:
                for i in range(len(molecule)-1, -1, -1):
                    tx, ty, td, tk = molecule[i]
                    if ty == y and tx == x:
                        board[ty][tx] -= 1
                        answer += tk
                        molecule.pop(i) # 뒤에서부터 빼줘서 pop(idx) 메서드를 사용함에 문제가 없도록 한다.
            remove_list.clear()



    print(f"#{tc+1} {answer}")





