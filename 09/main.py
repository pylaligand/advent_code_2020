#!/usr/bin/python

import argparse


def has_sum(total, window):
    for index, value in enumerate(window):
        candidates = [v for i, v in enumerate(window) if i != index]
        if total - value in candidates:
            return True
    return False


def find_first_intruder(numbers):
    for index in range(25, len(numbers)):
        current = numbers[index]
        window = numbers[index - 25:index]
        if not has_sum(current, window):
            return current
    raise Exception('Could not find any intruder')


def find_matching_range(total, numbers):
    for start_index in range(len(numbers)):
        for index in range(start_index + 1, len(numbers)):
            window = numbers[start_index:index]
            value = sum(window)
            if value == total:
                return min(window) + max(window)
            if value > total:
                break
    raise Exception('Could not locate range')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    numbers = [int(l) for l in lines]
    intruder = find_first_intruder(numbers)

    if args.next:
        print(find_matching_range(intruder, numbers))
    else:
        print(intruder)


if __name__ == "__main__":
    main()
