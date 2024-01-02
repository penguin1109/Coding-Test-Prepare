def make_lines(rectangle):
    temp = []
    for (lx, ly, rx, ry) in rectangle:
        for x in [lx, rx]: # x축 기준으로 양 끝 변의 좌표에 대해서 #
            for y in range(ly, ry): # 모든 y축의 모서리들의 좌표의 중점. range() 특성상 ry는 포함 안되기 때문에 ry+1을 할필요 없음 #
                temp.append((x, y+0.5)) # 길이가 1인 선분의 중점을 입력으로 넣어준다. #
        for y in [ly, ry]:
            for x in range(lx, rx):
                temp.append((x+0.5, y))
    temp = list(set(temp))
    lines = set()
    for x, y in temp:
        valid = True
        for (lx, ly, rx, ry) in rectangle:
            if lx < x < rx and ly < y < ry:
                valid = False
                break
        if valid:
            lines.add((x, y))
    # print(lines)
    return lines
            
def is_line(x1, y1, x2, y2, rectangle):
    """(x1, y1)->(x2,y2)로 두점 사이를 이동하는 한 칸의 line이 <이동경로>인지 확인"""
    if (x1 == x2): # x좌표가 동일한, 즉 세로line인 경우 #
        found = False
        for (lx, ly, rx, ry) in rectangle:
            if (x1 == lx or x1 == rx): # x좌표가 사각형의 끝에 있으면 #
                if ly <= y1 <= ry and ly <= y2 <= ry:
                    found = True
        if found == False:
            return False
            
    elif (y1 == y2): # y좌표가 동일한, 즉 가로 line인 경우 #
        found = False
        for (lx, ly, rx, ry) in rectangle:
            if (y1 == ly or y1 == ry):
                if lx <= x1 <= rx and lx <= x2 <= rx:
                    found = True # 어떤 사각형의 모서리인 경우 #
        if found == False:
            return False
    return True


def move(x1, y1, x2, y2, lines):
    """(x1, y1)에서 (x2, y2)로 이동하기 위해서 매번 이동하면서 해당 길이 <이동 경로>가 맞는지 확인한다."""   
    from collections import deque
    q = deque([[0, x1, y1]]) # (이동거리, 시작 x, 시작 y)
    DX, DY = [-1, 1, 0, 0], [0, 0, -1, 1]
    
    while q:
        dist, x, y = q.popleft()
        if x == x2 and y == y2:
            return dist
        for dx, dy in zip(DX, DY):
            nx, ny = x + dx, y + dy
            if dy == 0:
                cx, cy = x + 0.5 * dx, y
            else:
                cx, cy = x, y + 0.5*dy
         
            if (cx, cy) in lines:
                lines.remove((cx, cy))
                q.append([dist+1, nx, ny])
            
        
    
    
    
def solution(rectangle, characterX:int, characterY:int, itemX:int, itemY:int):
    lines = make_lines(rectangle)
    answer = move(characterX, characterY, itemX, itemY, lines)
    return answer

if __name__ == "__main__":
    rectangle = [[1,1,7,4],[3,2,5,5],[4,3,6,9],[2,6,8,8]]
    characterX = 1
    characterY = 3
    itemX = 7
    itemY = 8
    
    answer = solution(rectangle, characterX, characterY, itemX, itemY)
    
    print(answer)