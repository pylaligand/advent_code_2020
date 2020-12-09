#!/usr/bin/python

import argparse
from collections import namedtuple
import re


Entry = namedtuple('Entry', ['password', 'char', 'ref_one', 'ref_two'])


def parse_entry(raw_entry):
    pattern = '(\d+)-(\d+) (\w): (\w+)'
    match = re.match(pattern, raw_entry)
    if not match:
        raise Exception('Could not parse: ' + entry)
    return Entry(ref_one=int(match.group(1)),
                 ref_two=int(match.group(2)),
                 char=match.group(3),
                 password=match.group(4))


def is_valid(entry):
    count = sum(1 for c in entry.password if c == entry.char)
    return entry.ref_one <= count and count <= entry.ref_two


def is_really_valid(entry):
    one_matches = entry.password[entry.ref_one - 1] == entry.char
    two_matches = entry.password[entry.ref_two - 1] == entry.char
    return one_matches != two_matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        entries = [parse_entry(l.strip()) for l in input_file.readlines()]

    # valid_passwords = sum(1 for e in entries if is_valid(e))
    valid_passwords = sum(1 for e in entries if is_really_valid(e))

    print(valid_passwords)


if __name__ == "__main__":
    main()
