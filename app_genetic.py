from signal_util import *
from data_util import *
import json
from finder.fitness.frequency.values import *
import copy
from finder.genetic.tournament import *
from finder.genetic.elite import *


num_frequencies = 4

population_size = 8
num_elite = 1
winners_per_round = 1

max_rounds = 100

target_frequencies = get_random_frequency_array(num_frequencies)
print('Target frequencies:\n{}'.format(json.dumps(target_frequencies, indent=2)))

population = get_random_population(population_size, num_frequencies)

current_round = 1

NUM_WINDOWS = 1


def print_best_candidate(population):
    best_score = None
    best_candidate = None

    for c in population:
        c_score = c.get_too_high_score() + c.get_too_low_score()
        if best_score is None or c_score < best_score:
            best_score = c_score
            best_candidate = c

    print('\nBest candidate:')
    print(best_candidate.get_formatted())


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

while True:
    lowest_score = None
    best_index = None

    # TODO Note: it's taking a long time to calculate all the signals and scores for 64 candidates
    # print("before calculation")

    for i in range(len(population)):
        population[i].set_wav_signal(generate_signal_from_obj(population[i].get_frequencies()))
        population[i].set_bucketed_signal(generate_bucketed_signal(population[i].get_wav_signal(), NUM_WINDOWS))

        too_low_score, too_high_score = get_frequency_value_scores(target_bucketed, population[i].get_bucketed_signal())
        population[i].set_too_low_score(too_low_score)
        population[i].set_too_high_score(too_high_score)

        combined_score = population[i].get_too_low_score() + population[i].get_too_high_score()

        if lowest_score is None or combined_score < lowest_score:
            best_index = i
            lowest_score = combined_score

    # print("after calculation")

    if current_round > max_rounds or lowest_score < 3:
        break

    print("\nBest candidate in round {}:\n{}".format(current_round, population[best_index].get_formatted()))

    elite_indices = get_elite_indices(population, num_elite)

    remaining_indices_for_tournament = [i for i in range(len(population)) if i not in elite_indices]

    non_elite_surviving_indices = []

    select_tournament_winners(
        population,
        remaining_indices_for_tournament,
        non_elite_surviving_indices,
        winners_per_round,
        num_elite
    )

    all_surviving_indices = elite_indices + non_elite_surviving_indices

    # randomly pair the next generation
    random.shuffle(all_surviving_indices)
    surviving_index_pairs = zip(all_surviving_indices[0::2], all_surviving_indices[1::2])

    children = []

    for i1, i2 in surviving_index_pairs:
        c1 = copy.deepcopy(population[i1])
        c2 = copy.deepcopy(population[i2])

        f1 = sorted(c1.get_frequencies(), key=lambda f: f['frequency'])
        f2 = sorted(c2.get_frequencies(), key=lambda f: f['frequency'])

        i_crossover = random.randint(0, num_frequencies)

        c1.set_frequencies(
            f1[0:i_crossover] + f2[i_crossover:num_frequencies]
        )

        c2.set_frequencies(
            f2[0:i_crossover] + f1[i_crossover:num_frequencies]
        )

        children.append(c1)
        children.append(c2)

    # Mutation of non-elite parents
    # Incremental without replacement - add or subtract from frequencies, but not both in the same round
    for i in non_elite_surviving_indices:
        c = population[i]

        c_frequencies = c.get_frequencies()

        if c.get_too_high_score() == 0:
            add_qty = len(c_frequencies)
            subtract_qty = 0
        elif c.get_too_low_score() == 0:
            add_qty = 0
            subtract_qty = len(c_frequencies)
        elif len(c_frequencies) % 2 == 0:
            add_qty = int(len(c_frequencies) / 2)
            subtract_qty = int(len(c_frequencies) / 2)
        else:
            add_qty = int((len(c_frequencies) / 2) + random.random())
            subtract_qty = len(c_frequencies) - add_qty

        new_guess_frequencies = []

        too_high_adjustments = [p * c.get_too_high_score() for p in get_normalized_probability_list(subtract_qty)]
        for value in too_high_adjustments:
            eligible_guess_indices = [i for i in range(len(c_frequencies)) if
                                      c_frequencies[i]['frequency'] - value > 0]

            if len(eligible_guess_indices) > 0:
                subtract_index = random.randint(0, len(eligible_guess_indices) - 1)
                new_guess_frequencies.append({
                    'type': 'sine',
                    'frequency': c_frequencies[eligible_guess_indices[subtract_index]]['frequency'] - value
                })
                del c_frequencies[eligible_guess_indices[subtract_index]]
            else:
                keep_index = random.randint(0, len(c_frequencies) - 1)
                new_guess_frequencies.append({
                    'type': 'sine',
                    'frequency': c_frequencies[keep_index]['frequency']
                })
                del c_frequencies[keep_index]

        too_low_adjustments = [p * c.get_too_low_score() for p in get_normalized_probability_list(add_qty)]
        for value in too_low_adjustments:
            add_index = random.randint(0, len(c_frequencies) - 1)
            new_guess_frequencies.append({
                'type': 'sine',
                'frequency': c_frequencies[add_index]['frequency'] + value
            })
            del c_frequencies[add_index]

        c.set_frequencies(new_guess_frequencies)
        c.set_wav_signal(None)
        c.set_too_high_score(None)
        c.set_too_low_score(None)

    new_population = []

    for i in elite_indices:
        new_population.append(copy.deepcopy(population[i]))

    for i in non_elite_surviving_indices:
        new_population.append(copy.deepcopy(population[i]))

    for c in children:
        new_population.append(c)

    population = new_population

    current_round += 1

print_best_candidate(population)

print('\nTarget frequencies:\n{}'.format(
    json.dumps(sorted(target_frequencies, key=lambda x: x['frequency']), indent=2))
)

print('done after {} rounds'.format(current_round - 1))
