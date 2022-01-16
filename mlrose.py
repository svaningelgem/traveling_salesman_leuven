from itertools import combinations

import mlrose_hiive as mlrose

from common import check_time, coordinates, distance, write_gps_file

# Create list of distances between pairs of cities
dist_list = [
    (x, y, distance(coordinates[x], coordinates[y]))
    for x, y in combinations(range(len(coordinates)), r=2)
]


def main():
    # Source: https://mlrose.readthedocs.io/en/stable/source/tutorial2.html#solving-tsps-with-mlrose
    fitness_dists = mlrose.TravellingSales(distances=dist_list)
    problem_fit = mlrose.TSPOpt(length=len(coordinates), fitness_fn=fitness_dists, maximize=False)

    best_state, best_fitness, _ = mlrose.genetic_alg(problem_fit, max_iters=20)

    print("Best length after optimization: ", best_fitness)

    write_gps_file(coordinates[best_state, :], 'Leuven')


if __name__ == '__main__':
    with check_time():
        main()
