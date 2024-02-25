""" 프로그래머스 - 3xn 타일링
- 가로가 2, 세로가 1인 직사각형 모양의 타일 존재
- 
"""
DIV=1000000007

def solution(n):
    if n == 2:
        return 3
    if n == 4:
        return 11
    
    answer = 0
    
    # n /= 2
    # n -= 2
    ## n=2, n=4 일때는 고려를 미리 했기 때문에 저렇게 나눠주면 됨 ##
    # cnts = (3, 11) # (f[2], f[4])
    cnts = [0 for _ in range(n+1)]
    cnts[2] = 3
    if n > 2:
        cnts[4] = 11
        for i in range(6, n+1):
            if i%2 == 0: # 짝수인 경우만 개수 존재 #
                cnts[i] = 3 * cnts[i-2] + 2
                for j in range(i-4, -1, -2):
                    cnts[i] += 2 * cnts[j]
                cnts[i] %= DIV
            else: # 홀수인 경우엔 가능성이 없음 #
                cnts[i] = 0
        
                
    # while n > 0:
    #     cnts = (cnts[1], cnts[1] * 4 - cnts[0]) # 4*f(n-1) - f(n-4) = f(n) #
    #     n -= 1
    '''점화식의 정석으로 구해보자'''
    # answer = cnts[1] % DIV
    answer = cnts[-1] % DIV
        
        
    return answer