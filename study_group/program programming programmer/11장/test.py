def reverse_sentinel_qsort(x, l, u):
    t = x[l]
    m = i = u + 1
    while True:
        while x[i - 1] < t:
            i -= 1
        m -= 1
        x[m], x[i] = x[i], x[m]
        if i == l:
            break

if __name__ == '__main__':

    a = 0.1 + 0.2
    b = 0.3

    print(a == b)  # False 출력
    print(a)  # 0.30000000000000004 출력

    arr=[2,1,4]
    val = reverse_sentinel_qsort(arr, 0,len(arr))