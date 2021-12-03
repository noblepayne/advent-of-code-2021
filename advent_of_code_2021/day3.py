import collections
import functools

testdata = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def parse_input(input: str) -> list:
    return [list(s) for s in input.strip().splitlines()]


def transpose(data):
    return list(map(list, zip(*data)))


def count_row(row):
    return collections.Counter(row).most_common(2)


def count_digits(transposed_data):
    return list(map(count_row, transposed_data))


def digits_to_int(digits):
    return int("".join(digits), 2)


def γ(data):
    return digits_to_int([d[0][0] for d in data])


def ϵ(data):
    return digits_to_int([d[-1][0] for d in data])


def part1(input):
    data = parse_input(input)
    transposed_data = transpose(data)
    counted_data = count_digits(transposed_data)
    gamma = γ(counted_data)
    epsilon = ϵ(counted_data)
    return gamma * epsilon


#####################################################################################


def most_common_digit_per_col(counted_data, row):
    mc = counted_data[row][0]
    lc = counted_data[row][-1]
    return "1" if mc[1] == lc[1] else mc[0]


def least_common_digit_per_col(counted_data, row):
    mc = counted_data[row][0]
    lc = counted_data[row][-1]
    return "0" if mc[1] == lc[1] else lc[0]


def filter_numbers_by_digit_in_column(data, col, digit):
    return [row for row in data if row[col] == digit]


def _compute_gas(data, counted_data, common_digit_function):
    for col in range(len(counted_data)):
        digit = common_digit_function(counted_data, col)
        filtered = filter_numbers_by_digit_in_column(data, col, digit)
        if len(filtered) == 1:
            return digits_to_int(filtered[0])
        else:
            data = filtered
            counted_data = count_digits(transpose(data))


O2 = functools.partial(_compute_gas, common_digit_function=most_common_digit_per_col)
CO2 = functools.partial(_compute_gas, common_digit_function=least_common_digit_per_col)


def part2(input):
    data = parse_input(input)
    transposed_data = transpose(data)
    counted_data = count_digits(transposed_data)
    o2 = O2(data, counted_data)
    assert o2 is not None
    co2 = CO2(data, counted_data)
    assert co2 is not None
    return o2 * co2
