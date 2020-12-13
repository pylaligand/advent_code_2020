#!/usr/bin/python

import argparse


class Direction(object):

    EAST = 0
    NORTH = 90
    WEST = 180
    SOUTH = 270

    _BY_CHAR = {'E': EAST, 'N': NORTH, 'W': WEST, 'S': SOUTH}
    _DELTAS = {EAST: (1, 0), NORTH: (0, 1), WEST: (-1, 0), SOUTH: (0, -1)}


    @classmethod
    def from_char(cls, char):
        return cls._BY_CHAR[char]


    @classmethod
    def rotate(cls, direction, angle):
        return (direction + angle) % 360


    @classmethod
    def forward(cls, direction, amount):
        deltas = cls._DELTAS[direction]
        return (amount * deltas[0], amount * deltas[1])


class Ship(object):

    def __init__(self, direction):
        self.direction = direction
        self.x = 0
        self.y = 0
        self.wp_x = 0
        self.wp_y = 0


    def set_waypoint(self, x, y):
        self.wp_x = x
        self.wp_y = y


    def __repr__(self):
        return '[%s, %s | %s | %s, %s]' % (self.x, self.y, self.direction, self.wp_x, self.wp_y)


class Instruction(object):

    def __init__(self, line):
        self.type = line[0]
        self.amount = int(line[1:])


    def apply_guessed(self, ship):
        if self.type == 'R':
            ship.direction = Direction.rotate(ship.direction, -self.amount)
        elif self.type == 'L':
            ship.direction = Direction.rotate(ship.direction, +self.amount)
        else:
            if self.type == 'F':
                direction = ship.direction
            else:
                direction = Direction.from_char(self.type)
            delta_x, delta_y = Direction.forward(direction, self.amount)
            ship.x += delta_x
            ship.y += delta_y


    def apply_read(self, ship):
        if self.type in ['R', 'L']:
            rotation = self.amount
            if self.type == 'R':
                rotation = 360 - rotation
            if rotation == 90:
                old_wp_x = ship.wp_x
                ship.wp_x = -ship.wp_y
                ship.wp_y = old_wp_x
            elif rotation == 180:
                ship.wp_x = -ship.wp_x
                ship.wp_y = -ship.wp_y
            elif rotation == 270:
                old_wp_x = ship.wp_x
                ship.wp_x = ship.wp_y
                ship.wp_y = -old_wp_x
        elif self.type == 'F':
            ship.x = ship.x + ship.wp_x * self.amount
            ship.y = ship.y + ship.wp_y * self.amount
        else:
            direction = Direction.from_char(self.type)
            delta_x, delta_y = Direction.forward(direction, self.amount)
            ship.wp_x += delta_x
            ship.wp_y += delta_y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    instructions = [Instruction(line) for line in lines]
    ship = Ship(Direction.EAST)

    if args.next:
        ship.set_waypoint(10, 1)
        for i in instructions:
            i.apply_read(ship)
    else:
        for i in instructions:
            i.apply_guessed(ship)
    print(abs(ship.x) + abs(ship.y))


if __name__ == "__main__":
    main()
