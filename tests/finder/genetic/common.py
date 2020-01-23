from finder.candidate import Candidate


def get_candidates():
    candidates = []
    for i in range(4):
        c = Candidate()
        c.too_high_score = i + 1
        c.too_low_score = 0
        c.frequency_count_score = 0
        candidates.append(c)
    return candidates


def get_candidate_indices():
    return list(range(4))


def get_candidates_two_zeros():
    candidates = []
    for i in range(4):
        c = Candidate()
        if i > 1:
            c.too_high_score = 3
        else:
            c.too_high_score = 0
        c.too_low_score = 0
        c.frequency_count_score = 0
        candidates.append(c)
    return candidates


def get_candidates_all_zero():
    candidates = []
    for i in range(4):
        c = Candidate()
        c.too_high_score = 0
        c.too_low_score = 0
        c.frequency_count_score = 0
        candidates.append(c)
    return candidates
