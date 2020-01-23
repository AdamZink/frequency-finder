from data_util import *
import json
import copy
from finder.genetic.tournament import *
from finder.genetic.elite import *


min_starting_frequencies = 3
max_starting_frequencies = 6

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
        c_score = c.get_composite_score()
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


target = get_random_target(
    min_starting_frequencies,
    max_starting_frequencies,
    num_windows
)
print('Target frequencies:\n{}'.format(json.dumps(target.get_frequencies(), indent=2)))

population = get_random_population(
    population_size,
    min_starting_frequencies,
    max_starting_frequencies,
    target,
    num_windows
)

target.debug_bucketed()

while True:
    lowest_score = None
    best_index = None

    for i in range(len(population)):
        combined_score = population[i].get_composite_score()

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

        f1 = []
        f2 = []

        parent_frequencies = population[i1].get_frequencies() + population[i2].get_frequencies()
        min_parent_freq = min([f['frequency'] for f in parent_frequencies])
        max_parent_freq = max([f['frequency'] for f in parent_frequencies])

        min_crossover_freq = min_parent_freq / 1.5 if min_parent_freq / 1.5 > 1.0 else 1.0
        max_crossover_freq = max_parent_freq * 1.5 if max_parent_freq * 1.5 < 20000.0 else 20000.0

        crossover_frequency = get_random_frequency(min_crossover_freq, max_crossover_freq)

        for f in population[i1].get_frequencies():
            if f['frequency'] < crossover_frequency:
                f1.append(f)
            else:
                f2.append(f)

        for f in population[i2].get_frequencies():
            if f['frequency'] < crossover_frequency:
                f2.append(f)
            else:
                f1.append(f)

        c1.set_frequencies_and_calculate_scores(f1, target, num_windows)
        c2.set_frequencies_and_calculate_scores(f2, target, num_windows)

        children.append(c1)
        children.append(c2)

    # Mutation of children
    for c in children:
        # Adjust the number of frequencies
        if c.frequency_count_score > 0 and random.random() < 0.25:
            append_random_frequencies(
                c.frequencies,
                c.frequency_count_score
            )
        elif c.frequency_count_score < 0 and random.random() < 0.25:
            random.shuffle(c.frequencies)
            remove_frequencies(
                c.frequencies,
                -c.frequency_count_score if len(c.frequencies) > -c.frequency_count_score else len(c.frequencies) - 1
            )

        # Either add or subtract from each frequency value (with high probability)
        if random.random() < 0.9:
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

        # Completely random mutation of each frequency value (with low probability)
        for f in c.get_frequencies():
            if random.random() < 0.01:
                f['frequency'] = get_random_frequency(100, 2000)

        c.calculate_scores(target, num_windows)

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
