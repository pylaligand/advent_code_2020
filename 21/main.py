#!/usr/bin/python

import argparse
from collections import namedtuple

Food = namedtuple('Food', ['ingredients', 'allergens'])


def parse_food(lines):
    result = []
    for line in lines:
        if '(' in line:
            paren_index = line.index('(')
            ingredient_list = line[:paren_index]
            allergen_list = line[paren_index + 10:line.index(')')]
        else:
            ingredient_list = line
            allergen_list = ''
        result.append(
            Food(set(i for i in ingredient_list.split(' ') if i),
                 set(a.strip() for a in allergen_list.split(','))))
    return result


def _aggregate(foods):
    return (set.union(*[f.allergens for f in foods]),
            set.union(*[f.ingredients for f in foods]))


def _find_allergenless(foods):
    allergens, ingredients = _aggregate(foods)
    suspicious = set.union(*[
        set.intersection(*[f.ingredients for f in foods if a in f.allergens])
        for a in allergens
    ])
    return ingredients - suspicious


def count_allergenless(foods):
    cleared = _find_allergenless(foods)
    return sum(sum(1 for i in f.ingredients if i in cleared) for f in foods)


def find_allergen_list(foods):
    allergens, ingredients = _aggregate(foods)
    candidates = dict(
        (a,
         set.intersection(*[f.ingredients for f in foods if a in f.allergens]))
        for a in allergens)
    dangers = {}
    while True:
        try:
            allergen, ingredient = next((a, c.pop())
                                        for (a, c) in candidates.iteritems()
                                        if len(c) == 1)
        except StopIteration:
            break
        del candidates[allergen]
        dangers[allergen] = ingredient
        for _, i in candidates.iteritems():
            if ingredient in i:
                i.remove(ingredient)
    return ','.join(i for _, i in sorted(dangers.items()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    foods = parse_food(lines)

    if args.next:
        print(find_allergen_list(foods))
    else:
        print(count_allergenless(foods))


if __name__ == "__main__":
    main()
