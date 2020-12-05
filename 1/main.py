#!/usr/bin/python

import argparse


def find_pair_internal(numbers, target):
    for i in range(len(numbers) - 1):
        current = numbers[i]
        for j in range(i + 1, len(numbers)):
            check = numbers[j]
            if current + check == target:
                return (current, check)
    return (None, None)


def find_pair(numbers):
    a, b = find_pair_internal(numbers, 2020)
    if a is None:
        print('Could not find result :(')
        return
    print('%s + %s = 2020' % (a, b))
    print('Result: %s' % (a * b))


def find_triplet(numbers):
    for i in range(len(numbers) - 2):
        current = numbers[i]
        a, b = find_pair_internal(numbers[i + 1:], 2020 - current)
        if a is None:
            continue
        print('%s + %s + %s = 2020' % (current, a, b))
        print('Result: %s' % (current * a * b))
        return
    print('Could not find result :(')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        numbers = [int(l.strip()) for l in input_file.readlines()]

    # find_pair(numbers)
    find_triplet(numbers)


if __name__ == "__main__":
    main()
