#!/usr/bin/python

import argparse
from copy import copy
import re


def parse_hands(lines):
    result = {}
    lines = [l for l in lines if l]
    while lines:
        line = lines.pop(0)
        id = int(re.match('^Player (\d+):$', line).group(1))
        cards = []
        while lines:
            if lines[0].startswith('Player'):
                break
            cards.append(int(lines.pop(0)))
        result[id] = cards
    return result[1], result[2]


def deck_score(deck):
    return sum((i + 1) * c for (i, c) in enumerate(reversed(deck)))


def find_normal_score(deck_one, deck_two):
    while deck_one and deck_two:
        card_one = deck_one.pop(0)
        card_two = deck_two.pop(0)
        if card_one > card_two:
            deck_one.insert(len(deck_one), card_one)
            deck_one.insert(len(deck_one), card_two)
        else:
            deck_two.insert(len(deck_two), card_two)
            deck_two.insert(len(deck_two), card_one)
    return deck_score(deck_one if deck_one else deck_two)


def recursive_play(deck_one, deck_two):
    rounds = set()
    compute_game_hash = lambda d_one, d_two: hash((tuple(d_one), tuple(d_two)))
    while deck_one and deck_two:
        game_hash = compute_game_hash(deck_one, deck_two)
        if game_hash in rounds:
            return (True, deck_score(deck_one))
        rounds.add(game_hash)
        card_one = deck_one.pop(0)
        card_two = deck_two.pop(0)
        if len(deck_one) >= card_one and len(deck_two) >= card_two:
            one_wins, _ = recursive_play(copy(deck_one[:card_one]),
                                         copy(deck_two[:card_two]))
        else:
            one_wins = card_one > card_two
        if one_wins:
            deck_one.insert(len(deck_one), card_one)
            deck_one.insert(len(deck_one), card_two)
        else:
            deck_two.insert(len(deck_two), card_two)
            deck_two.insert(len(deck_two), card_one)
    return (bool(deck_one), deck_score(deck_one if deck_one else deck_two))


def find_recursive_score(deck_one, deck_two):
    _, score = recursive_play(deck_one, deck_two)
    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    deck_one, deck_two = parse_hands(lines)

    if args.next:
        print(find_recursive_score(deck_one, deck_two))
    else:
        print(find_normal_score(deck_one, deck_two))


if __name__ == "__main__":
    main()
