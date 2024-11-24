import copy
import time


def iterate(arr, n, i):
    """
    n개짜리 변수 있는 array 에 대해서 i만큼 회전한다면?
    :param arr:
    :param n:
    :param i:
    :return:
    """
    arr[:i].reverse() #

def juggling(arr, n, i):
    touched_element = list([1]*n)
    while(any(touched_element)):
        prev_last=None
        juggle_idx = 0
        temp = arr[juggle_idx]

        for j in range(0, n):

            if juggle_idx+j+i >= n:

                arr[prev_last] = temp
                touched_element[prev_last] = 0
                break
            arr[juggle_idx+j] = arr[juggle_idx+j+i]
            touched_element[juggle_idx+j] = 0
            prev_last = juggle_idx+j+i
        juggle_idx+=1

    return arr

# Python Program to left rotate the array by d positions
# using Juggling Algorithm

import math

# Function to rotate array
def rotateArr(arr, n,d):

    # Handle the case where d > size of array
    d %= n

    # Calculate the number of cycles in the rotation
    cycles = math.gcd(n, d)

    # Process each cycle
    for i in range(cycles):

        # Start element of current cycle
        startEle = arr[i]

        # Start index of current cycle
        currIdx = i

        # Rotate elements till we reach the start of cycle
        while True:
            nextIdx = (currIdx + d) % n

            if nextIdx == i:
                break

            # Update the next index with the current element
            arr[currIdx] = arr[nextIdx]
            currIdx = nextIdx

        # Copy the start element of current cycle at the last
        # index of the cycle
        arr[currIdx] = startEle
    return arr
# Python Program to reverse an array using temporary array

# function to reverse an array
def reverseArray(arr, n):
    n = len(arr)

    # Temporary array to store elements in reversed order
    temp = [0] * n

    # Copy elements from original array to temp in reverse order
    for i in range(n):
        temp[i] = arr[n - i - 1]

    # Copy elements back to original array
    for i in range(n):
        arr[i] = temp[i]

def reverse_upto_n(arr, left, right):
    # Reverse elements from the start up to index n-1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]  # Swap elements
        left += 1
        right -= 1
    return arr
def reverse(arr, n, i ):
    arr= reverse_upto_n(arr, 0, i-1)
    arr= reverse_upto_n(arr, i, n-1)
    arr= reverse_upto_n(arr, 0, n-1)
    return arr

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def test_reverse():
    arr = [1, 2, 3, 4, 5, 6,7,8,9,10,11,12]
    n=12
    d = 6

    for _ in range(10000000):
        reverse(arr, n, d)

@timing_decorator
def test_juggle():
    arr = [1, 2, 3, 4, 5, 6,7,8,9,10,11,12]
    n=12
    d = 6

    for _ in range(10000000):
        rotateArr(arr, n, d)

if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6,7,8,9,10,11,12]
    n=12
    d = 6

    # val = rotateArr(copy.copy(arr), n, d)
    # val2 = reverse(copy.copy(arr), n, d)

    test_reverse()
    test_juggle()