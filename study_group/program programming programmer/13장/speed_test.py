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
n = 1000  # Number of insertions
results = benchmark_insert(n)
print(results)