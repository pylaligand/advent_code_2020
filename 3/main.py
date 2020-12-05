#!/usr/bin/python

import argparse
from collections import namedtuple


Position = namedtuple('Position', ['x', 'y'])


class Map(object):

    def __init__(self, lines):
        self.line_width = len(lines[0])
        self.height = len(lines)
        self.trees = []
        for line in lines:
            self.trees.append([i for (i, p) in enumerate(line) if p == '#'])


    def _is_within_bounds(self, position):
        return position.x >= 0 and position.y >= 0 and position.y < self.height


    def _is_tree(self, position):
        adjusted_x = position.x % self.line_width
        return adjusted_x in self.trees[position.y]


    def find_tree_count(self, x_diff, y_diff):
        position = Position(0, 0)
        n_trees = 0
        while self._is_within_bounds(position):
            if self._is_tree(position):
                n_trees += 1
            position = Position(position.x + x_diff, position.y + y_diff)
        return n_trees


    def __str__(self):
        return self.trees.__str__()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        ze_map = Map([l.strip() for l in input_file.readlines()])

    # print(ze_map.find_tree_count(3, 1))

    result = ze_map.find_tree_count(1, 1)
    result *= ze_map.find_tree_count(3, 1)
    result *= ze_map.find_tree_count(5, 1)
    result *= ze_map.find_tree_count(7, 1)
    result *= ze_map.find_tree_count(1, 2)

    print(result)


if __name__ == "__main__":
    main()
