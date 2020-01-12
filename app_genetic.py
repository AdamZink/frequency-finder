from data_util import *
import json
import copy
from finder.genetic.tournament import *
from finder.genetic.elite import *


num_frequencies = 4

population_size = 8
num_elite = 1
winners_per_round = 2

max_rounds = 100

current_round = 1

num_windows = 1


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


def get_normalized_probability_list(qty):
    probability_list = []
    for _ in range(qty):
        probability_list.append(random.random())
    sum_of_probabilities = sum(probability_list) * 1.5
    return [p / sum_of_probabilities for p in probability_list]


target = Candidate()
target.set_frequencies_and_calculate_scores(get_random_frequency_array(num_frequencies), target, num_windows)
print('Target frequencies:\n{}'.format(json.dumps(target.get_frequencies(), indent=2)))

population = get_random_population(population_size, num_frequencies, target, num_windows)

target.debug_bucketed()

while True:
    lowest_score = None
    best_index = None

    for i in range(len(population)):
        combined_score = population[i].get_too_low_score() + population[i].get_too_high_score()

        if lowest_score is None or combined_score < lowest_score:
            best_index = i
            lowest_score = combined_score

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

    # Create children and calculate their fitness scores
    for i1, i2 in surviving_index_pairs:
        c1 = Candidate()
        c2 = Candidate()

        f1 = sorted(population[i1].get_frequencies(), key=lambda f: f['frequency'])
        f2 = sorted(population[i2].get_frequencies(), key=lambda f: f['frequency'])

        i_crossover = random.randint(0, num_frequencies)

        c1.set_frequencies_and_calculate_scores(
            f1[0:i_crossover] + f2[i_crossover:num_frequencies], target, num_windows
        )

        c2.set_frequencies_and_calculate_scores(
            f2[0:i_crossover] + f1[i_crossover:num_frequencies], target, num_windows
        )

        # TODO something broke the algorithm - it does not converge at the moment... the best score stays the same after 1st round

        # print('Children:')
        # print(c1.get_formatted())
        # print(c2.get_formatted())

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

        c.set_frequencies_and_calculate_scores(new_guess_frequencies, target, num_windows)

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
    json.dumps(sorted(target.get_frequencies(), key=lambda x: x['frequency']), indent=2))
)

print('done after {} rounds'.format(current_round - 1))
