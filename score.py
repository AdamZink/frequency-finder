import numpy as np


def get_signal_diff_score(signal_1, signal_2):
    diffs_1 = np.ediff1d(signal_1, to_begin=signal_1[0])
    diffs_2 = np.ediff1d(signal_2, to_begin=signal_2[0])
    subtracted = np.absolute(diffs_1 - diffs_2)
    return np.sum(subtracted) / diffs_1.shape[0]


def get_ordered_tuples(sums):
    # map of sum value -> index
    sum_map = {}
    for i in range(len(sums)):
        if sums[i] not in sum_map:
            sum_map[sums[i]] = []
        sum_map[sums[i]].append(i)

    tuples = []
    for value in sorted(list(sum_map), reverse=True):
        tuple_list = [(value, index) for index in sum_map[value]]
        tuples += tuple_list

    return tuples


def get_alternate_axis_sum_score(bucketed_1, bucketed_2, axis):
    score = 0
    frequency_sums_1 = np.sum(bucketed_1, axis=axis)
    frequency_sums_2 = np.sum(bucketed_2, axis=axis)

    # create tuples
    tuples_1 = get_ordered_tuples(frequency_sums_1)
    tuples_2 = get_ordered_tuples(frequency_sums_2)

    # assume lists are the same length (they will be if proper params were provided)
    tuple_len = len(tuples_1)
    for i in range(tuple_len):
        # tuples like (bucket value, index of sum)
        # TODO alternatively, refactor to use zip syntax?
        # value distribution penalty
        score += abs(tuples_1[i][0] - tuples_2[i][0])
        # axis position penalty (i.e. replaces (3) energy distribution penalty)
        score += abs(tuples_1[i][1] - tuples_2[i][1])

    return score


def get_alternate_frequency_sum_score(bucketed_1, bucketed_2):
    # want frequencies which are much higher/lower to have a higher score
    return get_alternate_axis_sum_score(bucketed_1, bucketed_2, axis=1)


def get_alternate_time_sum_score(bucketed_1, bucketed_2):
    # want frequencies occurring much earlier/later to have a higher score
    return get_alternate_axis_sum_score(bucketed_1, bucketed_2, axis=0)
