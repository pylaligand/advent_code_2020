#!/usr/bin/python

import unittest

from main import MONSTER, assemble, find_corners, find_monster, parse_tiles, Assembly, Constraint, Edge, PlacedTile, TileState


class Test20(unittest.TestCase):
    def test_parse_tiles(self):
        tiles = parse_tiles(EXAMPLE.splitlines())
        self.assertEquals(len(tiles), 9)
        self.assertTrue(1427 in tiles)
        self.assertFalse(12345 in tiles)

    def test_assembly_generate_constraints(self):
        tiles = parse_tiles(EXAMPLE.splitlines())
        assembly = Assembly(tiles)
        tile_id = 3079
        tile_state = TileState(flipped=False, rotation=0)
        assembly._pieces = {(0, 0): PlacedTile(tile_id, tile_state)}
        spots = assembly.generate_spots()
        top_edge_value = tiles[tile_id].get_edge(Edge.TOP, tile_state)
        self.assertEquals(spots[(-1, 0)],
                          [Constraint(Edge.BOTTOM, top_edge_value)])

    def test_find_corners(self):
        tiles = parse_tiles(EXAMPLE.splitlines())
        self.assertEquals(find_corners(tiles), 20899048083289)

    def test_tile_snap(self):
        tiles = parse_tiles(EXAMPLE.splitlines())
        tile = tiles[2311]

        snap = tile.snap(TileState(flipped=False, rotation=0))
        self.assertTrue(snap.get(0, 0))
        self.assertFalse(snap.get(0, 1))
        self.assertTrue(snap.get(2, 0))
        self.assertFalse(snap.get(0, 2))
        self.assertRaises(Exception, snap.get, 0, 9)

        snap = tile.snap(TileState(flipped=True, rotation=0))
        self.assertFalse(snap.get(2, 0))
        self.assertTrue(snap.get(0, 2))

        snap = tile.snap(TileState(flipped=False, rotation=90))
        self.assertFalse(snap.get(0, 0))
        self.assertTrue(snap.get(0, 1))

    def test_snap_monster(self):
        snap = MONSTER.snap(TileState(flipped=False, rotation=0))
        self.assertEquals(snap.width, 3)
        self.assertEquals(snap.height, 20)
        self.assertTrue(snap.get(0, 18))
        self.assertTrue(snap.get(1, 0))
        self.assertTrue(snap.get(1, 5))
        self.assertTrue(snap.get(1, 6))
        self.assertTrue(snap.get(1, 11))
        self.assertTrue(snap.get(1, 12))
        self.assertTrue(snap.get(1, 17))
        self.assertTrue(snap.get(1, 18))
        self.assertTrue(snap.get(1, 19))
        self.assertTrue(snap.get(2, 1))
        self.assertTrue(snap.get(2, 4))
        self.assertTrue(snap.get(2, 7))
        self.assertTrue(snap.get(2, 10))
        self.assertTrue(snap.get(2, 13))
        self.assertTrue(snap.get(2, 16))
        self.assertEquals(snap.count(), 15)

    def test_snap_monster_rotation(self):
        snap = MONSTER.snap(TileState(flipped=False, rotation=90))
        self.assertEquals(snap.width, 20)
        self.assertEquals(snap.height, 3)

    def test_snap_monster_with_state(self):
        snap = MONSTER.snap(TileState(flipped=True, rotation=180))
        self.assertEquals(snap.count(), 15)

    def test_get_picture(self):
        tiles = parse_tiles(EXAMPLE.splitlines())
        assembly = assemble(tiles)
        picture = assembly.get_picture()
        # picture.pretty_print()

    def test_find_monster(self):
        tiles = parse_tiles(EXAMPLE.splitlines())
        self.assertEquals(find_monster(tiles), 273)


EXAMPLE = '''
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
'''

if __name__ == "__main__":
    unittest.main()
