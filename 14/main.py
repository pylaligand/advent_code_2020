#!/usr/bin/python

import argparse
import re


class Assignment(object):

    def __init__(self, line):
        match = re.match('^mem\[(\d+)\] = (\d+)$', line)
        self.address = int(match.group(1))
        self.value = int(match.group(2))


class ValueMask(object):

    def __init__(self, line):
        bits = re.match('^mask = (.+)$', line).group(1)
        self.remover = 0
        self.adder = 0
        for i, v in enumerate(bits):
            if v == 'X':
                continue
            self.remover |= 1 << (len(bits) - 1 - i)
            if v == '1':
                self.adder |= 1 << (len(bits) - 1 - i)
        self.remover = ~self.remover


    def __repr__(self):
        return 'r=%s; a=%s' % (bin(~self.remover), bin(self.adder))


    def apply(self, value):
        return (value & self.remover) | self.adder


def compute_memory_v1(lines):
    memory = {}
    current_mask = None
    for line in lines:
        if line.startswith('mask'):
            current_mask = ValueMask(line)
            continue
        op = Assignment(line)
        memory[op.address] = current_mask.apply(op.value)
    return sum(v for v in memory.values())


class MemoryMask(object):

    def __init__(self, line):
        bits = re.match('^mask = (.+)$', line).group(1)
        self.remover = 0
        self.adders = [0]
        for i, v in enumerate(bits):
            if v == '0':
                continue
            self.remover |= 1 << (len(bits) - 1 - i)
            new_adders = [a | (1 << (len(bits) - 1 - i)) for a in self.adders]
            if v == '1':
                self.adders = new_adders
            else:
                self.adders.extend(new_adders)
        self.remover = ~self.remover


    def __repr__(self):
        return 'r=%s; a=%s' % (bin(~self.remover), ','.join(bin(a) for a in self.adders))


    def apply(self, address):
        return [((address & self.remover) | adder) for adder in self.adders]


def compute_memory_v2(lines):
    memory = {}
    current_mask = None
    for line in lines:
        if line.startswith('mask'):
            current_mask = MemoryMask(line)
            continue
        op = Assignment(line)
        for address in current_mask.apply(op.address):
            memory[address] = op.value
    return sum(v for v in memory.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    if args.next:
        print(compute_memory_v2(lines))
    else:
        print(compute_memory_v1(lines))


if __name__ == "__main__":
    main()
