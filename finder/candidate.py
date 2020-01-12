import json
from signal_util import generate_signal_from_obj, generate_bucketed_signal
from finder.fitness.frequency.values import get_frequency_value_scores
import numpy as np


class Candidate:

    def __init__(self):
        self.frequencies = []
        self.wav_signal = None
        self.bucketed_signal = None
        self.too_high_score = None
        self.too_low_score = None

    def set_frequencies_and_calculate_scores(self, frequencies, target, num_windows):
        self.frequencies = frequencies
        self.wav_signal = generate_signal_from_obj(self.frequencies)
        self.bucketed_signal = generate_bucketed_signal(self.wav_signal, num_windows)
        self.too_low_score, self.too_high_score = get_frequency_value_scores(
            target.get_bucketed_signal(),
            self.bucketed_signal
        )

    def get_frequencies(self):
        return self.frequencies

    def set_wav_signal(self, wav_signal):
        self.wav_signal = wav_signal

    def get_wav_signal(self):
        return self.wav_signal

    def set_bucketed_signal(self, bucketed_signal):
        self.bucketed_signal = bucketed_signal

    def get_bucketed_signal(self):
        return self.bucketed_signal

    def set_too_high_score(self, too_high_score):
        self.too_high_score = too_high_score

    def get_too_high_score(self):
        return self.too_high_score

    def set_too_low_score(self, too_low_score):
        self.too_low_score = too_low_score

    def get_too_low_score(self):
        return self.too_low_score

    def get_formatted(self):
        return '\nFrequencies: {}\nToo high score: {}\nToo low score: {}\nComposite score: {}'.format(
            json.dumps(sorted(self.frequencies, key=lambda x: x['frequency']), indent=2),
            self.too_high_score,
            self.too_low_score,
            None if self.too_high_score is None or self.too_low_score is None else self.too_high_score + self.too_low_score
        )

    def debug_bucketed(self):
        print('\nDebug output for bucketed data >>>')
        print(self.bucketed_signal.shape)
        for i in range(self.bucketed_signal.shape[0]):
            if np.sum(self.bucketed_signal[i]) > 0:
                print("row index {}: {}".format(i, self.bucketed_signal[i]))
        print('<<<\n')
