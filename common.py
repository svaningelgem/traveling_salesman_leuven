import contextlib
import csv
import math
from datetime import datetime
from typing import Generator, Tuple

import numpy as np
from scipy import spatial

Point = Tuple[float, float]


def _load_data() -> Generator[Tuple[float, float], None, None]:
    with open('coordinates.csv', 'r') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # Skip header
        for line in reader:
            yield float(line[0]), float(line[1])  # Don't return the name


def distance(x: Point, y: Point) -> float:
    # https://www.cuemath.com/euclidean-distance-formula/
    # I know I should use the haversine distance here, but the curve of the earth ain't that wrong on like 10km...
    return math.sqrt(
        (x[0] - x[1]) ** 2
        + (y[0] - y[1]) ** 2
    )


coordinates = np.array(list(_load_data()))
num_points = len(coordinates)
distance_matrix = spatial.distance.cdist(coordinates, coordinates, metric='euclidean')


def write_gps_file(coords: np.ndarray, name):
    with open(f'{name}.gpx', 'w') as fp:
        fp.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fp.write('<gpx version="1.1" creator="Me, myself and I">\n')
        fp.write('  <rte>\n')
        fp.write(f'    <name>{name}</name>\n')
        fp.write('    <number>0</number>\n')

        for coord in coords:
            fp.write(f'    <rtept lat="{coord[0]}" lon="{coord[1]}"/>\n')
        fp.write('  </rte>\n')
        fp.write('</gpx>\n')


def default_route():
    # We want to start & stop at the same place.
    # So, just add the first index (0) to the route.
    return np.concatenate([np.arange(num_points), [0]])


@contextlib.contextmanager
def check_time():
    print("Length of default route:", cost(default_route()))

    start = datetime.now()
    try:
        yield
    finally:
        stop = datetime.now()
        print("Time taken:", stop - start)


def cost(route):
    return distance_matrix[np.roll(route, 1), route].sum()  # shifts route array by 1 in order to look at pairs of cities