#!/usr/bin/python

import argparse
import itertools
import re


REQUIRED_ATTRS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


class Passport(object):

    def __init__(self, lines):
        raw_attrs = itertools.chain.from_iterable([line.split() for line in lines])
        self.attrs = dict(attr.split(':') for attr in raw_attrs)


    def __repr__(self):
        return self.attrs.__str__()


    def is_valid(self):
        return all(a in self.attrs for a in REQUIRED_ATTRS)


    def _validate_year(self, name, min, max):
        try:
            year = int(self.attrs[name])
            return min <= year and year <= max
        except ValueError:
            return False


    def _validate_height(self):
        match = re.match('^(\d+)(cm|in)$', self.attrs['hgt'])
        if not match:
            return False
        value = int(match.group(1))
        unit = match.group(2)
        if unit == 'cm':
            return 150 <= value and value <= 193
        else:
            return 59 <= value and value <= 76


    def _validate_hair_color(self):
        return re.match('^#[0-9a-f]{6}$', self.attrs['hcl'])


    def _validate_eye_color(self):
        return self.attrs['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


    def _validate_passport_id(self):
        return re.match('^\d{9}$', self.attrs['pid'])


    def is_really_valid(self):
        return (self.is_valid() and
                self._validate_year('byr', 1920, 2002) and
                self._validate_year('iyr', 2010, 2020) and
                self._validate_year('eyr', 2020, 2030) and
                self._validate_height() and
                self._validate_hair_color() and
                self._validate_eye_color() and
                self._validate_passport_id())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    passports = []
    passport_lines = []
    while True:
        if lines:
            current = lines.pop(0)
            if current:
                passport_lines.append(current)
                continue
        if passport_lines:
            passports.append(Passport(passport_lines))
            passport_lines = []
        if not lines:
            break

    print(passports)

    if not args.next:
        n_valid = sum(1 for p in passports if p.is_valid())
    else:
        n_valid = sum(1 for p in passports if p.is_really_valid())
    print(n_valid)


if __name__ == "__main__":
    main()
