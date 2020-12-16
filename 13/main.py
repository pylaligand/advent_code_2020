#!/usr/bin/python

import argparse


def find_earliest_departure(start_time, bus_ids):
    ids = [int(c) for c in bus_ids if c != 'x']
    time, id = min(((1 + start_time // i) * i, i) for i in ids)
    return (time - start_time) * id


def expand_candidates(candidates, shift):
    '''Generates an infinite loop of items from the `candidates` generator.

    Once the generator is exhausted, its contents are shifted by `shift` and
    the generation continues.
    '''
    base = 0
    # Record observed generated items.
    record = True
    observed = []
    while True:
        source = candidates if record else observed
        for c in source:
            if record:
                observed.append(c)
            value = base * shift + c
            yield value
        record = False
        base += 1


def filter_candidates(value, delta, candidates, upper_bound):
    '''Filters the list of candidate times retaining the ones matching the given
    value/delta combo.

    Candidates are within [0; upper_bound] and "repeat" past the upper bound.
    '''
    for candidate in expand_candidates(candidates, upper_bound):
        if candidate >= upper_bound * value:
            # The new upper bound was reached, no need to test further.
            return
        time = candidate + delta
        if not time % value:
            yield candidate


def find_staggered_departure(bus_ids):
    ids = [(int(id), index) for (index, id) in enumerate(bus_ids) if id != 'x']

    # Sort by decreasing id value. The will speed things up by having a maximum
    # delta between candidates right from the get go. Technically the
    # greatest common denominators between pairs of ids should factor in, but
    # the current approach is a good approximation - especially as the two
    # biggest integers in our set are mutually prime.
    ids = sorted(ids, reverse=True)

    # The idea is to generate candidates that work for a subset of the ids, and
    # iteratively add new ids to the set.
    # A key understanding is that for two ids iA and iB, we only need to look
    # at numbers up to iA * iB at which point the two buses are guaranteed to
    # be in sync. Candidates past that point are just the earlier ones shifted
    # by a multiple of iA * iB.
    # In order to speed things up and do as little work as possible, iterating
    # through candidates is always done via generators.

    # Candidate times will always be expressed relatively to the first bus in
    # the list - the one with the biggest id.
    first_value, first_index = ids[0]
    candidates = [first_value]
    upper_bound = first_value

    for id, index in ids[1:]:
        candidates = filter_candidates(id, index - first_index, candidates, upper_bound)
        upper_bound *= id

    return next(candidates) - first_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    start_time = int(lines[0])
    bus_ids = lines[1].split(',')

    if args.next:
        print(find_staggered_departure(bus_ids))
    else:
        print(find_earliest_departure(start_time, bus_ids))


if __name__ == "__main__":
    main()
