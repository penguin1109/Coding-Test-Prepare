import sys
sys.stdin = open('C:/Users/user/git_repos/samsung_code/input.txt', 'r')

input = sys.stdin.readline

T = int(input())
import copy
def rotate_anticlockwise(arr):
    first = arr[0]
    new = arr[1:]
    new.append(first)
    return new
def rotate_clockwise(arr):
    last = arr[-1]
    new = arr[:-1]
    new.insert(0, last)
    # arr = arr[:-1]
    return new
def rotate(magnets, idx, dir):
    """시계방향으로 회전하는 경우"""
    new_magnets = [[0 for _ in range(8)] for _ in range(4)]
    # print(f"MAG : {magnets}")
    prev = idx;prev_dir = dir
    for left in range(idx-1, -1, -1):
        l, r = magnets[left][2], magnets[prev][6]
        # print(left, l, r, prev)
        # print(f"MAGG : {magnets}")
        if l != r:
            temp = magnets[left]
            new_magnets[left] = rotate_clockwise(temp) if prev_dir == -1 else rotate_anticlockwise(temp)
            prev = left;prev_dir *= -1
        else:
            for i in range(left, -1, -1):
                new_magnets[i] = magnets[i]
            break
    prev = idx;prev_dir = dir
    for right in range(idx+1, 4):
        l, r = magnets[prev][2], magnets[right][6]
        if l != r:
            temp = magnets[right]
            new_magnets[right] = rotate_clockwise(temp) if prev_dir == -1 else rotate_anticlockwise(temp)
            prev = right
            prev_dir *= -1
        else:
            for i in range(right, 4):
                new_magnets[i] = magnets[i]
            break
    new_magnets[idx] = rotate_clockwise(magnets[idx]) if dir == 1 else rotate_anticlockwise(magnets[idx])
    return new_magnets


def calculate_score():
    scores = sum([magnets[i][0] * (2 ** i) for i in range(4)])
    return scores



for test_case in range(1, T+1):
    K = int(input().strip()) # 자석을 회전시키는 횟수 #
    magnets = [list(map(int, input().strip().split(' '))) for _ in range(4)]
    answer = 0
    for k in range(K):
        idx, dir = map(int, input().strip().split(' ')) # 회전시킬 자석의 번호, 회전의 방향 #
        magnets = rotate(magnets, idx-1, dir)

        # print(magnets)
    # break
    answer = calculate_score()
    print(f"#{test_case} {answer}")
