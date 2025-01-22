import random


def max_subarray_sum(arr):
    """
    배열에서 부분합의 최대값을 찾는 함수

    Parameters:
        arr (list): 정수 배열

    Returns:
        int: 부분합의 최대값
    """
    # 배열이 비었을 경우 0 반환
    if not arr:
        return 0

    # 초기값 설정
    max_sum = arr[0]  # 전체 최대 부분합
    current_sum = arr[0]  # 현재 부분합

    # 배열 순회
    for num in arr[1:]:
        # 현재 부분합을 업데이트
        current_sum = max(num, current_sum + num)

        # 전체 최대값 갱신
        max_sum = max(max_sum, current_sum)

    return max_sum

def generate_random_array():
    """
    [-1, 1] 사이에서 균일한 랜덤 값 5개를 선택하여 배열을 반환

    Returns:
        list: 랜덤 값 배열
    """
    return [random.uniform(-1, 1) for _ in range(5)]


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    random_sum_array = list()
    N=10000
    for i in range(N):
        arr=generate_random_array()
        val = max_subarray_sum(arr)
        random_sum_array.append(val)

    plt.figure(figsize=(8, 5))
    plt.hist(random_sum_array, bins=100, color='skyblue', edgecolor='black', alpha=0.7)  # bins: 구간의 개수
    plt.title("Histogram of Array Values", fontsize=16)
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(alpha=0.6, linestyle='--')
    plt.show()
    print(sum(random_sum_array)/len(random_sum_array))