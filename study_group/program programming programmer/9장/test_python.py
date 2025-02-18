from collections import defaultdict


def goodsearch(n, t, x=[1, 2, 3, 4, 5]):
    l = 0
    u = n - 1
    while (l <= u):
        m = (l + u) // 2
        # printf(" %d %d %d\n" , l, m, u)
        # print(f"{l} {m} {u}")
        if (x[m] < t):
            l = m + 1
        elif (x[m] > t):
            u = m - 1
        else:
            return m

    return -1


def binary_search_unrolled(x, t):
    l = -1  # 시작점 (배열 밖)
    n = len(x)

    # 큰 단계부터 차례로 점프
    if l + 512 < n and x[l + 512] < t: l += 512
    if l + 256 < n and x[l + 256] < t: l += 256
    if l + 128 < n and x[l + 128] < t: l += 128
    if l + 64 < n and x[l + 64] < t: l += 64
    if l + 32 < n and x[l + 32] < t: l += 32
    if l + 16 < n and x[l + 16] < t: l += 16
    if l + 8 < n and x[l + 8] < t: l += 8
    if l + 4 < n and x[l + 4] < t: l += 4
    if l + 2 < n and x[l + 2] < t: l += 2
    if l + 1 < n and x[l + 1] < t: l += 1

    # 최종 위치 확인
    return l + 1 if (l + 1 < n and x[l + 1] == t) else -1

def generate_hashed_dict(arr:list):
    hashed_dict = dict()
    for idx,val in enumerate(arr):
        hashed_dict[val]=idx
    return hashed_dict
def find_from_hashed_dict(hashed_dict, target):
    if target in hashed_dict:
        return hashed_dict[target]
    return None



# 테스트
arr = [i for i in range(1000)]  # 정렬된 리스트 (0~999)

# target = 789
# result = binary_search_unrolled(arr, target)
# print(f"Index of {target}: {result}")  # 예상 출력: Index of 789: 789
