from pycards.blackjack import Player, Dealer, Table
from pycards.blackjack.players import SimplePlayer, InteractivePlayer
from pycards import Deck

import logging
logging.basicConfig(level='DEBUG')

players = [InteractivePlayer()]
dealer = Dealer()
deck = Deck()
table = Table(players, dealer, deck)

for x in xrange(1, 1000):
    print x
    table.turn()
