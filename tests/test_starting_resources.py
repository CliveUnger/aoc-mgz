import unittest
from mgz.model import parse_match


class TestStartingResources(unittest.TestCase):

    def test_starting_resources_from_header(self):
        with open('tests/recs/de-68.0.aoe2record', 'rb') as handle:
            match = parse_match(handle)
        olive = next(p for p in match.players if p.name == 'Olive')
        # Huns start with 100 less wood — confirms per-player header values
        self.assertEqual(
            olive.starting_resources,
            {'food': 200, 'wood': 100, 'stone': 200, 'gold': 100},
        )
