import unittest
from pybj import Hand, Player, Card


class TestBlackJack(unittest.TestCase):

    def test_hand_methods(self):

        ha3 = Hand(Card(3), Card('A'))
        hbj = Hand(Card('J'), Card('A'))
        h21 = Hand(Card(5), Card(10), Card(6))
        hbust = Hand(Card(10), Card(10), Card(2))
        hpair = Hand(Card('J'), Card(10))

        self.assertTrue(hbj > h21 > ha3 > hbust)
        self.assertTrue(hbust < ha3 < h21 < hbj)
        self.assertFalse(hbj < hbj)
        self.assertFalse(hbj > hbj)

        self.assertTrue(hbust.bust)
        self.assertFalse(h21.bust)
        self.assertTrue(ha3.soft)
        self.assertFalse(hbj.soft)
        self.assertTrue(hbj.blackjack)
        self.assertTrue(hpair.pair)
        self.assertFalse(hbust.pair)
        self.assertFalse(ha3.pair)

        self.assertEqual(ha3.sum, 14)
        self.assertTrue(hbj.sum, 21)

        self.assertEqual(ha3.name, 'soft 14')
        self.assertEqual(hbj.name, 'blackjack')
        self.assertEqual(h21.name, '21')
        self.assertEqual(hpair.name, 'pair of 10')

        h_special_soft = Hand(Card(10), Card(10), Card('A'))
        self.assertFalse(h_special_soft.soft)

        self.assertTrue(Hand(Card(10), is_split=True).is_split)

    def test_player_win_loose(self):
        player = Player()
        hand = Hand(Card(10), Card(3))
        stash = player.stash
        bet = player.bet()
        player.hand = hand
        player.win()
        self.assertEqual(player.stash, stash + bet)
        bet = player.bet()
        player.hands = hand
        player.loose()
        self.assertEqual(player.stash, stash)
        bet = player.bet(10)
        player.hand = hand
        player.win(how_many_times_your_bet=2)
        self.assertEqual(player.stash, stash + 20)

        # with two hands
        hand = Hand(Card(10), Card('J'))
        player.stash = 10.
        player.bet()
        player.hand = hand
        player._split()
        self.assertEqual(player.stash, 0.)
        player.hands[0].hit(Card(5))
        player.hands[1].hit(Card(4))
        player.win()  # hand 0
        player.loose()  # hand 1 becomes hand 0 because it is deleted when finished
        self.assertEqual(player.stash, 10.)







