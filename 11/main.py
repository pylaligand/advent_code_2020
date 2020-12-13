#!/usr/bin/python

import argparse


class Status(object):

    EMPTY = 'L'
    FLOOR = '.'
    OCCUPIED = '#'

    @classmethod
    def from_char(cls, char):
        return char


class Layout(object):

    def __init__(self, lines):
        self.seats = []
        self.width = len(lines)
        self.height = len(lines[0])
        for line in lines:
            row = []
            for char in line:
                row.append(Status.from_char(char))
            self.seats.append(row)


    def _next_status_by_vicinity(self, x, y):
        status = self.seats[x][y]
        if status == Status.FLOOR:
            return Status.FLOOR
        neighbors = []
        for i in range(max(0, x - 1), 1 + min(x + 1, self.width - 1)):
            for j in range(max(0, y - 1), 1 + min(y + 1, self.height - 1)):
                if (i, j) == (x, y):
                    continue
                neighbors.append(self.seats[i][j])
        if status == Status.EMPTY and all(n != Status.OCCUPIED for n in neighbors):
            return Status.OCCUPIED
        if status == Status.OCCUPIED and sum(1 for n in neighbors if n == Status.OCCUPIED) >= 4:
            return Status.EMPTY
        return status


    def _next_status_by_visibility(self, x, y):
        status = self.seats[x][y]
        if status == Status.FLOOR:
            return Status.FLOOR
        neighbors = []
        for delta_x in [-1, 0, +1]:
            for delta_y in [-1, 0, +1]:
                if (delta_x, delta_y) == (0, 0):
                    continue
                i, j = x, y
                while True:
                    i = i + delta_x
                    j = j + delta_y
                    if i < 0 or i >= self.width:
                        break
                    if j < 0 or j >= self.height:
                        break
                    if self.seats[i][j] == Status.FLOOR:
                        continue
                    neighbors.append(self.seats[i][j])
                    break
        if status == Status.EMPTY and all(n != Status.OCCUPIED for n in neighbors):
            return Status.OCCUPIED
        if status == Status.OCCUPIED and sum(1 for n in neighbors if n == Status.OCCUPIED) >= 5:
            return Status.EMPTY
        return status


    def _step(self, compute_next):
        next_seats = []
        for i in range(0, self.width):
            next_row = []
            for j in range(0, self.height):
                next_row.append(compute_next(i, j))
            next_seats.append(next_row)
        if next_seats == self.seats:
            return False
        self.seats = next_seats
        return True


    def run_by_vicinity(self):
        while self._step(self._next_status_by_vicinity):
            pass


    def run_by_visibility(self):
        while self._step(self._next_status_by_visibility):
            pass


    def n_occupied(self):
        return sum(1 for i in range(0, self.width) for j in range(0, self.height)
                   if self.seats[i][j] == Status.OCCUPIED)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    layout = Layout(lines)

    if args.next:
        layout.run_by_visibility()
    else:
        layout.run_by_vicinity()
    print(layout.n_occupied())


if __name__ == "__main__":
    main()
