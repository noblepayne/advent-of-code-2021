import collections
import itertools
import functools
import operator

td = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def count_increases(data: list) -> int:
    last = None
    increases = 0
    for x in data:
        if last is not None:
            if x > last:
                increases += 1
        last = x
    return increases


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def count_increases_again(data):
    return len([window for window in sliding_window(data, 2) if window[1] > window[0]])


def part1(data):
    return count_increases(data)


def count_sliding_increases(n: int, data: list):
    finished_buckets = []
    buckets = collections.deque([] for _ in range(n))

    for x in data:
        for b in buckets:
            b.append(x)
            if len(b) == 1:
                break

        if len(buckets[0]) == n:
            finished_buckets.append(buckets.popleft())
            buckets.append([])

    return finished_buckets


def part2(n, data):
    buckets = count_sliding_increases(n, data)
    sums = [functools.reduce(operator.add, b) for b in buckets]
    return count_increases(sums)
