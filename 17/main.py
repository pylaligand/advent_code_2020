#!/usr/bin/python

import argparse


class DimensionState(object):

    def __init__(self, with_4th):
        self._cubes = {}
        self._with_4th = with_4th


    def is_active(self, x, y, z, w):
        return self._cubes.setdefault((x, y, z, w), False)


    def set_active(self, x, y, z, w, active):
        self._cubes[(x, y, z, w)] = active


    def extent(self):
        x_values = [x for (x, y, z, w), active in self._cubes.iteritems() if active]
        x_range = range(min(x_values) - 1, max(x_values) + 2) if x_values else range(0, 0)
        y_values = [y for (x, y, z, w) in self._cubes.keys()]
        y_range = range(min(y_values) - 1, max(y_values) + 2) if y_values else range(0, 0)
        z_values = [z for (x, y, z, w) in self._cubes.keys()]
        z_range = range(min(z_values) - 1, max(z_values) + 2) if z_values else range(0, 0)
        if self._with_4th:
            w_values = [w for (x, y, z, w) in self._cubes.keys()]
            w_range = range(min(w_values) - 1, max(w_values) + 2) if w_values else range(0, 0)
        else:
            w_range = range(0, 1)
        return (x_range, y_range, z_range, w_range)


    def active_count(self):
        return sum(1 for v in self._cubes.values() if v)


class Dimension(object):

    def __init__(self, lines, with_4th):
        self._state = DimensionState(with_4th)
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                if char == '#':
                    self._state.set_active(x, y, 0, 0, True)
        self._with_4th = with_4th


    def _compute_new_cube_state(self, xc, yc, zc, wc):
        n_active_neighbors = 0
        for x in range(xc - 1, xc + 2):
            for y in range(yc - 1, yc + 2):
                for z in range(zc - 1, zc + 2):
                    for w in range(wc - 1, wc + 2):
                        if (x, y, z, w) == (xc, yc, zc, wc):
                            continue
                        if self._state.is_active(x, y, z, w):
                            n_active_neighbors += 1
        if self._state.is_active(xc, yc, zc, wc):
            return n_active_neighbors == 2 or n_active_neighbors == 3
        else:
            return n_active_neighbors == 3


    def step(self):
        new_state = DimensionState(self._with_4th)
        x_range, y_range, z_range, w_range = self._state.extent()
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    for w in w_range:
                        if self._compute_new_cube_state(x, y, z, w):
                            new_state.set_active(x, y, z, w, True)
        self._state = new_state


    def is_active(self, x, y, z, w):
        return self._state.is_active(x, y, z, w)


    def active_count(self):
        return self._state.active_count()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    if args.next:
        dimension = Dimension(lines, with_4th=True)
    else:
        dimension = Dimension(lines, with_4th=False)

    for i in range(6):
        dimension.step()
    print(dimension.active_count())


if __name__ == "__main__":
    main()
