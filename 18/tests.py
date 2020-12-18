#!/usr/bin/python

import unittest

from main import compute_precedence, compute_serial


class Test18(unittest.TestCase):

    def assertComputeSerial(self, line, result):
        self.assertEquals(compute_serial(line), result)


    def test_compute_serial_simple(self):
        self.assertComputeSerial('2', 2)
        self.assertComputeSerial('   12  ', 12)
        self.assertComputeSerial('3 * 5', 15)
        self.assertComputeSerial('300 + 14', 314)
        self.assertComputeSerial('30 + 1 * 2', 62)


    def test_compute_serial_examples(self):
        self.assertComputeSerial('1 + 2 * 3 + 4 * 5 + 6', 71)
        self.assertComputeSerial('1 + (2 * 3) + (4 * (5 + 6))', 51)
        self.assertComputeSerial('2 * 3 + (4 * 5)', 26)
        self.assertComputeSerial('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437)
        self.assertComputeSerial('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240)
        self.assertComputeSerial('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632)


    def assertComputePrecedence(self, line, result):
        self.assertEquals(compute_precedence(line), result)


    def test_compute_precedence_simple(self):
        self.assertComputePrecedence('2', 2)
        self.assertComputePrecedence('   12  ', 12)
        self.assertComputePrecedence('3 * 5', 15)
        self.assertComputePrecedence('300 + 14', 314)
        self.assertComputePrecedence('30 + 1 * 2', 62)
        self.assertComputePrecedence('30 * 1 + 2', 90)


    def test_compute_precedence_examples(self):
        self.assertComputePrecedence('1 + 2 * 3 + 4 * 5 + 6', 231)
        self.assertComputePrecedence('1 + (2 * 3) + (4 * (5 + 6))', 51)
        self.assertComputePrecedence('2 * 3 + (4 * 5)', 46)
        self.assertComputePrecedence('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445)
        self.assertComputePrecedence('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060)
        self.assertComputePrecedence('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340)


if __name__ == "__main__":
    unittest.main()
