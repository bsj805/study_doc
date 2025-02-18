import random
import time

# 🟢 튜닝된 이진 탐색 (Unrolled Binary Search)
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

# 🔵 해시 딕셔너리 생성
def generate_hashed_dict(arr):
    return {val: idx for idx, val in enumerate(arr)}

# 🔵 해시 딕셔너리 탐색
def find_from_hashed_dict(hashed_dict, target):
    return hashed_dict.get(target, None)

# 🏆 성능 비교 함수
def benchmark_search(N, arr):
    targets = random.sample(arr, N)  # 🔹 N개의 랜덤한 탐색 대상 선택

    # 🟢 이진 탐색 테스트
    start = time.perf_counter()
    for t in targets:
        binary_search_unrolled(arr, t)
    end = time.perf_counter()
    binary_search_time = (end - start) / N * 1e6  # 평균 검색 시간 (μs)

    # 🔵 해시 탐색 테스트
    start = time.perf_counter()
    hashed_dict = generate_hashed_dict(arr)

    for t in targets:
        find_from_hashed_dict(hashed_dict, t)
    end = time.perf_counter()
    hashed_search_time = (end - start) / N * 1e6  # 평균 검색 시간 (μs)

    # 🔥 결과 출력
    print(f"🔹 Number of Searches: {N}")
    print(f"🟢 Binary Search Time: {binary_search_time:.2f} μs per search")
    print(f"🔵 Hashed Search Time: {hashed_search_time:.2f} μs per search")
    print(f"⚡ Speedup (Hash vs Binary): {binary_search_time / hashed_search_time:.2f}x\n")

# 🛠️ 테스트 실행
arr = list(range(1000))  # 🔹 정렬된 1000개 리스트
benchmark_search(100, arr)  # 🔥 100개 테스트
benchmark_search(500, arr)  # 🔥 500개 테스트
benchmark_search(1000, arr)  # 🔥 1000개 테스트
