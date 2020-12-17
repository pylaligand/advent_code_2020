#!/usr/bin/python

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    if args.next:
        raise Exception('not implemented!')
    else:
        raise Exception('not implemented!')


if __name__ == "__main__":
    main()
