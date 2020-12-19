#!/usr/bin/python

import argparse
from collections import namedtuple
from itertools import chain
import re

Character = namedtuple('Character', ["value"])
Combo = namedtuple('Combo', ["rules"])
Pipe = namedtuple('Pipe', ["combos"])


def _parse_rule(line):
    parse_combo = lambda input: Combo([int(t) for t in input.strip().split()])
    index_str, value = line.split(':')
    index = int(index_str.strip())
    if '"' in value:
        match = re.match('^\s*"(\w)"\s*$', value)
        return (index, Character(match.group(1)))
    elif '|' in value:
        return (index, Pipe([parse_combo(c) for c in value.split('|')]))
    else:
        return (index, parse_combo(value))


class Ruleset(object):
    def __init__(self, lines):
        self._rules = dict(_parse_rule(l) for l in lines)
        self._patterns = {}  # index --> (pattern, max_len)
        self._max_len = 0

    def __repr__(self):
        return self._rules.__repr__()

    def replace(self, line):
        index, rule = _parse_rule(line)
        self._rules[index] = rule
        self._patterns = {}

    def set_max_len(self, value):
        self._max_len = value

    def get_pattern(self, index):
        if index in self._patterns:
            return self._patterns[index]

        def get_combo_pattern(combo):
            patterns = [self.get_pattern(r) for r in combo.rules]
            pattern = ''.join(p for p, _ in patterns)
            max_len = sum(m for _, m in patterns)
            return (pattern, max_len)

        if not index in self._rules:
            raise Exception('Rule %s unknown' % index)
        rule = self._rules[index]

        if isinstance(rule, Character):
            result = (rule.value, 1)

        elif isinstance(rule, Combo):
            result = get_combo_pattern(rule)

        elif isinstance(rule, Pipe):
            self_ref_count = sum(1 for c in rule.combos for r in c.rules
                                 if r == index)
            if self_ref_count:
                if not self._max_len:
                    raise Exception('Can\'t loop %s without a maximum' % index)
                if self_ref_count > 1:
                    raise Exception('Too many loops for %s: %s' %
                                    (index, self_ref_count))
                if len(rule.combos) > 2:
                    raise Exception('That\'s too many combos for %s Bob' %
                                    index)

                loop_combo = next(c for c in rule.combos
                                  if any(r == index for r in c.rules))
                other_combo = next(c for c in rule.combos if c != loop_combo)
                loop_index = loop_combo.rules.index(index)

                if len(loop_combo.rules) == 1:
                    raise Exception('That\'s impossible to resolve my friend')

                elif len(loop_combo.rules) == 2:
                    # If the loop is combined with a single other rule, check
                    # that the other combo only contains that other rule.
                    if (len(other_combo.rules) != 1 or other_combo.rules[0] !=
                            loop_combo.rules[1 - loop_index]):
                        raise Exception('Can\'t loop %s in %s' %
                                        (index, loop_combo))

                    base, _ = get_combo_pattern(other_combo)
                    result = (('(?:%s)+' % base), self._max_len)

                elif len(loop_combo.rules) == 3:
                    # Check that the looping rule is always in the middle of two
                    # other rules, and that these other two are reflected in the
                    # same order in the other combo.
                    if (loop_index != 1 or len(other_combo.rules) != 2
                            or other_combo.rules[0] != loop_combo.rules[0]
                            or other_combo.rules[1] != loop_combo.rules[2]):
                        raise Exception('This is too weird for %s: %s' %
                                        (index, other_combo))

                    first_pattern, first_len = self.get_pattern(
                        loop_combo.rules[0])
                    second_pattern, second_len = self.get_pattern(
                        loop_combo.rules[2])
                    max_len = 0
                    options = []
                    while max_len < self._max_len:
                        max_len += first_len + second_len
                        latest = options[-1] if options else ''
                        options.append(''.join(
                            [first_pattern, latest, second_pattern]))
                    result = ('(?:%s)' % '|'.join(options), max_len)

            else:
                patterns = [get_combo_pattern(c) for c in rule.combos]
                pattern = '(?:' + '|'.join(p for p, _ in patterns) + ')'
                max_len = max(m for _, m in patterns)
                result = (pattern, max_len)

        self._patterns[index] = result
        return result

    def match(self, rule, message):
        pattern = self.get_pattern(rule)[0]
        pattern = '^' + pattern + '$'
        return bool(re.match(pattern, message))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    messages_index = lines.index('')
    rules = Ruleset(lines[:messages_index])
    messages = lines[messages_index + 1:]

    if args.next:
        rules.replace('8: 42 | 42 8')
        rules.replace('11: 42 31 | 42 11 31')
        rules.set_max_len(max(len(m) for m in messages))
    print(sum(1 for m in messages if rules.match(0, m)))


if __name__ == "__main__":
    main()
