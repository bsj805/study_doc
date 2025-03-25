import time
import random

class HeapArr(object):
    """맨위가 제일 큰 max heap"""
    def __init__(self):
        self.heap_arr = [None] # heap은 0번째요소를 채워놓고 시작 1번부터해야 left는 idx*2 , right는 idx*2+1 이 된다.

    def get_left_idx(self, idx):
        return idx*2
    def get_left(self, idx):
        if len(self.heap_arr) <= idx*2:
            return None
        return self.heap_arr[idx*2]
    def get_right_idx(self, idx):
        return idx * 2 +1
    def get_right(self, idx):
        if len(self.heap_arr) <= idx * 2+1:
            return None
        return self.heap_arr[idx * 2+1]
    def get_parent_idx(self, idx):
        return idx//2
    def get_parent(self, idx):
        if idx//2 ==0:
            return None
        return self.heap_arr[idx // 2]

    def swap(self, idx1, idx2):
        value = self.heap_arr[idx1]
        self.heap_arr[idx1] = self.heap_arr[idx2]
        self.heap_arr[idx2] = value
    def sift_up(self, idx):
        """위 노드와 loop invariant 맞추기"""
        cur_node = self.heap_arr[idx]
        parent_node = self.get_parent(idx)
        if not parent_node:
            return
        if cur_node > parent_node:
            self.swap(idx, self.get_parent_idx(idx))
            return self.sift_up(self.get_parent_idx(idx))
    def sift_down(self,idx):
        """아래 노드와 loop invariant 맞추기"""
        cur_node = self.heap_arr[idx]
        left_node = self.get_left(idx)
        right_node = self.get_right(idx)
        swap_index = None
        if not left_node and not right_node:
            return
        if not right_node:
            swap_index = self.get_left_idx(idx)

        elif left_node > right_node:
            swap_index = self.get_left_idx(idx)
        else:
            swap_index = self.get_right_idx(idx)

        if cur_node < self.heap_arr[swap_index]:
            self.swap(idx, swap_index)
            return self.sift_down(swap_index)

    def insert(self, value):
        """새로운 요소 삽입"""
        self.heap_arr.append(value)  # 배열 끝에 추가
        self.sift_up(len(self.heap_arr) - 1)  # 위로 정렬

    def pop(self):
        """최대값 제거 후 반환"""
        if len(self.heap_arr) == 1:
            return None  # 빈 힙

        if len(self.heap_arr) == 2:
            return self.heap_arr.pop()  # 요소가 하나뿐이라면 바로 반환

        self.swap(1, len(self.heap_arr) - 1)  # 루트와 마지막 요소 교환
        max_value = self.heap_arr.pop()  # 최대값 제거
        self.sift_down(1)  # 아래로 정렬
        return max_value


if __name__ == '__main__':
    heap = HeapArr()
    heap.insert(10)
    heap.insert(20)
    heap.insert(5)
    heap.insert(30)

    print(heap.pop())  # 30
    print(heap.pop())  # 20
    print(heap.pop())  # 10
    print(heap.pop())  # 5
    print(heap.pop())  # None (Heap is empty)


    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)


    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)


    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result


    def insertion_sort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr


    def radix_sort(arr):
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            counting_sort(arr, exp)
            exp *= 10


    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        for i in range(n):
            arr[i] = output[i]


    random.seed(42)
    arr = [random.randint(1, 100000) for _ in range(10000)]

    arr_heap = arr[:]
    heap = HeapArr()
    start = time.time()
    for num in arr_heap:
        heap.insert(num)
    sorted_heap = [heap.pop() for _ in range(len(arr_heap))][::-1]
    print("Heap Sort Time:", time.time() - start)


    start = time.time()
    arr_quick=[]
    for num in arr:
        arr_quick.append(num)
    quicksort(arr_quick)
    print("Quick Sort Time:", time.time() - start)


    start = time.time()
    arr_merge = []
    for num in arr:
        arr_merge.append(num)
    merge_sort(arr_merge)
    print("Merge Sort Time:", time.time() - start)


    start = time.time()
    arr_insertion = []
    for num in arr:
        arr_insertion.append(num)
    insertion_sort(arr_insertion)
    print("Insertion Sort Time:", time.time() - start)


    start = time.time()
    arr_radix = []
    for num in arr:
        arr_radix.append(num)
    radix_sort(arr_radix)
    print("Radix Sort Time:", time.time() - start)



