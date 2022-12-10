import numpy as np


def read_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def delta(list):
    arr = np.array(list)
    return arr[1:] - arr[:-1]


def problem1(list):
    d = delta(list)
    bigger = d > 0
    return sum(bigger)


def window(list, n=3):
    arr = np.array(list)
    return [arr[i : len(list) - (n - i - 1)] for i in range(n)]
    return [arr[i : -(n - i - 1)] for i in range(n)]


def problem2(list):
    w = window(list, 3)
    s = sum(w)
    d = delta(s)
    return sum(d > 0)


test_input = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]


input_raw = read_file("2021/data/day01/input.txt")
input_num = [int(x) for x in input_raw]

assert problem1(test_input) == 7

print(f"Problem 1: {problem1(input_num)}")

assert problem2(test_input) == 5

print(f"Problem 2: {problem2(input_num)}")
