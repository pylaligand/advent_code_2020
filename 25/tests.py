#!/usr/bin/python

import unittest

from main import compute_loop_size, find_encryption_key


class Test25(unittest.TestCase):
    def test_compute_loop_size(self):
        self.assertEquals(compute_loop_size(5764801), 8)
        self.assertEquals(compute_loop_size(17807724), 11)

    def test_find_encryption_key(self):
        self.assertEquals(find_encryption_key(5764801, 17807724), 14897079)


if __name__ == "__main__":
    unittest.main()
