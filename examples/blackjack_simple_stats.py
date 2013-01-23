import sys
from itertools import combinations_with_replacement, product
from pybj import Deck, Card, Hand, Player, Dealer

nb_runs = int(sys.argv[1])

deck = Deck(8)

symbols = set(deck.symbols)
_dealer_poss = sorted(set(Hand(Card(s)).name for s in deck.symbols))
_player_poss = sorted(set([Hand(Card(a), Card(b)).name for a,b in combinations_with_replacement(symbols, 2)]))
_poss = list(product(_dealer_poss, _player_poss))
stats = {x: {'count':0, 'gains':0} for x in _poss}

players = [Player()]
dealer = Dealer()


for _ in xrange(nb_runs):

    # Give some cards
    for p in players + [dealer]:
        p.hand = Hand(deck.deal(2))

    for p in players:

        stats_key = (Hand(dealer.hand[0]).name, p.hand.name)
        stats[stats_key]['count'] += 1

        action = p.ask()
        if action == 'hit':
            p.hand.hit(deck.deal_one())



    if player_hand.bust:
        stats[stats_key]['gains'] -= 1
        continue

    while dealer_hand.sum < 17:
        dealer_hand.hit(deck.deal())

    if dealer_hand.bust:
        stats[stats_key]['gains'] += 1
        continue

    # Here nobody busted
    if dealer_hand > player_hand:
        stats[stats_key]['gains'] -= 1
        continue
    if dealer_hand < player_hand:
        stats[stats_key]['gains'] += 1
        continue
    assert dealer_hand.sum == player_hand.sum
    # Here both hands are equal

keys = sorted(stats.keys())
for k in keys:
    count = stats[k]['count']
    gains = stats[k]['gains']
    print k, ':', (1. * gains / count if count != 0 else 0), 'happened {} times'.format(count)


# FIXME ca sent le bug pcq on gagne .48$ en moyenne en ayant un blackjack
# ca devrait pas etre .69$ ??
