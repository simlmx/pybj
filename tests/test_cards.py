import unittest
from ..cards import Deck


class TestCards(unittest.TestCase):
    def setUp(self):
        self.deck = Deck(2)

    def test_all(self):
        cards = self.deck.deal(4)
        cards += self.deck.deal()
        cards.append(self.deck.deal_one())


if __name__ == '__main__':
    unittest.main()
