import numpy as np


def get_mask_value(sum):
    return 1 if sum > 0 else 0


def get_frequency_count_score(target, guess):
    assert target.shape == guess.shape

    # i.e. rows like [0, 1, 1, 0] get sum of 2
    target_sums = np.sum(target, axis=1)
    guess_sums = np.sum(guess, axis=1)

    # i.e. sum of 2 gets mapped to 1 (to indicate presence of frequency in any window)
    target_masked_sums = np.vectorize(get_mask_value)(target_sums)
    guess_masked_sums = np.vectorize(get_mask_value)(guess_sums)

    return np.sum(target_masked_sums) - np.sum(guess_masked_sums)
