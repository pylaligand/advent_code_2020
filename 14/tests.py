#!/usr/bin/python

import unittest

from main import MemoryMask, ValueMask


class Test14(unittest.TestCase):

    def test_value_mask(self):
        mask = ValueMask('mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')
        self.assertEquals(mask.apply(11), 73)
        self.assertEquals(mask.apply(101), 101)
        self.assertEquals(mask.apply(0), 64)


    def test_memory_mask(self):
        mask = MemoryMask('mask = 000000000000000000000000000000X1001X')
        self.assertItemsEqual(mask.apply(42), [26, 27, 58, 59])
        mask = MemoryMask('mask = 00000000000000000000000000000000X0XX')
        self.assertItemsEqual(mask.apply(26), [16, 17, 18, 19, 24, 25, 26, 27])


if __name__ == "__main__":
    unittest.main()
