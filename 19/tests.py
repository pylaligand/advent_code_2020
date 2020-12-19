#!/usr/bin/python

import unittest

from main import Ruleset


class Test19(unittest.TestCase):
    def assertPatternEquals(self, rules, index, pattern):
        self.assertEquals(rules.get_pattern(index)[0], pattern)

    def test_ruleset_get_pattern(self):
        rules = Ruleset([
            '0: "a"',
        ])
        self.assertPatternEquals(rules, 0, "a")

        rules = Ruleset([
            '0: "a"',
            '1: 0 0',
        ])
        self.assertPatternEquals(rules, 1, "aa")

        rules = Ruleset([
            '0: "a"',
            '1: 0 2 | 2 0 0',
            '2: "b"',
        ])
        self.assertPatternEquals(rules, 1, "(?:ab|baa)")

    def test_ruleset_get_pattern_bad_index(self):
        rules = Ruleset([
            '0: "a"',
        ])
        self.assertRaises(Exception, rules.get_pattern, 12)

    def test_examples_simple(self):
        rules = Ruleset([
            '0: 4 1 5',
            '1: 2 3 | 3 2',
            '2: 4 4 | 5 5',
            '3: 4 5 | 5 4',
            '4: "a"',
            '5: "b"',
        ])
        self.assertTrue(rules.match(0, 'ababbb'))
        self.assertFalse(rules.match(0, 'bababa'))
        self.assertTrue(rules.match(0, 'abbbab'))
        self.assertFalse(rules.match(0, 'aaabbb'))
        self.assertFalse(rules.match(0, 'aaaabbb'))

    def assertMatchCount(self, rules, index, messages, count):
        self.assertEquals(sum(1 for m in messages if rules.match(index, m)),
                          count)

    def test_examples_hard(self):
        rules = Ruleset([
            '42: 9 14 | 10 1',
            '9: 14 27 | 1 26',
            '10: 23 14 | 28 1',
            '1: "a"',
            '11: 42 31',
            '5: 1 14 | 15 1',
            '19: 14 1 | 14 14',
            '12: 24 14 | 19 1',
            '16: 15 1 | 14 14',
            '31: 14 17 | 1 13',
            '6: 14 14 | 1 14',
            '2: 1 24 | 14 4',
            '0: 8 11',
            '13: 14 3 | 1 12',
            '15: 1 | 14',
            '17: 14 2 | 1 7',
            '23: 25 1 | 22 14',
            '28: 16 1',
            '4: 1 1',
            '20: 14 14 | 1 15',
            '3: 5 14 | 16 1',
            '27: 1 6 | 14 18',
            '14: "b"',
            '21: 14 1 | 1 14',
            '25: 1 1 | 1 14',
            '22: 14 14',
            '8: 42',
            '26: 14 22 | 1 20',
            '18: 15 15',
            '7: 14 5 | 1 21',
            '24: 14 1',
        ])
        messages = [
            'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
            'bbabbbbaabaabba',
            'babbbbaabbbbbabbbbbbaabaaabaaa',
            'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
            'bbbbbbbaaaabbbbaaabbabaaa',
            'bbbababbbbaaaaaaaabbababaaababaabab',
            'ababaaaaaabaaab',
            'ababaaaaabbbaba',
            'baabbaaaabbaaaababbaababb',
            'abbbbabbbbaaaababbbbbbaaaababb',
            'aaaaabbaabaaaaababaa',
            'aaaabbaaaabbaaa',
            'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
            'babaaabbbaaabaababbaabababaaab',
            'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
        ]
        self.assertMatchCount(rules, 0, messages, 3)

        rules.replace('8: 42 | 42 8')
        rules.replace('11: 42 31 | 42 11 31')
        rules.set_max_len(max(len(m) for m in messages))
        self.assertMatchCount(rules, 0, messages, 12)


if __name__ == "__main__":
    unittest.main()
