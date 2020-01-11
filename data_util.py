import random
from finder.candidate import Candidate


def get_random_frequency():
    return (random.random() * 400) + 200


def append_random_frequencies(frequencies, freq_count):
    for _ in range(freq_count):
        frequencies.append({
                'type': 'sine',
                'frequency': get_random_frequency()
        })


def get_random_frequency_array(freq_count):
    assert freq_count > 0

    frequencies = []
    append_random_frequencies(frequencies, freq_count)

    return frequencies


def get_random_population(qty, freq_count):
    population = []
    for _ in range(qty):
        candidate = Candidate()
        candidate.set_frequencies(get_random_frequency_array(freq_count))
        population.append(candidate)

    return population
