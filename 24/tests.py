#!/usr/bin/python

import unittest

from main import count_black_tiles, make_beauty_happen, parse_sequences, Direction, Sequence


class Test24(unittest.TestCase):
    def test_parse_sequences(self):
        sequences = parse_sequences(['seenww'])
        self.assertEquals(sequences, [
            Sequence([
                Direction.SOUTHEAST, Direction.EAST, Direction.NORTHWEST,
                Direction.WEST
            ])
        ])

    def test_count_black_tiles(self):
        sequences = parse_sequences(l for l in EXAMPLE.splitlines() if l)
        self.assertEquals(count_black_tiles(sequences), 10)

    def test_make_beauty_happen(self):
        sequences = parse_sequences(l for l in EXAMPLE.splitlines() if l)
        self.assertEquals(make_beauty_happen(sequences, 1), 15)
        self.assertEquals(make_beauty_happen(sequences, 2), 12)
        self.assertEquals(make_beauty_happen(sequences, 10), 37)
        self.assertEquals(make_beauty_happen(sequences, 50), 566)
        self.assertEquals(make_beauty_happen(sequences, 100), 2208)


EXAMPLE = '''
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''

if __name__ == "__main__":
    unittest.main()
