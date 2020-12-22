#!/usr/bin/python

import unittest

from main import find_normal_score, find_recursive_score, parse_hands


class Test22(unittest.TestCase):
    def test_find_normal_score(self):
        d_one, d_two = parse_hands(EXAMPLE.splitlines())
        self.assertEquals(find_normal_score(d_one, d_two), 306)

    def test_find_recursive_score(self):
        d_one, d_two = parse_hands(EXAMPLE.splitlines())
        self.assertEquals(find_recursive_score(d_one, d_two), 291)

    def test_recursion(self):
        d_one, d_two = parse_hands(RECURSIVE_EXAMPLE.splitlines())
        find_recursive_score(d_one, d_two)


EXAMPLE = '''
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''

RECURSIVE_EXAMPLE = '''
Player 1:
43
19

Player 2:
2
29
14
'''

if __name__ == "__main__":
    unittest.main()
