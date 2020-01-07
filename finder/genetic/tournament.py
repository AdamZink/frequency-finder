import random
import copy


def get_composite_score(candidate):
    return candidate.get_too_high_score() + candidate.get_too_low_score()


def get_inverted_scores(scores):
    min_score = min(scores)
    max_min_diff = max(scores) - min_score
    return [abs((s - min_score) - max_min_diff) + min_score for s in scores]


def get_candidate_weights(candidates):
    inverted_composite_scores = get_inverted_scores([get_composite_score(c) for c in candidates])
    composite_score_sum = sum(inverted_composite_scores)
    if composite_score_sum == 0:
        return [1.0 / len(candidates)] * len(candidates)
    return [s / composite_score_sum for s in inverted_composite_scores]


def get_round_winner_indices(candidates, winners_per_round):
    assert winners_per_round > 0
    assert winners_per_round <= len(candidates)

    winner_indices = []
    candidate_indices = [i for i in range(len(candidates))]

    while len(winner_indices) < winners_per_round:
        candidate_weights = get_candidate_weights([candidates[i] for i in candidate_indices])

        num = random.random()
        selected_index = None
        for i in range(len(candidate_indices)):
            if i == len(candidate_indices) - 1:
                selected_index = i
                break
            num -= candidate_weights[i]
            if num <= 0:
                selected_index = i
                break

        winner_indices.append(candidate_indices[selected_index])
        del candidate_indices[selected_index]

    return winner_indices


# append parents which move on to next population / delete from current population
def select_tournament_winners(population, next_population, winners_per_round):
    while len(next_population) < len(population):
        random.shuffle(population)

        winner_indices = get_round_winner_indices(population[0:3], winners_per_round)

        for i in winner_indices:
            next_population.append(copy.deepcopy(population[i]))
        for i in winner_indices:
            del population[i]
