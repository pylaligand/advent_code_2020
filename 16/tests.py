#!/usr/bin/python

import unittest

from main import Field, Ticket


class Test16(unittest.TestCase):

    def test_field(self):
        field = Field('duration: 39-525')
        self.assertEquals(field.name, 'duration')
        self.assertTrue(field.contains(314))
        self.assertFalse(field.contains(1020))

        field = Field('grade: 1-46 or 72-95 or 314-315')
        self.assertEquals(field.name, 'grade')
        self.assertTrue(field.contains(1))
        self.assertFalse(field.contains(101))
        self.assertTrue(field.contains(315))


    def test_ticket(self):
        ticket = Ticket('320,347,742,887,648,3,389,257,143,6')
        self.assertTrue(742 in ticket.values)
        self.assertTrue(ticket.values[1] == 347)
        self.assertFalse(1020 in ticket.values)


if __name__ == "__main__":
    unittest.main()
