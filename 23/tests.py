#!/usr/bin/python

import unittest

from main import parse_cups, play_n_easy_moves, play_n_hard_moves, Node


class Test23(unittest.TestCase):
    def test_node(self):
        node1 = Node(1)
        self.assertItemsEqual(node1.values(), [1])
        node2 = Node(2)
        node3 = Node(3)
        node1.add(node2)
        self.assertEquals(node1.prev, node2)
        self.assertEquals(node1.next, node2)
        self.assertEquals(node2.prev, node1)
        self.assertEquals(node2.next, node1)
        self.assertEquals(node3.prev, node3)
        self.assertEquals(node3.next, node3)
        self.assertItemsEqual(node1.values(), [1, 2])
        node2.add(node3)
        self.assertEquals(node1.prev, node3)
        self.assertEquals(node1.next, node2)
        self.assertEquals(node2.prev, node1)
        self.assertEquals(node2.next, node3)
        self.assertEquals(node3.prev, node2)
        self.assertEquals(node3.next, node1)
        self.assertItemsEqual(node1.values(), [1, 2, 3])
        node1.remove(1)
        self.assertEquals(node1.prev, node3)
        self.assertEquals(node1.next, node3)
        self.assertEquals(node2.prev, None)
        self.assertEquals(node2.next, None)
        self.assertEquals(node3.prev, node1)
        self.assertEquals(node3.next, node1)
        self.assertItemsEqual(node1.values(), [1, 3])

    def test_play_ten_easy_moves(self):
        self.assertEquals(play_n_easy_moves(parse_cups('389125467'), 10),
                          '92658374')

    def test_play_hundred_easy_moves(self):
        self.assertEquals(play_n_easy_moves(parse_cups('389125467'), 100),
                          '67384529')

    def test_play_n_hard_moves(self):
        self.assertEquals(play_n_hard_moves(parse_cups('389125467'), 10000000),
                          '149245887792')


if __name__ == "__main__":
    unittest.main()
