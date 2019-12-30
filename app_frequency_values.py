from signal_util import *
from data_util import *
import json
from finder.fitness.frequency.values import *
import copy


# TODO combine with app_count.py logic to converge to correct count and value of frequencies

num_frequencies = 3

target_frequencies = get_random_frequency_array(num_frequencies)
print('Target frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))

guess_frequencies = get_random_frequency_array(num_frequencies)
print('Initial guesses:\n{}'.format(json.dumps(guess_frequencies, indent=2)))

max_rounds = 250
current_round = 1

NUM_WINDOWS = 1


def debug_bucketed(bucketed):
    print('\nDebug output for bucketed data >>>')
    print(bucketed.shape)
    for i in range(bucketed.shape[0]):
        if np.sum(bucketed[i]) > 0:
            print("row index {}: {}".format(i, bucketed[i]))
    print('<<<\n')


def get_normalized_probability_list(qty):
    probability_list = []
    for _ in range(qty):
        probability_list.append(random.random())
    sum_of_probabilities = sum(probability_list) * 1.5
    return [p / sum_of_probabilities for p in probability_list]


target_signal = get_signal_from_obj(target_frequencies)
target_bucketed = get_bucketed_signal(target_signal, NUM_WINDOWS)
debug_bucketed(target_bucketed)

last_score = None

while current_round <= max_rounds:
    guess_signal = get_signal_from_obj(guess_frequencies)
    guess_bucketed = get_bucketed_signal(guess_signal, NUM_WINDOWS)
    debug_bucketed(guess_bucketed)

    too_low_score, too_high_score = get_frequency_value_scores(target_bucketed, guess_bucketed)
    print(too_low_score)
    print(too_high_score)

    last_score = abs(too_low_score) + abs(too_high_score)

    if last_score == 0:
        break

    # A) Naive approach - for too low and too high, pick a random frequency and make the adjustment
    # Works for up to 3 frequencies, but bounces around and does not reliably converge with 4 or more
    # if too_low_score > 0:
    #     increase_index = random.randint(0, len(guess_frequencies) - 1)
    #     guess_frequencies[increase_index]['frequency'] += (too_low_score * NUM_WINDOWS)
    #
    # if too_high_score > 0:
    #     eligible_guess_indices = [i for i in range(len(guess_frequencies)) if guess_frequencies[i]['frequency'] - too_high_score > 0]
    #     decrease_index = random.randint(0, len(eligible_guess_indices) - 1)
    #     guess_frequencies[eligible_guess_indices[decrease_index]]['frequency'] -= (too_high_score * NUM_WINDOWS)

    # B) Incremental approach - add or subtract part of the adjustment from multiple guess frequencies
    # if too_low_score > 0:
    #     too_low_adjustments = [p * too_low_score for p in get_normalized_probability_list(2)]
    #     for value in too_low_adjustments:
    #         increase_index = random.randint(0, len(guess_frequencies) - 1)
    #         print(value)
    #         guess_frequencies[increase_index]['frequency'] += (value * NUM_WINDOWS)
    #
    # if too_high_score > 0:
    #     too_high_adjustments = [p * too_high_score for p in get_normalized_probability_list(2)]
    #     for value in too_high_adjustments:
    #         eligible_guess_indices = [i for i in range(len(guess_frequencies)) if guess_frequencies[i]['frequency'] - value > 0]
    #         decrease_index = random.randint(0, len(eligible_guess_indices) - 1)
    #         guess_frequencies[eligible_guess_indices[decrease_index]]['frequency'] -= (value * NUM_WINDOWS)

    # C) Incremental without replacement - add or subtract from frequencies, but not both in the same round
    # Works somewhat better for 3 or 4 frequencies, but still bounces around and does not reliably converge
    # TODO Next step: use the value fitness in a genetic algorithm
    if too_high_score == 0:
        add_qty = len(guess_frequencies)
        subtract_qty = 0
    elif too_low_score == 0:
        add_qty = 0
        subtract_qty = len(guess_frequencies)
    elif len(guess_frequencies) % 2 == 0:
        add_qty = int(len(guess_frequencies) / 2)
        subtract_qty = int(len(guess_frequencies) / 2)
    else:
        add_qty = int((len(guess_frequencies) / 2) + random.random())
        subtract_qty = len(guess_frequencies) - add_qty

    new_guess_frequencies = []

    too_high_adjustments = [p * too_high_score for p in get_normalized_probability_list(subtract_qty)]
    for value in too_high_adjustments:
        eligible_guess_indices = [i for i in range(len(guess_frequencies)) if
                                  guess_frequencies[i]['frequency'] - value > 0]

        if len(eligible_guess_indices) > 0:
            subtract_index = random.randint(0, len(eligible_guess_indices) - 1)
            new_guess_frequencies.append({
                'type': 'sine',
                'frequency': guess_frequencies[eligible_guess_indices[subtract_index]]['frequency'] - value
            })
            del guess_frequencies[eligible_guess_indices[subtract_index]]
        else:
            keep_index = random.randint(0, len(guess_frequencies) - 1)
            new_guess_frequencies.append({
                'type': 'sine',
                'frequency': guess_frequencies[keep_index]['frequency']
            })
            del guess_frequencies[keep_index]

    too_low_adjustments = [p * too_low_score for p in get_normalized_probability_list(add_qty)]
    for value in too_low_adjustments:
        add_index = random.randint(0, len(guess_frequencies) - 1)
        new_guess_frequencies.append({
            'type': 'sine',
            'frequency': guess_frequencies[add_index]['frequency'] + value
        })
        del guess_frequencies[add_index]

    guess_frequencies = copy.deepcopy(new_guess_frequencies)

    print('Current guess frequencies:\n{}'.format(json.dumps(guess_frequencies, indent=2)))
    print('Target frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))

    current_round += 1

print('done after {} rounds'.format(current_round))
print('Final guess frequencies:\n{}'.format(json.dumps(guess_frequencies, indent=2)))
print('Target frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))