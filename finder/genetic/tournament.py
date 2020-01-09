import random


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


def get_round_winner_indices(population, candidate_indices, winners_per_round):
    assert winners_per_round > 0
    assert winners_per_round <= len(candidate_indices)

    winner_indices = []

    while len(winner_indices) < winners_per_round:
        candidate_weights = get_candidate_weights([population[i] for i in candidate_indices])

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
def select_tournament_winners(population, remaining_indices_for_tournament, non_elite_surviving_indices, winners_per_round, num_elite):
    tournament_pool_indices = [i for i in remaining_indices_for_tournament]

    while num_elite + len(non_elite_surviving_indices) < len(tournament_pool_indices):
        random.shuffle(tournament_pool_indices)

        # TODO fix for partial number of winners remaining (e.g. only 1 spot left because of elitism)

        winner_indices = get_round_winner_indices(population, tournament_pool_indices[0:3], winners_per_round)

        for i in winner_indices:
            non_elite_surviving_indices.append(i)

        tournament_pool_indices = [i for i in remaining_indices_for_tournament if i not in non_elite_surviving_indices]
