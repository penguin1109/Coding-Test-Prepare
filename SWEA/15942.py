import queue
import copy
""" 풀이 방법
<그리디 알고리즘>
현 시점에서 정복할 수 있는 가장 큰 행성(=가장 주민이 많은 행성)을 정복하고 
침공에 사용 가능할 함선의 수가 늘어난 상태에서
다음으로 정복할 수 있는 행성중 제일 큰것을 찾고 정복할 수 있을 때까지 행성이 큰 순서대로 동원한다.
-> 현재 함선 수 이하의 주민이 있는 행성 중 가장 주민이 많은 행성의 위치를 UPPER BOUND 알고리즘을 사용할 수 있다.
=========================================================================
1. 모든 행성 정복에 필요한 함선의 수를 계산 한다.
2. 현재 함선 수 이하의 주민이 있는 행성 중 가장 주민이 많은 행성을 고른다.
3. <침략>을 진행 하고, 앞으로 행성 정복을 하기 위해서 함선이 더 필요 하다면 <동원>을 한다.
4. 1번부터 반복 한다. 
"""
people = [0 for _ in range(200005)] # 각 행성마다의 인구수
temp = [0 for _ in range(200005)] # merge_sort를 하기 위한 배열
occupy = [False for _ in range(200005)]
parent = [-1 for _ in range(200005)]
def merge_sort(start, end):
    if (start >= end):
        return
    mid = (start + end) // 2
    merge_sort(start, mid)
    merge_sort(mid+1, end)

    i = start;j = mid+1;k = start;
    # temp = [0 for _ in range(len(people))]
    while ((i <= mid) and (j <= end)):
        if (people[i] <= people[j]):
            temp[k] = people[i]
            k += 1;i += 1;
        else:
            temp[k] = people[j]
            k += 1;j+=1;
    while (i <= mid):
        temp[k] = people[i]
        i += 1;
        k += 1;
    while (j <= end):
        temp[k] = people[j]
        j += 1;
        k += 1

    for a in range(start, end+1):
        people[a] = temp[a]


def upper_bound(n, key):
    start = 1;
    end = n
    while (end - start > 0):
        mid = (start + end) // 2
        if (people[mid] <= key):
            start = mid + 1
        else:
            end = mid
    return end
def find(p):
    # print(parent[p])
    if (parent[p] == p):
        return p
    else:
        parent[p] = find(parent[p])
    return parent[p]


def init(n):
    for i in range(n+1):
        occupy[i] = False
        parent[i] = i

T = int(input())
for test_case in range(1, T+1):
    # n, k = map(int, input().split(' ')) # 전체 행성의 수, 외계인이 갖고 있는 함선의 수
    n, k = map(int, input().split(' '))
    planet = list(map(int, input().split(' '))) # n개의 행성 각각에 있는 인간의 수
    people[1: n+1] = planet
    # assert len(planet) == n
    ships_needed = sum(planet)
    merge_sort(1, n)
    # print(people[:n])
    answer = 0
    init(n)
    p = 0
    # print(parent[:n])
    while (ships_needed > k): # 현재 갖고 있는 함선의 수에 비해서 필요한 함수의 개수가 많을 동안
         p = upper_bound(n=n+1, key=k) - 1 # 사실 지금 당장은 불가능할수도 있다. -> 불가능하다면 -1이 return될 것
         # print(p, people[1:n+1])
         # print(ships_needed, k, p)
         # print(occupy[1:n+1])
         if (p > 0):
             p = find(p)
             # print(p)
             if (occupy[p]):
                 answer = -1
                 break
             k += people[p] # 함선 동원
             ships_needed -= people[p] # 행성 침략
             answer += 1 # 동원 횟수 증가
             occupy[p] = True
             if p:
                 parent[p] = find(p-1)
         else:
             answer = -1
             break
    print(f"#{test_case} {answer}")
