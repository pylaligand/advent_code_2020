#!/usr/bin/python

import argparse
import operator


class Field(object):

    def __init__(self, line):
        name, intervals = line.split(':')
        self.name = name
        self.intervals = []
        for i in intervals.strip().split(' or '):
            bounds = i.split('-')
            self.intervals.append(range(int(bounds[0]), int(bounds[1]) + 1))


    def __repr__(self):
        return self.name


    def contains(self, value):
        return any(value in i for i in self.intervals)


class Ticket(object):

    def __init__(self, line):
        self.values = [int(v) for v in line.split(',')]


    def __repr__(self):
        return '%s...' % self.values[0]


def find_invalid_nearby(fields, nearby_tickets):
    return sum(v for t in nearby_tickets for v in t.values
               if not any(f.contains(v) for f in fields))


def decipher_ticket(fields, my_ticket, nearby_tickets):
    # Filter invalid nearby tickets out.
    valid_tickets = [t for t in nearby_tickets
                     if all(any(f.contains(v) for f in fields) for v in t.values)]

    # Compute the fields that could match a given position.
    positions = {}  # index --> [fields]
    for i in range(0, len(my_ticket.values)):
        for f in fields:
            if all(f.contains(t.values[i]) for t in valid_tickets):
                positions.setdefault(i, []).append(f)

    # Identify fields which only have a single option, remove them from all
    # positions, rinse and repeat.
    assigned_fields = [None] * len(my_ticket.values)
    while positions:
        i, f = next((i, f) for (i, f) in positions.iteritems() if len(f) == 1)
        field = f[0]
        assigned_fields[i] = field
        del positions[i]
        for f in positions.values():
            f.remove(field)

    # Compute the departure values.
    values = [my_ticket.values[i] for (i, f) in enumerate(assigned_fields)
              if f.name.startswith('departure')]
    return reduce(operator.mul, values, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    lines = [l for l in lines if l]
    ticket_index = lines.index('your ticket:')
    nearby_index = lines.index('nearby tickets:')

    fields = [Field(l) for l in lines[:ticket_index]]
    my_ticket = Ticket(lines[ticket_index + 1])
    nearby_tickets = [Ticket(l) for l in lines[nearby_index + 1:]]

    if args.next:
        print(decipher_ticket(fields, my_ticket, nearby_tickets))
    else:
        print(find_invalid_nearby(fields, nearby_tickets))


if __name__ == "__main__":
    main()
