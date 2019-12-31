import numpy as np
from scipy import signal
import scipy.io.wavfile as wf
import math
from score import *
import random
import os
import copy
import json


# Part 1 - generate target signal as numpy array
def get_sine(frequency, samples_per_second, duration_in_seconds=1):
    t = np.arange(samples_per_second * duration_in_seconds)
    return np.sin(2.0 * np.pi * t * ((1.0 * frequency) / samples_per_second))


def normalize_for_wav(data, max_amplitude):
    return np.int16(data / np.max(np.abs(data)) * (max_amplitude * (32767 - 100)))


# TODO try having 2 target frequencies, but only have 1 frequency in the guess. will it still converge to local min?
def get_target_frequencies():
    return [
        {
            'type': 'sine',
            'frequency': 400
        }
        # ,
        # {
        #     'type': 'sine',
        #     'frequency': 300
        # }
    ]


def get_signal_from_obj(frequency_obj, samples_per_second=44100, max_amplitude=0.1):
    data = np.zeros((samples_per_second,))
    for obj in frequency_obj:
        data += get_sine(obj['frequency'], samples_per_second, 1)
    return normalize_for_wav(data, max_amplitude)


def write_signal_to_wav(data, filename, samples_per_second=44100):
    filename = os.path.join('/spectrograms', filename)
    wf.write(filename, samples_per_second, data)
    print('Wrote ' + filename)

    return data


def get_random_frequency():
    return (random.random() * 400) + 200


def get_random_guess_frequencies():
    return [
        {
            'type': 'sine',
            'frequency': get_random_frequency()
        }
        # ,
        # {
        #     'type': 'sine',
        #     'frequency': get_random_frequency()
        # }
    ]


def get_bucketed_signal(data, number_of_windows):
    fs = data.size

    window_length_in_samples = math.floor(fs / number_of_windows)
    # print('\nwindow length: ' + str(window_length_in_samples))

    window_length_in_seconds = math.floor(number_of_windows / fs)
    # print('\nwindow time (sec): ' + str(window_length_in_seconds))

    # frequency_resolution = fs / window_length_in_samples
    # print('frequency resolution: ' + str(frequency_resolution))

    frequency_axis, time_axis, sxx = signal.spectrogram(
        data,
        fs=fs,
        window=signal.get_window('hann', window_length_in_samples),
        noverlap=0
    )

    # quantize Sxx into n number of bins of equal size between 0 and the max value
    max_sxx = np.amax(sxx)
    sxx_broadcasted = sxx / max_sxx

    # use ceiling to get Sxx values between 0 and num_Sxx_buckets - 1
    num_sxx_buckets = 2
    return np.ceil(sxx_broadcasted * num_sxx_buckets) - 1


def get_composite_score(guess_signal, target_signal, target_bucketed, number_of_windows):
    frequency_score = 1.0 * get_alternate_frequency_sum_score(
        get_bucketed_signal(guess_signal, number_of_windows),
        target_bucketed
    )

    signal_score = 1.0 * get_signal_diff_score(guess_signal, target_signal)

    return {
        'composite': frequency_score + signal_score,
        'frequency_score': frequency_score,
        'signal_score': signal_score
    }


number_of_windows = 4

print('Generating target wav file...')

target_frequencies = get_target_frequencies()
target_signal = get_signal_from_obj(target_frequencies)
write_signal_to_wav(target_signal, 'target_signal.wav')
print(target_signal)

target_bucketed = get_bucketed_signal(target_signal, number_of_windows)


# Part 2 - genetic algorithm
num_of_species = 4
max_generations = 50
target_score = 1.0

random_guesses = []
# random_guesses = [
#     [
#         {
#             'type': 'sine',
#             'frequency': 400
#         }
#     ],
#     [
#         {
#             'type': 'sine',
#             'frequency': 420
#         }
#     ],
#     [
#         {
#             'type': 'sine',
#             'frequency': 440
#         }
#     ],
#     [
#         {
#             'type': 'sine',
#             'frequency': 460
#         }
#     ]
# ]

for _ in range(num_of_species):
    random_guesses.append(get_random_guess_frequencies())

print(random_guesses)

generation_best_scores = np.empty(shape=(0, 2))
best_guess = random_guesses[0]

final_generation = max_generations

for i in [i + 1 for i in range(max_generations)]:

    print('\nGeneration ' + str(i))

    next_generation = []

    best_score = None
    best_index = None

    # map of index of random_guesses to score
    score_map = {}
    for j in range(num_of_species):
        score_map[j] = get_composite_score(
            get_signal_from_obj(random_guesses[j]),
            target_signal,
            target_bucketed,
            number_of_windows
        )
        if best_score is None or score_map[j]['composite'] < best_score['composite']:
            best_score = score_map[j]
            best_index = j

    # keep the best (elitism)
    best_guess = copy.deepcopy(random_guesses[best_index])
    next_generation.append({
        'guess': best_guess,
        'score': score_map[best_index]
    })
    del random_guesses[best_index]

    # tournament rounds - pick best score each time until keep goal is reached
    tournament_round_size = 3
    tournament_keep_goal = num_of_species / 2

    while len(next_generation) < tournament_keep_goal:
        tournament_indexes = random.sample(range(len(random_guesses)), tournament_round_size)
        best_round_index = tournament_round_size - 1

        for j in range(tournament_round_size - 1):
            if score_map[tournament_indexes[j]]['composite'] < score_map[tournament_indexes[best_round_index]]['composite']:
                best_round_index = j

        next_generation.append({
            'guess': copy.deepcopy(random_guesses[tournament_indexes[best_round_index]]),
            'score': score_map[tournament_indexes[best_round_index]]
        })
        del random_guesses[tournament_indexes[best_round_index]]

    # print('\nNext generation results before children:')
    # print(json.dumps(next_generation, indent=2))
    #
    # print('\nThese guesses do not continue further:')
    # print(random_guesses)

    # randomly pair the next generation
    random.shuffle(next_generation)
    parent_pairs = zip(next_generation[0::2], next_generation[1::2])

    child_results = []

    print('\nPairs:')
    for p1, p2 in parent_pairs:
        print(p1)
        print(p2)

        better_parent = p1 if p1['score']['composite'] < p2['score']['composite'] else p2
        worse_parent = p2 if better_parent == p1 else p1

        # Take advantage of linearity of frequency scores and compute distance from target frequencies
        frequency_adjustment = (better_parent['score']['frequency_score'] / 2.0) * number_of_windows

        print('adjustment: {}'.format(frequency_adjustment))

        # When comparing 2 parents, cannot tell which direction to adjust, so have each child go in opposite direction
        child_results.append({
            'frequency': better_parent['guess'][0]['frequency'] + frequency_adjustment,
            'signal_score': better_parent['score']['signal_score']
        })

        second_direction = 1 if better_parent['guess'][0]['frequency'] - frequency_adjustment > 0 else -1

        child_results.append({
            'frequency': better_parent['guess'][0]['frequency'] - (frequency_adjustment * second_direction),
            'signal_score': better_parent['score']['signal_score']
        })

    # print('\nChild results before mutation:')
    # print(json.dumps(child_results, indent=2))

    # mutation
    for child_result in child_results:
        # reduce the max mutation amount as child's signal score approaches 0
        mutation_range = child_result['signal_score'] / 500.0
        # print(mutation_range)

        if random.random() < 1:
            child_result['frequency'] += (random.random() * 2.0 * mutation_range) - mutation_range

        next_generation.append({
            'guess': [{
                'type': 'sine',
                'frequency': child_result['frequency']
            }]
        })

    # print('\nNext generation including children:')
    # print(json.dumps(next_generation, indent=2))

    random_guesses = [n['guess'] for n in next_generation]

    print('Next generation: ' + json.dumps(random_guesses, indent=2))

    generation_best_scores = np.append(generation_best_scores, [[i, best_score]], axis=0)
    print('Best score: ' + json.dumps(best_score, indent=2))

    if best_score['composite'] < target_score:
        final_generation = i
        break

print('Final guesses: ' + json.dumps(random_guesses, indent=2))
print(generation_best_scores)
print('Best guess: ' + json.dumps(best_guess, indent=2))
print('Target: ' + json.dumps(target_frequencies, indent=2))
print('Relative cost (species * generations): ' + str(num_of_species * final_generation))
