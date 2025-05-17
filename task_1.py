from collections import OrderedDict
import random
import time

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, index):
        """Видаляє всі діапазони, які містять змінений індекс."""
        keys_to_remove = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]

class RangeQueryProcessor:
    def __init__(self, array, cache_capacity=1000):
        self.array = array
        self.cache = LRUCache(cache_capacity)

    def range_sum(self, L, R):
        key = (L, R)
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        # Обчислюємо суму
        total = sum(self.array[L:R+1])
        self.cache.put(key, total)
        return total

    def update(self, index, value):
        self.array[index] = value
        self.cache.invalidate(index)


# ---------- TESTS ----------
# 1. Генеруємо масив на 100_000 випадкових елементів
N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]

# 2. Генеруємо 50_000 випадкових запитів
# Припустимо, що 80% запитів — це повтори кількох популярних діапазонів
popular_ranges = [(10, 500), (1000, 2000), (50000, 70000)]

queries = []
for _ in range(50000):
    if random.random() < 0.8:
        queries.append(('Range', *random.choice(popular_ranges)))
    else:
        L = random.randint(0, N - 1000)
        R = L + random.randint(0, 1000)
        queries.append(('Range', L, R))


# ---------- Без кешу ----------
array_no_cache = array.copy()

start_time = time.time()

for query in queries:
    if query[0] == "Range":
        _, L, R = query
        _ = sum(array_no_cache[L:R+1])
    else:
        _, index, value = query
        array_no_cache[index] = value

no_cache_time = time.time() - start_time

# ---------- З кешем ----------
array_with_cache = array.copy()
processor = RangeQueryProcessor(array_with_cache, cache_capacity=1000)

start_time = time.time()

for query in queries:
    if query[0] == "Range":
        _, L, R = query
        _ = processor.range_sum(L, R)
    else:
        _, index, value = query
        processor.update(index, value)

with_cache_time = time.time() - start_time

# ---------- Результати ----------
print(f"Час виконання без кешу: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {with_cache_time:.2f} секунд")

