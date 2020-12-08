#!/usr/bin/python

import argparse
from contextlib import contextmanager
import re


class Type(object):
    Accumulate = 'acc'
    Jump = 'jmp'
    Noop = 'nop'


class Instruction(object):

    def __init__(self, line):
        match = re.match('^(\w{3}) ([\+-]?\d+)$', line)
        self.type = match.group(1)
        self.value = int(match.group(2))


    def __repr__(self):
        return '(%s, %s)' % (self.type, self.value)


    def can_flip(self):
        return self.type != Type.Accumulate


    @contextmanager
    def flip(self):
        if not self.can_flip():
            raise 'Cannot flip %s' % self
        try:
            self.type = Type.Jump if self.type == Type.Noop else Type.Noop
            yield
        finally:
            self.type = Type.Jump if self.type == Type.Noop else Type.Noop


def run(instructions):
    '''Runs the given instruction set.

    Returns a tuple (is_looping, accumulator).
    If "is_looping", the program reached a looping point; execution is stopped
    right before an instruction gets executed a second time. If not, then the
    program terminated normally. In both cases "accumulator" contains the
    accumulated value after the last executed instruction.
    '''
    index = 0
    visited = set()
    accumulator = 0
    while True:
        if index in visited:
            return (True, accumulator)
        visited.add(index)
        ins = instructions[index]
        if ins.type == Type.Jump:
            index += ins.value
        else:
            if ins.type == Type.Accumulate:
                accumulator += ins.value
            index += 1
        if index == len(instructions):
            return (False, accumulator)
        if index < 0 or index > len(instructions):
            raise 'Reached invalid instruction index: %d' % index


def find_fix(instructions):
    for ins in instructions:
        if not ins.can_flip():
            continue
        with ins.flip():
            is_loop, accumulator = run(instructions)
            if not is_loop:
                return accumulator
    raise 'Could not find terminating program!'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    instructions = [Instruction(line) for line in lines]

    if args.next:
        print(find_fix(instructions))
    else:
        reached_loop, accumulator = run(instructions)
        if not reached_loop:
            raise 'Did not detect a loop :('
        print(accumulator)


if __name__ == "__main__":
    main()
