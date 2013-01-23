from pybj import Player, Dealer, Table, Deck
from pybj.players import SimplePlayer, InteractivePlayer

import logging
logging.basicConfig(level='DEBUG')

players = [InteractivePlayer()]
dealer = Dealer()
deck = Deck()
table = Table(players, dealer, deck)

for x in xrange(1, 1000):
    print x
    table.turn()
