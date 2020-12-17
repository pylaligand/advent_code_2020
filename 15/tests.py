#!/usr/bin/python

import unittest

from main import find_nth


class Test15(unittest.TestCase):

    def test_find_nth(self):
        starting_numbers = [0, 3, 6]
        self.assertEquals(find_nth(4, starting_numbers), 0)
        self.assertEquals(find_nth(5, starting_numbers), 3)
        self.assertEquals(find_nth(6, starting_numbers), 3)
        self.assertEquals(find_nth(7, starting_numbers), 1)
        self.assertEquals(find_nth(8, starting_numbers), 0)
        self.assertEquals(find_nth(9, starting_numbers), 4)
        self.assertEquals(find_nth(10, starting_numbers), 0)


    def test_find_nth_high(self):
        nth = 30000000
        self.assertEquals(find_nth(nth, [0, 3, 6]), 175594)
        self.assertEquals(find_nth(nth, [1, 3, 2]), 2578)
        self.assertEquals(find_nth(nth, [2, 1, 3]), 3544142)
        self.assertEquals(find_nth(nth, [1, 2, 3]), 261214)
        self.assertEquals(find_nth(nth, [2, 3, 1]), 6895259)
        self.assertEquals(find_nth(nth, [3, 2, 1]), 18)
        self.assertEquals(find_nth(nth, [3, 1, 2]), 362)


if __name__ == "__main__":
    unittest.main()
