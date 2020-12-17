#!/usr/bin/python

import argparse


def find_nth(nth, starting_numbers):
    spotted = {}  # number --> turn spotted
    for i, n in enumerate(starting_numbers[:-1]):
        spotted[n] = i + 1
    turn = len(starting_numbers)
    number = starting_numbers[-1]
    while True:
        if turn == nth:
            break
        if number not in spotted:
            spotted[number] = turn
            number = 0
        else:
            new_number = turn - spotted[number]
            spotted[number] = turn
            number = new_number
        turn += 1
    return number


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    starting_numbers = [8, 11, 0, 19, 1, 2]

    if args.next:
        print(find_nth(30000000, starting_numbers))
    else:
        print(find_nth(2020, starting_numbers))


if __name__ == "__main__":
    main()
