from pybj import Player, Dealer, Table, Deck
from pybj.players import SimplePlayer, InteractivePlayer

import logging
logging.basicConfig(level='INFO')

players = [InteractivePlayer()]
dealer = Dealer()
deck = Deck()
table = Table(players, dealer, deck)

for x in xrange(1, 1000):
    print 'Turn {}'.format(x)
    table.turn()
