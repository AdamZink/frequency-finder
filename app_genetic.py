from signal_util import *
from data_util import *
import json
from finder.fitness.frequency.values import *
import copy


population_size = 4
num_frequencies = 1

target_frequencies = get_random_frequency_array(num_frequencies)
print('Target frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))

population = get_random_population(population_size, num_frequencies)

print('\nInitial candidates:')
for c in population:
    print(c.get_formatted())

max_rounds = 1
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


target_signal = generate_signal_from_obj(target_frequencies)
target_bucketed = generate_bucketed_signal(target_signal, NUM_WINDOWS)
debug_bucketed(target_bucketed)

while current_round <= max_rounds:

    lowest_score = None

    for c in population:
        cascade_update = False

        if c.get_wav_signal() is None:
            c.set_wav_signal(generate_signal_from_obj(c.get_frequencies()))
            cascade_update = True

        if c.get_bucketed_signal() is None or cascade_update is True:
            c.set_bucketed_signal(generate_bucketed_signal(c.get_wav_signal(), NUM_WINDOWS))
            cascade_update = True

        if cascade_update is True:
            too_low_score, too_high_score = get_frequency_value_scores(target_bucketed, c.get_bucketed_signal())
            c.set_too_low_score(too_low_score)
            c.set_too_high_score(too_high_score)

        combined_score = c.get_too_low_score() + c.get_too_high_score()
        if lowest_score is None or combined_score < lowest_score:
            lowest_score = combined_score

    if lowest_score == 0:
        break


    # TODO use tournament selection on the population
    #  e.g. rounds of random 4, pick best 2, continue until half of population is chosen for crossover


    # TODO crossover


    # Mutation
    # Incremental without replacement - add or subtract from frequencies, but not both in the same round
    # Works somewhat better for 3 or 4 frequencies, but still bounces around and does not reliably converge
    # TODO Next step: use the value fitness in a genetic algorithm
    # if too_high_score == 0:
    #     add_qty = len(guess_frequencies)
    #     subtract_qty = 0
    # elif too_low_score == 0:
    #     add_qty = 0
    #     subtract_qty = len(guess_frequencies)
    # elif len(guess_frequencies) % 2 == 0:
    #     add_qty = int(len(guess_frequencies) / 2)
    #     subtract_qty = int(len(guess_frequencies) / 2)
    # else:
    #     add_qty = int((len(guess_frequencies) / 2) + random.random())
    #     subtract_qty = len(guess_frequencies) - add_qty
    #
    # new_guess_frequencies = []
    #
    # too_high_adjustments = [p * too_high_score for p in get_normalized_probability_list(subtract_qty)]
    # for value in too_high_adjustments:
    #     eligible_guess_indices = [i for i in range(len(guess_frequencies)) if
    #                               guess_frequencies[i]['frequency'] - value > 0]
    #
    #     if len(eligible_guess_indices) > 0:
    #         subtract_index = random.randint(0, len(eligible_guess_indices) - 1)
    #         new_guess_frequencies.append({
    #             'type': 'sine',
    #             'frequency': guess_frequencies[eligible_guess_indices[subtract_index]]['frequency'] - value
    #         })
    #         del guess_frequencies[eligible_guess_indices[subtract_index]]
    #     else:
    #         keep_index = random.randint(0, len(guess_frequencies) - 1)
    #         new_guess_frequencies.append({
    #             'type': 'sine',
    #             'frequency': guess_frequencies[keep_index]['frequency']
    #         })
    #         del guess_frequencies[keep_index]
    #
    # too_low_adjustments = [p * too_low_score for p in get_normalized_probability_list(add_qty)]
    # for value in too_low_adjustments:
    #     add_index = random.randint(0, len(guess_frequencies) - 1)
    #     new_guess_frequencies.append({
    #         'type': 'sine',
    #         'frequency': guess_frequencies[add_index]['frequency'] + value
    #     })
    #     del guess_frequencies[add_index]
    #
    # guess_frequencies = copy.deepcopy(new_guess_frequencies)
    #
    # print('Current guess frequencies:\n{}'.format(json.dumps(guess_frequencies, indent=2)))
    # print('Target frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))

    current_round += 1

print('done after {} rounds'.format(current_round - 1))

best_score = None
best_candidate = None

for c in population:
    c_score = c.get_too_high_score() + c.get_too_low_score()
    if best_score is None or c_score < best_score:
        best_score = c_score
        best_candidate = c

print('\nBest candidate:')
print(best_candidate.get_formatted())

print('\nTarget frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))
