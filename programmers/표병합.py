parent = [[]]
value = [[]]
R = 51
C = 51

def get_parent(r, c):
    if [r, c] == parent[r][c]:
        return [r, c]
    parent[r][c] = get_parent(*parent[r][c])
    return parent[r][c]

def _update(toks):
    global parent, value, R, C
    if len(toks) == 4: # UPDATE r c value #
        r, c, val = toks[1:]
        r, c = int(r), int(c)
        p = get_parent(r, c) # 병합 상태가 아니면 [r,c]일 것이고, 맞다면 parent 좌표일 것임 # 
        # print("p ", p)
        # print("value ", val)
        value[p[0]][p[1]] = val
        
    elif len(toks) == 3: # UPDATE value1 value2 #
        value1, value2 = toks[1:]
        for r in range(R):
            for c in range(C):
                if value[r][c] == value1:
                    value[r][c] = value2
    else:
        raise ValueError(f"Invalid length : {toks}")



def _merge(toks):
    r1, c1, r2, c2 = map(int, toks[1:])
    p1 = get_parent(r1, c1)
    p2 = get_parent(r2, c2)
    if value[p1[0]][p1[1]] == "": # (r1, c1)이 값이 없는 칸인 경우에 #
        parent[p1[0]][p1[1]] = p2
    else:
        parent[p2[0]][p2[1]] = p1

def match_parent():
    for r in range(R):
        for c in range(C):
            get_parent(r, c)
            
def _unmerge(toks):
    global parent, value
    r, c = map(int, toks[1:])
    p = get_parent(r, c)
    val = value[p[0]][p[1]]
    
    match_parent()
    
    for _r in range(R):
        for _c in range(C):
            _p = get_parent(_r, _c)
            if _p == p: # 동일한 부모의 하위에 있는 노드들인 경우 자기자신을 parent node로 변경 #
                parent[_r][_c] = [_r, _c]
                value[_r][_c] = "" # 초기 상태, 즉 비어있을 때로 바뀌어야 한다. #
    value[r][c] = val
 

def _print(toks):
    r, c = map(int, toks[1:])
    p = get_parent(r,c)
    val = value[p[0]][p[1]]
    if val == "":
        return "EMPTY"
    return val

def solution(commands):
    answer = []
    global parent, value
    parent = [[[0,0] for _ in range(C)] for _ in range(R)]
    value = [["" for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            parent[r][c] = [r,c]
            
    
    for cmd in commands:
        cmd_toks = cmd.split(' ')
        # print(cmd_toks)
        if cmd_toks[0] == "UPDATE":
            _update(cmd_toks)
        elif cmd_toks[0] == "MERGE":
            _merge(cmd_toks)
        elif cmd_toks[0] == "UNMERGE":
            _unmerge(cmd_toks)
        else:
            ans = _print(cmd_toks)
            answer.append(ans)
    return answer

if __name__ == "__main__":
    commands = ["UPDATE 1 1 menu", "UPDATE 1 2 category", "UPDATE 2 1 bibimbap", "UPDATE 2 2 korean", "UPDATE 2 3 rice", "UPDATE 3 1 ramyeon", "UPDATE 3 2 korean", "UPDATE 3 3 noodle", "UPDATE 3 4 instant", "UPDATE 4 1 pasta", "UPDATE 4 2 italian", "UPDATE 4 3 noodle", "MERGE 1 2 1 3", "MERGE 1 3 1 4", "UPDATE korean hansik", "UPDATE 1 3 group", "UNMERGE 1 4", "PRINT 1 3", "PRINT 1 4"]
    print(solution(commands))