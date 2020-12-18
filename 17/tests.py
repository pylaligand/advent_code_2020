#!/usr/bin/python

import unittest

from main import Dimension, DimensionState


class TestDimensionState(unittest.TestCase):

    def test_get_set(self):
        state = DimensionState(with_4th=False)
        self.assertFalse(state.is_active(1, 2, 3, 0))
        state.set_active(1, 2, 3, 0, True)
        self.assertTrue(state.is_active(1, 2, 3, 0))
        self.assertFalse(state.is_active(101, 22, 314, 0))


    def test_extent(self):
        state = DimensionState(with_4th=False)
        x_range, y_range, z_range, w_range = state.extent()
        self.assertEquals(len(x_range), 0)
        self.assertEquals(len(y_range), 0)
        self.assertEquals(len(z_range), 0)

        state.set_active(1, 20, 300, 0, True)
        x_range, y_range, z_range, w_range = state.extent()
        self.assertEquals(len(x_range), 3)
        self.assertEquals(len(y_range), 3)
        self.assertEquals(len(z_range), 3)
        self.assertEquals(list(x_range), [0, 1, 2])
        self.assertEquals(list(y_range), [19, 20, 21])
        self.assertEquals(list(z_range), [299, 300, 301])

        state.set_active(5, 20, 300, 0, True)
        x_range, y_range, z_range, w_range = state.extent()
        self.assertEquals(len(x_range), 7)
        self.assertEquals(len(y_range), 3)
        self.assertEquals(len(z_range), 3)
        self.assertEquals(list(x_range), [0, 1, 2, 3, 4, 5, 6])
        self.assertEquals(list(y_range), [19, 20, 21])
        self.assertEquals(list(z_range), [299, 300, 301])


    def test_active_count(self):
        state = DimensionState(with_4th=False)
        self.assertEquals(state.active_count(), 0)
        state.set_active(1, 2, 3, 0, True)
        self.assertEquals(state.active_count(), 1)
        state.set_active(10, 200, 3000, 0, True)
        self.assertEquals(state.active_count(), 2)
        state.set_active(1, 2, 3, 0, False)
        self.assertEquals(state.active_count(), 1)



class TestDimension(unittest.TestCase):

    def test_initialization(self):
        lines = ['.#.',
                 '..#',
                 '###']
        dim = Dimension(lines, with_4th=False)
        self.assertTrue(dim.is_active(0, 1, 0, 0))
        self.assertFalse(dim.is_active(1, 1, 0, 0))
        self.assertFalse(dim.is_active(0, 1, 1, 0))


    def test_step(self):
        lines = ['.#.',
                 '..#',
                 '###']
        dim = Dimension(lines, with_4th=False)
        dim.step()
        self.assertFalse(dim.is_active(0, 1, 0, 0))
        self.assertTrue(dim.is_active(1, 0, -1, 0))
        self.assertTrue(dim.is_active(2, 1, 0, 0))
        self.assertTrue(dim.is_active(3, 1, 1, 0))


    def test_six_steps(self):
        lines = ['.#.',
                 '..#',
                 '###']
        dim = Dimension(lines, with_4th=False)
        for i in range(6):
            dim.step()
        self.assertEquals(dim.active_count(), 112)


    def test_six_steps_with_4th(self):
        lines = ['.#.',
                 '..#',
                 '###']
        dim = Dimension(lines, with_4th=True)
        for i in range(6):
            dim.step()
        self.assertEquals(dim.active_count(), 848)


if __name__ == "__main__":
    unittest.main()
