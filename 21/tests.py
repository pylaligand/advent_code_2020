#!/usr/bin/python

import unittest

from main import count_allergenless, find_allergen_list, parse_food


class Test21(unittest.TestCase):
    def test_parse_food(self):
        [food] = parse_food(['aaa b ccc dd eeeee (contains foo, bar, blah)'])
        self.assertEquals(len(food.ingredients), 5)
        self.assertTrue('aaa' in food.ingredients)
        self.assertTrue('ccc' in food.ingredients)
        self.assertEquals(len(food.allergens), 3)
        self.assertTrue('foo' in food.allergens)
        self.assertTrue('blah' in food.allergens)

    def test_example_count(self):
        foods = parse_food(l for l in EXAMPLE.splitlines() if l)
        self.assertEquals(count_allergenless(foods), 5)

    def test_example_list(self):
        foods = parse_food(l for l in EXAMPLE.splitlines() if l)
        self.assertEquals(find_allergen_list(foods), 'mxmxvkd,sqjhc,fvjkl')


EXAMPLE = '''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''

if __name__ == "__main__":
    unittest.main()
