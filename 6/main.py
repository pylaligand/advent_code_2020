#!/usr/bin/python

import argparse


class Group(object):

    def __init__(self, lines):
        self.answers = [set(c for c in line) for line in lines]

    def positive_count(self):
        return len(set.union(*self.answers))

    def common_count(self):
        return len(set.intersection(*self.answers))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    groups = []
    group_lines = []
    while True:
        if lines:
            current = lines.pop(0)
            if current:
                group_lines.append(current)
                continue
        if group_lines:
            groups.append(Group(group_lines))
            group_lines = []
        if not lines:
            break

    if args.next:
        total = sum(g.common_count() for g in groups)
        print(total)
    else:
        total = sum(g.positive_count() for g in groups)
        print(total)


if __name__ == "__main__":
    main()
