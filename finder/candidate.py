import json


class Candidate:

    def __init__(self):
        self.frequencies = []
        self.wav_signal = None
        self.bucketed_signal = None
        self.too_high_score = None
        self.too_low_score = None

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies

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
