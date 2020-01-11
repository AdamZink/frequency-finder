import numpy as np
from scipy import signal
import math


def get_sine(frequency, samples_per_second, duration_in_seconds=1):
    t = np.arange(samples_per_second * duration_in_seconds)
    return np.sin(2.0 * np.pi * t * ((1.0 * frequency) / samples_per_second))


def normalize_for_wav(data, max_amplitude):
    return np.int16(data / np.max(np.abs(data)) * (max_amplitude * (32767 - 100)))


def generate_signal_from_obj(frequency_obj, samples_per_second=44100, max_amplitude=0.1):
    data = np.zeros((samples_per_second,))
    for obj in frequency_obj:
        data += get_sine(obj['frequency'], samples_per_second, 1)
    return normalize_for_wav(data, max_amplitude)


def generate_bucketed_signal(data, number_of_windows):
    fs = data.size

    window_length_in_samples = math.floor(fs / number_of_windows)
    # print('\nwindow length: ' + str(window_length_in_samples))

    # window_length_in_seconds = math.floor(number_of_windows / fs)
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
    # TODO fix bug causing:
    #  ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    rel_max_indices_filtered = np.array([i for i in rel_max_index_arrays[0] if (sxx[i] * 1.0) / max_sxx > 0.01])

    return np.array([np.array([1 if i in rel_max_indices_filtered else 0]) for i in range(len(sxx))])
