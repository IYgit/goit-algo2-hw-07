import matplotlib.pyplot as plt
import timeit
from functools import lru_cache

import matplotlib
matplotlib.use('Agg')


# ---------- Fibonacci with LRU Cache ----------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# ---------- Splay Tree Implementation ----------
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if key == self.root.key:
            self.root.value = value
            return
        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def get(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

# ---------- Fibonacci with Splay Tree ----------
def fibonacci_splay(n, cache):
    if n <= 1:
        return n
    cached = cache.get(n)
    if cached is not None:
        return cached
    result = fibonacci_splay(n - 1, cache) + fibonacci_splay(n - 2, cache)
    cache.insert(n, result)
    return result

# ---------- Benchmark ----------
ns = list(range(0, 1000, 50))
lru_times = []
splay_times = []

for n in ns:
    # Time for LRU
    fibonacci_lru.cache_clear()
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    lru_times.append(lru_time)

    # Time for Splay Tree
    splay_cache = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_cache), number=1)
    splay_times.append(splay_time)

# ---------- Plot ----------
plt.figure(figsize=(12, 6))
plt.plot(ns, lru_times, label='LRU Cache', marker='o')
plt.plot(ns, splay_times, label='Splay Tree', marker='s')
plt.xlabel('n (Fibonacci Index)')
plt.ylabel('Execution Time (seconds)')
plt.title('Fibonacci Performance: LRU Cache vs Splay Tree')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("assets/fibonacci_comparison.png")

# Виведення таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<22}{'Splay Tree Time (s)':<22}")
print("-" * 54)
for n, lru, splay in zip(ns, lru_times, splay_times):
    print(f"{n:<10}{lru:<22.8f}{splay:<22.8f}")
