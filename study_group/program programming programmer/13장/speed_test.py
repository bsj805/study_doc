import time
import random


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def rinsert_list(p, t):
    if p is None or p.val > t:
        return ListNode(t, p)
    elif p.val < t:
        p.next = rinsert_list(p.next, t)
    return p


def insert_list(head, t):
    return rinsert_list(head, t)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rinsert_tree(p, t):
    if p is None:
        return TreeNode(t)
    elif p.val < t:
        p.right = rinsert_tree(p.right, t)
    elif p.val > t:
        p.left = rinsert_tree(p.left, t)
    return p


def insert_tree(root, t):
    return rinsert_tree(root, t)


def insert_bin(bins, maxval, bins_count, t):
    i = t // (1 + maxval // bins_count)
    bins[i] = rinsert_list(bins[i], t)


def benchmark_insert(n, maxval=100000, bins_count=100):
    # Test Linked List
    head = None
    start_time = time.time()
    for _ in range(n):
        head = insert_list(head, random.randint(0, maxval))
    list_time = time.time() - start_time

    # Test Binary Search Tree
    root = None
    start_time = time.time()
    for _ in range(n):
        root = insert_tree(root, random.randint(0, maxval))
    tree_time = time.time() - start_time

    # Test Bins
    bins = [None] * bins_count
    start_time = time.time()
    for _ in range(n):
        insert_bin(bins, maxval, bins_count, random.randint(0, maxval))
    bin_time = time.time() - start_time

    return {
        "Linked List": list_time,
        "Binary Tree": tree_time,
        "Bins": bin_time
    }


# Example Usage
# n = 1000  # Number of insertions
# results = benchmark_insert(n)
# print(results)

import random
import matplotlib.pyplot as plt
from collections import Counter

def floyd_random_selection(n, m):
    selected = set()
    for j in range(n - m + 1, n + 1):
        t = random.randint(1, j)
        if t in selected:
            selected.add(j)
        else:
            selected.add(t)
    return selected

def random_selection_builtin(n, m):
    return set(random.sample(range(1, n + 1), m))

# 실험 설정
n = 10000  # 전체 범위
m = 10    # 선택할 개수
trials = 100000

# 데이터 수집
counter_floyd = Counter()
counter_builtin = Counter()

for _ in range(trials):
    counter_floyd.update(floyd_random_selection(n, m))
    counter_builtin.update(random_selection_builtin(n, m))

# 그래프 그리기
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Floyd 알고리즘 결과
numbers_floyd, frequencies_floyd = zip(*sorted(counter_floyd.items()))
axes[0].bar(numbers_floyd, [f / trials for f in frequencies_floyd], width=1.0, color='blue', alpha=0.7)
axes[0].set_title("Floyd’s Algorithm")
axes[0].set_xlabel("Number")
axes[0].set_ylabel("Selection Probability")

# 내장 함수 결과
numbers_builtin, frequencies_builtin = zip(*sorted(counter_builtin.items()))
axes[1].bar(numbers_builtin, [f / trials for f in frequencies_builtin], width=1.0, color='red', alpha=0.7)
axes[1].set_title("random.sample()")
axes[1].set_xlabel("Number")

# 그래프 출력
plt.tight_layout()
plt.show()