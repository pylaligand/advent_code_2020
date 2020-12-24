#!/usr/bin/python

import argparse
from collections import namedtuple

Sequence = namedtuple('Sequence', ['directions'])


# Tile coordinates:
# - x-axis: positive from northwest to southeast
# - y-axis: positive from southwest to northeast
class Direction(object):
    WEST = (-1, -1)
    EAST = (+1, +1)
    SOUTHWEST = (0, -1)
    SOUTHEAST = (+1, 0)
    NORTHWEST = (-1, 0)
    NORTHEAST = (0, +1)

    ALL = [WEST, EAST, SOUTHWEST, SOUTHEAST, NORTHWEST, NORTHEAST]


def parse_sequences(lines):
    result = []
    for line in lines:
        chars = list(line)
        directions = []
        while chars:
            c1 = chars.pop(0)
            if c1 == 'e' or c1 == 'w':
                directions.append(Direction.EAST if c1 ==
                                  'e' else Direction.WEST)
            else:
                c2 = chars.pop(0)
                if c1 == 'n':
                    directions.append(Direction.NORTHEAST if c2 ==
                                      'e' else Direction.NORTHWEST)
                else:
                    directions.append(Direction.SOUTHEAST if c2 ==
                                      'e' else Direction.SOUTHWEST)
        result.append(Sequence(directions))
    return result


def _compute_starting_state(sequences):
    tiles = {}  # coordinates --> is_black
    for seq in sequences:
        coords = (0, 0)
        for d in seq.directions:
            coords = (coords[0] + d[0], coords[1] + d[1])
        tiles[coords] = not tiles.get(coords, False)
    return tiles


def _count_black_tiles(tiles):
    return sum(1 for v in tiles.values() if v)


def count_black_tiles(sequences):
    tiles = _compute_starting_state(sequences)
    return _count_black_tiles(tiles)


def make_beauty_happen(sequences, days):
    tiles = _compute_starting_state(sequences)
    for _ in range(0, days):
        min_x = min(x for x, _ in tiles.keys())
        max_x = max(x for x, _ in tiles.keys())
        min_y = min(y for _, y in tiles.keys())
        max_y = max(y for _, y in tiles.keys())
        new_tiles = {}
        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                black_neighbors_count = 0
                for d in Direction.ALL:
                    if tiles.get((x + d[0], y + d[1]), False):
                        black_neighbors_count += 1
                is_black = tiles.get((x, y), False)
                new_value = False
                if is_black:
                    if black_neighbors_count in [1, 2]:
                        new_value = True
                else:
                    if black_neighbors_count == 2:
                        new_value = True
                new_tiles[(x, y)] = new_value
        tiles = new_tiles
    return _count_black_tiles(tiles)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    sequences = parse_sequences(lines)

    if args.next:
        print(make_beauty_happen(sequences, 100))
    else:
        print(count_black_tiles(sequences))


if __name__ == "__main__":
    main()
