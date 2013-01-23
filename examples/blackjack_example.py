from pybj import Player, Dealer, Table, Deck
from pybj.players import SimplePlayer, InteractivePlayer

import logging
logging.basicConfig(level='INFO')

players = [SimplePlayer()]
dealer = Dealer()
#deck = Deck(symbols = ['A', '10', '8'])
deck = Deck()
table = Table(players, dealer, deck)

for x in xrange(1, 10):
    print x
    table.turn()
