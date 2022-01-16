from __future__ import division

from common import check_time, coordinates, cost, default_route, write_gps_file


def main_2opt(route):
    def _swap_i_j():
        new_route = route.copy()
        new_route[i:j] = route[j - 1:i - 1:-1]  # this is the 2-optSwap since j >= i we use -1
        return new_route

    route_distance = cost(route)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue  # changes nothing, skip then
                new_route = _swap_i_j()
                new_distance = cost(new_route)
                if new_distance < route_distance:
                    route = new_route    # change current route to best
                    route_distance = new_distance
                    improved = True

    return route


if __name__ == '__main__':
    with check_time():
        optimized_route = main_2opt(default_route())
        print("Cost of route after 2opt: ", cost(optimized_route))

        best_x = coordinates[optimized_route, :]
        write_gps_file(best_x, 'Leuven')
