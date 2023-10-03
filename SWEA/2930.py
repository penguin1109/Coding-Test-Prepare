class Heap:
  def __init__(self):
    self.heap = [-1] * 10**5
    self.length = 0
  
  def swap(self, a, b):
    temp = self.heap[a]
    self.heap[a] = self.heap[b]
    self.heap[b] = temp

  def push(self, x):
    cur_idx = self.length
    self.heap[cur_idx] = x
    while (cur_idx > 0):
      parent_idx = (cur_idx-1)//2
      if (self.heap[parent_idx] < x):
        self.swap(cur_idx, parent_idx)
      else:
        break
      cur_idx = parent_idx

    self.length += 1
  
  def pop(self):
    if self.length == 0:
      return -1
    last_ = self.heap[self.length-1]
    rm = self.heap[0]
    self.heap[0] = last_
    idx = 0
    self.length -= 1
    
    while True:
      parent = idx
      idx = (idx*2)+1
    
      if (idx >= self.length):
        break
      elif (idx + 1 == self.length):
        if (self.heap[parent] > self.heap[idx]):
          break
        self.swap(parent, idx)
        break
      else:
        if (self.heap[idx] < self.heap[idx+1]):
          idx += 1
        if (self.heap[parent] > self.heap[idx]):
          break
        self.swap(parent, idx)
    return rm

if __name__ == "__main__":
  T = int(input())
  for test_case in range(T):
    N = int(input()) ## 연산 수
    heap = Heap()
    answer = []
    for n in range(N):
      temp = input().split(' ')
      if (len(temp) == 2):
        x = int(temp[-1])
        heap.push(x)
      else:
        ret = heap.pop()
        answer.append(ret)
      print(heap.heap[:heap.length])
    print(f"#{test_case+1}", end=' ')
    for i in range(len(answer)):
        if i == len(answer)-1:
            print(f"{answer[i]}")
        else:
            print(f"{answer[i]}", end = ' ')
