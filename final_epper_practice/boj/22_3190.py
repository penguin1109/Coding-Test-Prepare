""" BOJ 3190.뱀
- 사과 : 길이+
- 벽이나 자신의 몸과 부딪히면 끝
- 처음 뱀의 위치 : (1, 1)
- 처음 뱀의 길이 : 1
- 처음 뱀의 방향 : 오른쪽

[출력] 게임이 몇 초에 끝나는지
"""
import sys
input = sys.stdin.readline

N = int(input().strip()) # 보드의 크기 #
K = int(input().strip()) # 사과의 개수 #

DX, DY = [1, 0, -1, 0], [0, 1, 0, -1] # 우, 하, 좌, 상 #


def _in_range(x, y):
    return (0 < x <= N) and (0 < y <= N)

class Snake:
    def __init__(self):
        super(Snake, self).__init__()
        self.head = (1, 1)
        self.tail = (1, 1)
        self.dir = 0 # 오른쪽 #

        self.track = [[-1 for _ in range(N+1)] for _ in range(N+1)]
        self.track[1][1] = 1
        
        self.queue = [(1, 1)]
    
    def _change_dir(self, c):
        if c == 'L': # 왼쪽 90도 회전 #
            self.dir = (self.dir + 3) % 4
        elif c == 'D': # 오른쪽 90도 회전 #
            self.dir = (self.dir + 1) % 4
    
    def _move_one_step(self):
        hx, hy = self.head
        hx += DX[self.dir]
        hy += DY[self.dir]
        
        if _in_range(hx, hy) == False: # 벽에 부딪힌 경우 #
            return False
        
        if self.track[hy][hx] == 1: # 자신의 몸과 부딪힌 경우 #
            return False
        
        elif self.track[hy][hx] == 0: # 사과가 있는 경우에 사과는 없애고 꼬리는 고정 #
            self.track[hy][hx] = 1
            self.head = (hx, hy)
            self.queue.append((hx, hy))
            
        else: # 사과가 없는 경우에는 꼬리가 한칸 앞으로 이동 #
            self.queue.append((hx, hy))
            self.queue = self.queue[1:]
            self.track[self.tail[1]][self.tail[0]] = -1
            self.tail = self.queue[0]
            self.head = (hx, hy)
            self.track[hy][hx] = 1
        return True
            
        
 
snake = Snake()

for k in range(K):
    y, x = map(int, input().strip().split(' ')) # 행 위치, 열 위치 #
    snake.track[y][x] = 0 # 사과 위치는 0으로 나타냄 #


L = int(input().strip())
changes = {}
for l in range(L):
    x, c = map(str, input().strip().split(' ')) # 정수 x, 문자 c #
    x = int(x)
    changes[x] = c


    
spent_time = 0
while True:
    spent_time += 1
    ret = snake._move_one_step()
    if ret == False:
        break
    if spent_time in changes:
        c = changes[spent_time]
        snake._change_dir(c)



print(spent_time)