import random


def get_random_frequency():
    return (random.random() * 400) + 200


def append_random_frequencies(frequencies, count):
    for _ in range(count):
        frequencies.append({
                'type': 'sine',
                'frequency': get_random_frequency()
        })


def get_random_frequency_array(freq_count):
    assert freq_count > 0

    frequencies = []
    append_random_frequencies(frequencies, freq_count)

    return frequencies
