#!/usr/bin/python

import argparse


def find_full_chain(ratings):
    one_deltas = sum(1 for i in range(1, len(ratings))
                     if ratings[i] - ratings[i-1] == 1)
    three_deltas = sum(1 for i in range(1, len(ratings))
                       if ratings[i] - ratings[i-1] == 3)
    return one_deltas * three_deltas


def count_arrangements(ratings):
    count_for_rating = {}  # rating index --> number of paths to device
    count_for_rating[len(ratings) - 1] = 1

    def determine_count(index):
        if index in count_for_rating:
            return count_for_rating[index]
        result = 0
        for next_index in range(index + 1, len(ratings)):
            delta = ratings[next_index] - ratings[index]
            if delta > 3:
                break
            result += determine_count(next_index)
        count_for_rating[index] = result
        return result

    return determine_count(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    ratings = [int(l) for l in lines]
    outlet_rating = 0
    device_rating = max(ratings) + 3
    ratings.extend([outlet_rating, device_rating])
    ratings = sorted(ratings)

    if args.next:
        print(count_arrangements(ratings))
    else:
        print(find_full_chain(ratings))


if __name__ == "__main__":
    main()
