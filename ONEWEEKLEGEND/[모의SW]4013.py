""" 특이한 자석
<조건>
- 판에 4개의 자석이 놓여 있고, 8개의 날을 갖고 있음
- 각 날마다 N, S극의 자성을 갖는다.
- 자석을 1칸씩 K번 회전시키려 할 떄, 1칸 회전 할 때 붙어 있는 자석은 서로 붙어 있는 날의 자성과 다르면 인력에 의해 반대로 회전한다.

<점수>
1번: N - 0 S - 1
2번: N - 0 S - 2
3번: N - 0 S - 4
4번: N - 0 S - 8

<문제>
자석을 1칸씩 K번 회전시키려 할때, 회전 시킨 후 획득하는 점수의 총 합을 출력하여라.
"""

import copy
T = int(input())

def rotate_clock(arr):
    new_arr = [0 for _ in range(len(arr))]
    for i in range(len(arr)):
        new_arr[(i+1) % 8] = arr[i]
    return new_arr

def rotate_counter(arr):
    new_arr = [0 for _ in range(len(arr))]
    for i in range(len(arr)):
        new_arr[(i+7) % 8] = arr[i]
    return new_arr

def rotate(arr, dir):
    if dir == -1:
        return rotate_counter(arr)
    else:
        return rotate_clock(arr)
def continuously_rotate(mag_n, mag_d, magnets):
    # 회전해야 하는 자석 번호, 자석 회전 방향, 자석 정보
    new_magnets = copy.deepcopy(magnets)
    new_magnets[mag_n] = rotate(magnets[mag_n], mag_d) # 타겟이 되는 자석은 무조건 회전해야 한다.
    L, R = mag_n, 3-mag_n

    """
    헷갈리지 말아야 할 것은 자석이 회전을 하고 붙어 있는 자석은 그대로 있는 원래 상태에서 
    **자성이 다르면 반대로 회전** 하는 것이다.
    연쇄적이긴 하지만 **동시에 회전은 아니다**
    """
    for l in range(1, L+1):
        new_n = mag_n - l
        if new_n < 0:
            break
        if magnets[new_n][2] != magnets[new_n + 1][6]:
            # 자성이 다르면 회전
            new_magnets[new_n] = rotate(new_magnets[new_n], mag_d * ((-1) ** l))
        else:
            break
    for r in range(1, R+1):
        new_n = mag_n + r
        if new_n-1 < 0 or new_n > 3:
            break
        if magnets[new_n][6] != magnets[new_n - 1][2]:
            new_magnets[new_n] = rotate(new_magnets[new_n], mag_d * ((-1) ** r))
        else:
            break


    return new_magnets




for tc in range(T):
    K = int(input()) # 자석을 회전시키는 횟수
    magnets = []; answer = 0;
    for i in range(4):
        magnets.append(list(map(int, input().strip().split(' ')))) # N극: 0  |  S극: 1
    for k in range(K):
        mag_n, mag_d = map(int, input().strip().split(' ')) # mag_d가 1이면 시계, -1이면 반시계
        magnets = continuously_rotate(mag_n-1, mag_d, magnets)
    # print(magnets)
    for i in range(4):
        answer += magnets[i][0] * (2 ** i)
    print(f"#{tc+1} {answer}")




