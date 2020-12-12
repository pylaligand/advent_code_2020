#!/usr/bin/python

import argparse


def binary_search(sequence, size, start):
    bounds = (0, size - 1)
    for i in sequence:
        min, max = bounds
        delta = (max - min + 1) / 2
        if i == start:
            bounds = (min, max - delta)
        else:
            bounds = (min + delta, max)
    min, max = bounds
    if min != max:
        raise Exception('Could not find spot: %s / %s' % (sequence, size))
    return min


class BoardingPass(object):

    def __init__(self, sequence):
        self.row = binary_search(sequence[:7], 128, 'F')
        self.column = binary_search(sequence[7:], 8, 'L')


    def __repr__(self):
        return '[%s, %s]' % (self.row, self.column)


    def id(self):
        return self.row * 8 + self.column


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    passes = [BoardingPass(line) for line in lines]
    if args.next:
        pass_ids = [p.id() for p in passes]
        missing_ids = [i for i in range(0, 8 * 128) if i not in pass_ids]
        for id in missing_ids:
            if id - 1 >= 0 and id - 1 not in pass_ids:
                continue
            if id + 1 >= 0 and id + 1 not in pass_ids:
                continue
            print(id)
    else:
        max_id = max(p.id() for p in passes)
        print(max_id)


if __name__ == "__main__":
    main()
