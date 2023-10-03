""" 무선 충전
<조건>
- 각 충전기의 위치, 충전 범위, 성능 정보를 제공한다.
- 충전기의 충전 범위가 C일 때, 충전기와의 거리가 C이하이면 접속 가능하다.
- 거리는 L1 Distance로 계산
- 한 충전기에 두 명의 사용자가 접속한 경우에 접속한 사용자의 수만큼 충전 양을 **균등하게 분배**한다.
- 한 사용자가 여러 충전기에 접속이 가능한 경우가 있기 때문에 충전한 양의 합이 최대가 되도록 해야 한다.
    -> 실제로 나누어서 충전을 하는 대신에 한 사용자가 접속 가능한 다른 충전기를 사용하는게 **당연히 최댓값**이다.
- 사용자가 지도 밖으로 이동하는 경우는 없다.

<문제>
충전기의 정보와 사용자의 이동 궤적이 주어질 때 **모든 사용자가 충전한 양의 합의 최댓값**을 구하여라.

<주의>
- 삼성 코딩 테스트 문제를 풀 때 주의해야 할 점은 x, y좌표의 위치가 기존의 다른 문제들과 달리 순서가 바뀌어 있을 수 있다는 것이다.

"""

import heapq
DY, DX = [0, -1, 0, 1, 0], [0, 0, 1, 0, -1] # 매 초마다의 이동방향
T = int(input())
SIZE = 10 # 지도의 가로와 세로의 크기는 무조건 10
def check_range(x, y):
    return (0 <= x < SIZE and 0 <= y < SIZE)

def dist(x1, y1, x2, y2):
    # 충전기와 사람 사이의 거리를 계산하는 식
    return abs(x1-x2) + abs(y1-y2)
def check_chargable(m, pt, battery):
    x, y = pt
    nax, nay = x + DX[m], y + DY[m]
    chargable = []
    for idx, b in enumerate(battery):
        bx, by, c, p = b
        if dist(nax, nay, bx, by) <= c: # 거리가 충전기의 충전 범위 내에 있으면 추가해 준다.
            heapq.heappush(chargable, (-p, idx)) # chargable.append(idx)
    PT = (nax, nay)
    return PT, chargable

def select_max_val(alist, blist):
    an = len(alist)
    bn = len(blist)
    n = min(an, bn)
    answer = 0
    if n == 0:
        if len(alist) > 0:
            answer = (heapq.heappop(alist)[0] * -1)
        elif len(blist) > 0:
            answer = (heapq.heappop(blist)[0] * -1)
        return answer

    # n이 1이 아니기 때문에 두 리스트에 적어도 하나의 접속 가능한 충전기가 있다는 뜻이다.
    av, ai = heapq.heappop(alist)
    bv, bi = heapq.heappop(blist)
    if ai != bi:
        answer = (av + bv) * -1
    else:
        if alist and blist: # 둘다 2개 이상은 갖고 있는 경우
            av2, ai2 = heapq.heappop(alist)
            bv2, bi2 = heapq.heappop(blist)
            answer = (av + min(av2, bv2)) * -1
        elif alist and not blist:
            av2, ai2 = heapq.heappop(alist)
            answer = (bv + av2) * -1
        elif blist and not alist:
            bv2, bi2 = heapq.heappop(blist)
            answer = (av + bv2) * -1
        else:
            answer = av * -1
    return answer








for tc in range(T):
    M, N = map(int, input().strip().split(' ')) # 총 이동 시간, 충전기의 개수
    # 사용자 각각의 이동 정보는 M개의 숫자로 구성된다. (사용자는 총 2명)
    A = list(map(int, input().strip().split(' '))) # 사용자 A의 이동정보 (0,0)에서 출발
    B = list(map(int, input().strip().split(' '))) # 사용자 B의 이동정보 (9,9)에서 출발

    battery = []
    for _ in range(N):
        # 충전기의 정보는 X , Y , C , P  -> 좌표, 충전 범위, 처리량 이다.
        X, Y, C, P = list(map(int, input().strip().split(' ')))
        battery.append([X-1, Y-1, C, P])

    APT = (0,0) # A의 처음 시작 위치는 (0,0)
    BPT = (9,9) # B의 처음 시작 위치는 (9,9)
    ANSWER = 0
    A = [0] + A
    B = [0] + B
    for time in range(len(A)):
        am = A[time];bm = B[time]; # A, B각각의 이동 방향이다.
        APT, alist = check_chargable(am, APT, battery)
        BPT, blist = check_chargable(bm, BPT, battery)
        ANSWER += select_max_val(alist, blist)
    print(f"#{tc+1} {ANSWER}")







