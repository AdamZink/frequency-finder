from scipy import signal
import math
import random
import json
import numpy as np
from finder.fitness.frequency.count import *


def get_sine(frequency, samples_per_second, duration_in_seconds=1):
    t = np.arange(samples_per_second * duration_in_seconds)
    return np.sin(2.0 * np.pi * t * ((1.0 * frequency) / samples_per_second))


def normalize_for_wav(data, max_amplitude):
    return np.int16(data / np.max(np.abs(data)) * (max_amplitude * (32767 - 100)))


def get_signal_from_obj(frequency_obj, samples_per_second=44100, max_amplitude=0.1):
    data = np.zeros((samples_per_second,))
    for obj in frequency_obj:
        data += get_sine(obj['frequency'], samples_per_second, 1)
    return normalize_for_wav(data, max_amplitude)


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

    # Find relative extrema in spectrogram energy. Identify frequencies as extrema above a minimum threshold
    max_sxx = np.amax(sxx)
    rel_max_index_arrays = signal.argrelextrema(sxx, np.greater)
    rel_max_indices_filtered = np.array([i for i in rel_max_index_arrays[0] if (sxx[i] * 1.0) / max_sxx > 0.01])

    return np.array([np.array([1 if i in rel_max_indices_filtered else 0]) for i in range(len(sxx))])


def get_random_frequency():
    return (random.random() * 400) + 200


def append_random_frequency(frequencies):
    frequencies.append({
            'type': 'sine',
            'frequency': get_random_frequency()
        })


def get_random_frequency_array(freq_count):
    assert freq_count > 0

    frequencies = []
    for _ in range(0, freq_count):
        append_random_frequency(frequencies)

    return frequencies


def remove_frequency(frequencies):
    frequencies.pop()


target_frequencies = get_random_frequency_array(3)
# print(target_frequencies)

guess_frequencies = get_random_frequency_array(6)
# print(guess_frequencies)


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
        append_random_frequency(guess_frequencies)
    elif score < 0 and len(guess_frequencies) > 1:
        remove_frequency(guess_frequencies)
    else:
        break

    print(json.dumps(guess_frequencies, indent=2))

    current_round += 1

print('done')
print(json.dumps(target_frequencies, indent=2))
print('vs')
print(json.dumps(guess_frequencies, indent=2))
print('Final guess: number of frequencies = {}'.format(len(guess_frequencies)))
