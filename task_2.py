import time
import random
from functools import lru_cache

# ---------- Варіант 1: Fibonacci з LRU-кешем ----------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# ---------- Варіант 2: Fibonacci з Splay Tree-кешем ----------
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTreeCache:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
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
                root = self._right_rotate(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            return root if root.right is None else self._left_rotate(root)

    def get(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def put(self, key, value):
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

# ---------- Fibonacci з Splay Tree кешем ----------
class FibonacciSplay:
    def __init__(self):
        self.cache = SplayTreeCache()

    def compute(self, n):
        cached = self.cache.get(n)
        if cached is not None:
            return cached
        if n <= 1:
            self.cache.put(n, n)
            return n
        val = self.compute(n - 1) + self.compute(n - 2)
        self.cache.put(n, val)
        return val

# ---------- Тестування і порівняння ----------
def benchmark(func, calls):
    start = time.time()
    for n in calls:
        func(n)
    return time.time() - start

if __name__ == "__main__":
    # Генеруємо список випадкових n у діапазоні [10, 30]
    test_calls = [random.randint(10, 30) for _ in range(500)]

    # LRU
    fibonacci_lru.cache_clear()  # обнуляємо кеш перед тестом
    t1 = benchmark(fibonacci_lru, test_calls)
    print(f"Час виконання з LRU-кешем: {t1:.4f} секунд")

    # Splay
    fib_splay = FibonacciSplay()
    t2 = benchmark(fib_splay.compute, test_calls)
    print(f"Час виконання з Splay Tree: {t2:.4f} секунд")
