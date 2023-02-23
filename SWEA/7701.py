ret_arr = [[]for _ in range(20005)] ## 추가적인 공간에 저장해 주어야 한다.
def check_alphabetic_order(a, b):
  arr = [a,b]
  
  if (sorted(arr) == arr):
    return True
  return False

def merge_sort(arr, start, end):
  if (start < end):
    mid = (end+ start)//2
    merge_sort(arr, start, mid)
    merge_sort(arr, mid+1, end)
    merge(arr, start, mid, end)
    # print(ret_arr)
  return ret_arr
  

def merge(arr, start, mid, end):
  i = start
  j = mid+1
  k = end

  ret_idx = start
  while (i <= mid and j <= end):
    if (len(arr[i]) < len(arr[j])):
      ret_arr[ret_idx] = arr[i]
      ret_idx+=1;i+=1;
    elif (len(arr[i]) > len(arr[j])):
      ret_arr[ret_idx] = arr[j]
      ret_idx+=1;j+=1;
    else:
      if (check_alphabetic_order(arr[i], arr[j]) == True):
        ret_arr[ret_idx] = arr[i]
        i+= 1;ret_idx += 1;
      else:
        ret_arr[ret_idx] = arr[j]
        j +=1;ret_idx+=1;
  if (i > mid):
    for p in range(j, end+1):
      ret_arr[ret_idx] = arr[p]
      ret_idx+=1
  else:
    for p in range(i, mid+1):
      ret_arr[ret_idx] = arr[p]
      ret_idx += 1
  for i in range(start, end+1):
    arr[i] = ret_arr[i]
  return 

if __name__ == "__main__":
  T = int(input())
  MAXN = 20005
  for test_case in range(T):
    N = int(input())
    names = []
    for n in range(N):
      names.append(input())
      ## 이름 정렬할 때에 우선은 길이가 짧은 순으로 앞에 두고, 같은 길이면 사전순으로 앞에 정렬한다.
      # names[n] = [len(name), name]
    names.sort() # 알파벳 순으로 정렬
    names = list(set(names)) # 중복 제와
    ret_arr = merge_sort(names, 0, len(names)-1)
    print(f"#{test_case+1}")
    for n in range(len(names)):
      print(ret_arr[n])
    for n in range(len(names)):
        ret_arr[n] = 0
