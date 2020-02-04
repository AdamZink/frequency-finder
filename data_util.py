import random
from finder.candidate import Candidate


def get_random_frequency(f_min, f_max):
    return (random.random() * (f_max - f_min)) + f_min


def append_random_frequencies(frequencies, freq_count):
    for _ in range(freq_count):
        # TODO make the gain a random value between 0 and 1, and then add fitness score to evaluate gain accuracy
        frequencies.append({
                'type': 'sine',
                'frequency': get_random_frequency(200, 1000),
                'gain': 1.0
        })


def get_random_frequency_array(freq_count):
    assert freq_count > 0

    frequencies = []
    append_random_frequencies(frequencies, freq_count)

    return frequencies


def get_random_population(qty, min_freqs, max_freqs, target, num_windows):
    population = []
    for _ in range(qty):
        candidate = Candidate()
        candidate.set_frequencies_and_calculate_scores(
            get_random_frequency_array(random.randint(min_freqs, max_freqs)),
            target,
            num_windows
        )
        population.append(candidate)

    return population


def remove_frequencies(frequencies, count):
    for _ in range(count):
        frequencies.pop()


def get_random_target(min_freqs, max_freqs, num_windows):
    candidate = Candidate()
    candidate.set_frequencies(get_random_frequency_array(random.randint(min_freqs, max_freqs)))
    candidate.generate_signals(num_windows)
    return candidate
