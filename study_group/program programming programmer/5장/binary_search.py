import random
import time


def badsearch(n,t,x=[1,2,3,4,5]):
    l = 0
    u = n-1
    while (l <= u):
        m = (l + u) // 2
        # printf(" %d %d %d\n" , l, m, u)
        # print(f"{l} {m} {u}")
        if (x[m] < t):
            l = m
        elif (x[m] > t):
            u = m
        else:
            return m

    return -1

def goodsearch(n,t,x=[1,2,3,4,5]):
    l = 0
    u = n-1
    while (l <= u):
        m = (l + u) // 2
        # printf(" %d %d %d\n" , l, m, u)
        # print(f"{l} {m} {u}")
        if (x[m] < t):
            l = m+1
        elif (x[m] > t):
            u = m-1
        else:
            return m

    return -1

def validation_scaffold(numtests, arr_size,algnum):
    # Start timer
    starttime = time.time()
    x = list()
    for i in range(arr_size):
        x.append(i)
    n=len(x)

    for testnum in range(numtests):
        for i in range(arr_size):
            if algnum == 1:
                assert badsearch(arr_size,i,x) == i
            elif algnum == 2:
                assert goodsearch(arr_size,i,x) == i
            else:
                print("Invalid algorithm number!")
                return

    # Calculate elapsed time
    clicks = time.time() - starttime

    # Print results
    print(f"Algorithm: {algnum}, Array size: {n}, Number of tests: {numtests}, Time taken: {clicks:.6f} seconds")

def random_validation_scaffold(numtests, arr_size,algnum):
    # Start timer

    x = list()
    for i in range(arr_size):
        x.append(i)
    n=len(x)
    indicies = list(range(arr_size))
    random.shuffle(indicies)
    starttime = time.time()
    for testnum in range(numtests):

        for i in indicies:
            if algnum == 1:
                assert badsearch(arr_size,i,x) == i
            elif algnum == 2:
                assert goodsearch(arr_size,i,x) == i
            else:
                print("Invalid algorithm number!")
                return

    # Calculate elapsed time
    clicks = time.time() - starttime

    # Print results
    print(f"Algorithm: {algnum}, Array size: {n}, Number of tests: {numtests}, Time taken: {clicks:.6f} seconds")

print("random 안하고 캐시타게 한거")
arr_size=1000000
validation_scaffold(10,arr_size,2)
validation_scaffold(10,arr_size,2)
# validation_scaffold(10,arr_size,2)
# validation_scaffold(10,arr_size,2)
# validation_scaffold(10,arr_size,2)
print("-------------------------")
print("random 하게 해서 캐시 못타게 한거")
random_validation_scaffold(10,arr_size,2)
random_validation_scaffold(10,arr_size,2)
# random_validation_scaffold(10,arr_size,2)
# random_validation_scaffold(10,arr_size,2)
# random_validation_scaffold(10,arr_size,2)
print("-------------------------")

# x=[1,2,3,4,5]
# n=len(x)
# badsearch(n,1)
# # badsearch(n,5) # 무한루프 3, 3, 4
# # print("result",badsearch(n,1), badsearch(n,3), badsearch(n,5))
#
# print("result",goodsearch(n,1), goodsearch(n,3), goodsearch(n,5))
#
# x=[1,3,2,5,4]
#
# print("bad result",goodsearch(n,1), goodsearch(n,3), goodsearch(n,5))