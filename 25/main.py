#!/usr/bin/python

import argparse


def _compute_public_key(base, subject, loop):
    result = base
    for _ in range(0, loop):
        result = (result * subject) % 20201227
    return result


def compute_loop_size(public_key):
    value = 1
    loop = 0
    while True:
        loop += 1
        value = _compute_public_key(value, 7, 1)
        if value == public_key:
            break
    return loop


def find_encryption_key(card_key, door_key):
    card_loop = compute_loop_size(card_key)
    return _compute_public_key(1, door_key, card_loop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    card_key = int(lines[0])
    door_key = int(lines[1])
    print(find_encryption_key(card_key, door_key))


if __name__ == "__main__":
    main()
