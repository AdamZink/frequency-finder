def get_elite_indices(population, num_elite):
    assert num_elite <= len(population)

    composite_score_lookup = [
        (
            i,
            population[i].get_too_high_score() + population[i].get_too_low_score()
        ) for i in range(len(population))]

    return [t[0] for t in sorted(composite_score_lookup, key=lambda c: c[1])][0:num_elite]
