#!/usr/bin/python

import argparse
import re


class BagSpec(object):

    def __init__(self, line):
        name_match = re.match('^(.+) bags contain', line)
        if name_match:
            self.name = name_match.group(1)
        contents = re.findall('(\d+) ([^\.,]+) bags?[\.,]', line)
        self.contents = dict((n, int(q)) for (q, n) in contents)


    def __repr__(self):
        return self.name + '[' + str(self.contents) + ']'


    def can_contain(self):
        return set(self.contents.keys())


def count_containing_bags(bag_name, specs):
    outer_bags = set()
    inner_bags = set([bag_name])
    while inner_bags:
        inner_bags = set(s.name for s in specs
                         if s.can_contain().intersection(inner_bags))
        outer_bags.update(inner_bags)
    return len(outer_bags)


def count_contained_bags(bag_name, specs):
    counts = {}

    def count(name):
        if name not in counts:
            spec = next(s for s in specs if s.name == name)
            counts[name] = sum(q * (1 + count(n)) for (n, q) in spec.contents.iteritems())
        return counts[name]

    return count(bag_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    specs = [BagSpec(line) for line in lines]

    if args.next:
        print(count_contained_bags('shiny gold', specs))
    else:
        print(count_containing_bags('shiny gold', specs))



if __name__ == "__main__":
    main()
