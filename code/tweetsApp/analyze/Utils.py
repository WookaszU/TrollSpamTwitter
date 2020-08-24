
def append_to_bin(value, bins_numbers_list, bins):
    pointer = 0
    epsilon = 0.00000000000000001
    while value - bins_numbers_list[pointer] > epsilon:
        pointer += 1

    bins[pointer] += 1

    return pointer


def filter_zero_values_from_end(input_list):
    pointer = len(input_list) - 1
    while input_list[pointer] == 0 and pointer > 0:
        pointer -= 1

    return input_list[0:pointer + 1]


def get_bins_x10(power):
    multiplier = 1
    tab = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    bins_ratios = [0]

    while bins_ratios[len(bins_ratios) - 1] <= 10**power:
        bins_ratios.extend([i * multiplier for i in tab])
        multiplier *= 10

    return bins_ratios
