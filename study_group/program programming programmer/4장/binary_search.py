

def binary_search(target, data):
    start = 0 			# 맨 처음 위치
    end = len(data) - 1 	# 맨 마지막 위치
    exec_count = 0
    while start <= end:
        mid = (start + end) // 2 # 중간값

        if data[mid] == target:
            return mid 		# target 위치 반환

        elif data[mid] > target: # target이 작으면 왼쪽을 더 탐색
            exec_count+=1
            end = mid - 1

        else:                    # target이 크면 오른쪽을 더 탐색
            exec_count+=1

            start = mid + 1
    print("실행횟수",exec_count)
    return

data=[6,43,12,2,3,1,5,10,15,18,25,17,16,19,20,21,22,23,24,25,26,27,30,31,32,33,34,35,36,37,38,39]
data.sort()
print(data)
a= binary_search(1, data)  # 32개 배열 실행횟수 4

for i in range(64,128+32):
    data.append(i)

data.sort()
print(data)
b= binary_search(1, data) # 128개 배열 실행횟수 6