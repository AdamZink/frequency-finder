import numpy as np


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


def get_frequency_tuple_score(target, guess, axis, sign):
    assert target.shape == guess.shape
    assert abs(sign) == 1

    score = 0
    target_sums = np.sum(target, axis=axis)
    guess_sums = np.sum(guess, axis=axis)

    # create tuples
    target_tuples = get_ordered_tuples(target_sums)
    guess_tuples = get_ordered_tuples(guess_sums)

    for i in range(len(target_tuples)):
        # tuples like (bucket value, index of sum)
        if guess_tuples[i][0] > 0 and target_tuples[i][0] > 0 \
                and (sign * guess_tuples[i][1]) > (sign * target_tuples[i][1]):
            score += (sign * guess_tuples[i][1]) - (sign * target_tuples[i][1])

    return score


def get_frequency_tuple_too_low_score(target, guess, axis):
    return get_frequency_tuple_score(target, guess, axis, -1)


def get_frequency_tuple_too_high_score(target, guess, axis):
    return get_frequency_tuple_score(target, guess, axis, 1)


def get_frequency_value_scores(target, guess):
    # return a 2-part score:
    # the "too low" score indicates quantity of buckets to adjust frequencies higher
    # the "too high" score indicates quantity of buckets to adjust frequencies lower
    return get_frequency_tuple_too_low_score(target, guess, axis=1), \
           get_frequency_tuple_too_high_score(target, guess, axis=1)
