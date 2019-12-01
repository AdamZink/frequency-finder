import json
import numpy as np
from finder.fitness.frequency.count import *
from signal_util import *
from data_util import *


def remove_frequencies(frequencies, count):
    for _ in range(count):
        frequencies.pop()


target_frequencies = get_random_frequency_array(random.randint(1, 10))
print('Target count: {}'.format(len(target_frequencies)))

guess_frequencies = get_random_frequency_array(random.randint(1, 10))
print('Initial guess count: {}'.format(len(guess_frequencies)))

best_score = None
max_rounds = 10
current_round = 1

NUM_WINDOWS = 1


def debug_bucketed(bucketed):
    print('\nDebug output for bucketed data >>>')
    print(bucketed.shape)
    for i in range(bucketed.shape[0]):
        if np.sum(bucketed[i]) > 0:
            print("row index {}: {}".format(i, bucketed[i]))
    print('<<<\n')


target_signal = get_signal_from_obj(target_frequencies)
target_bucketed = get_bucketed_signal(target_signal, NUM_WINDOWS)
debug_bucketed(target_bucketed)

while current_round <= max_rounds:

    guess_signal = get_signal_from_obj(guess_frequencies)
    guess_bucketed = get_bucketed_signal(guess_signal, NUM_WINDOWS)
    debug_bucketed(guess_bucketed)

    score = get_frequency_count_score(target_bucketed, guess_bucketed)
    print(score)

    if score > 0:
        append_random_frequencies(guess_frequencies, score)
    elif score < 0 and len(guess_frequencies) > 1:
        if len(guess_frequencies) + score > 0:
            remove_frequencies(guess_frequencies, -score)
        else:
            remove_frequencies(guess_frequencies, 1)
    else:
        break

    print(json.dumps(guess_frequencies, indent=2))

    current_round += 1

print('done')
print(json.dumps(target_frequencies, indent=2))
print('vs')
print(json.dumps(guess_frequencies, indent=2))
print('Final guess: number of frequencies = {}'.format(len(guess_frequencies)))
print('Expected target count: {}'.format(len(target_frequencies)))
