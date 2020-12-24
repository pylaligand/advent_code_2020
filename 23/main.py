#!/usr/bin/python

import argparse
from itertools import chain


def parse_cups(cups):
    return [int(c) for c in cups]


class Node(object):
    def __init__(self, value):
        self.value = value
        self.prev = self
        self.next = self

    def __repr__(self):
        return 'N(%s)' % self.value

    def __str__(self):
        return repr(self)

    def set_next(self, node):
        self.next = node
        if node:
            node.prev = self

    def set_prev(self, node):
        self.prev = node
        if node:
            node.next = self

    def remove(self, n):
        if n == 0:
            return None
        result = self.next
        result.set_prev(None)
        new_next = self.next
        for _ in range(0, n):
            new_next = new_next.next
        new_next.prev.set_next(None)
        self.set_next(new_next)
        return result

    def add(self, node):
        old_next = self.next
        last = node.prev
        if not last:
            last = node
            while last.next != None and last.next != node:
                last = last.next
        self.set_next(node)
        old_next.set_prev(last)

    def values(self):
        current = self
        result = []
        while True:
            result.append(current.value)
            if current.next == self or current.next == None:
                break
            current = current.next
        return result


class Solver(object):
    def __init__(self, values, pad=None):
        self._nodes = {}  # value --> Node
        self._current = None
        self._min = min(values)
        max_value = max(values)
        current = None
        if pad:
            iter = chain(values, range(max_value + 1, pad + 1))
            self._max = pad
        else:
            iter = values
            self._max = max_value
        for v in iter:
            node = Node(v)
            self._nodes[v] = node
            if not self._current:
                self._current = node
            if current:
                current.add(node)
            current = node

    def play(self, n):
        for _ in range(0, n):
            removed = self._current.remove(3)
            removed_values = removed.values()
            dest_value = self._current.value - 1
            while True:
                if dest_value < self._min:
                    dest_value = self._max
                if dest_value not in removed_values:
                    break
                dest_value -= 1
            dest_node = self._nodes[dest_value]
            dest_node.add(removed)
            self._current = self._current.next
        return self

    def order_after_one(self):
        one = self._nodes[1]
        result = ''
        current = one.next
        while current != one:
            result += str(current.value)
            current = current.next
        return result

    def one_neighbors(self):
        one = self._nodes[1]
        return str(one.next.value * one.next.next.value)


def play_n_easy_moves(cups, n):
    return Solver(cups).play(n).order_after_one()


def play_n_hard_moves(cups, n):
    return Solver(cups, pad=1000000).play(n).one_neighbors()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    cups = parse_cups('685974213')

    if args.next:
        print(play_n_hard_moves(cups, 10000000))
    else:
        print(play_n_easy_moves(cups, 100))


if __name__ == "__main__":
    main()
