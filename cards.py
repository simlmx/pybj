import random
from itertools import product

import logging
logger = logging.getLogger(__name__)

class Card(object):
    _color_names = {
        'S': 'spades',
        'C': 'clubs',
        'H': 'hearts',
        'D': 'diamonds',
    }
    _symbol_names = {
        'A': 'ace',
        'J': 'jack',
        'Q': 'queen',
        'K': 'king',
    }

    def __init__(self, symbol, color='H'):
        """ `symbol`: a string like 'A', '2', '3', ..., '10', 'J', 'Q', 'K'
            `color`: 'S', 'C', 'H', 'D'
        """
        self.symbol = str(symbol)
        self.color = color

    def __str__(self):
        name = ''
        if self.symbol in self._symbol_names:
            name += self._symbol_names[self.symbol]
        else:
            name += self.symbol
        name += ' of '
        name += self._color_names[self.color]
        return name
    __repr__ = __str__




class Deck(object):
    # TODO jokers?

    _on_deal = []

    def __init__(self, nb_decks=1, symbols = None, colors = None, shuffle_on='end'):
        if symbols is None:
            symbols = map(str, range(2,11)) + 'J Q K A'.split()
        if colors is None:
            colors = ['S', 'C', 'H', 'D']
        self.symbols = symbols
        self.colors = colors
        self.nb_decks = nb_decks
        self.shuffle_on = shuffle_on

        cards = list(product(self.symbols, self.colors))
        cards *= nb_decks
        # The last card is the top of the deck
        self.undealt_cards = [Card(s,c) for s,c in cards]
        # The last card is the last that has been dealt
        self.dealt_cards = []
        random.shuffle(self.undealt_cards)

    def deal(self, nb_cards=1, visible=True):
        """ Return a list of 'nb_cards' cards
            visible: if "players" can see the card. This is for the
            callbacks
        """
        cards = []
        for i in xrange(nb_cards):
            # Move each card from the undealt_cards list to the dealt_cards
            # list

            # TODO shuffle at some point X that we can define, e.g. middle of
            # deck, where there are no cards left etc.
            card = self.undealt_cards.pop()
            self.dealt_cards.append(card)
            cards.append(card)
            if self.shuffle_on == 'end' and len(self.undealt_cards) == 0:
                self.shuffle()
                for callback in self._on_deal:
                    callback('shuffle')
        for callback in self._on_deal:
            callback(cards)
        logger.debug('Deck deals {}'.format(cards))
        return cards

    def deal_one(self):
        """Deals a single card."""
        return self.deal(1)[0]

    def shuffle(self):
        """Gather back all the cards and shuffle."""
        self.undealt_cards.extend(self.dealt_cards)
        self.dealt_cards = []
        random.shuffle(self.undealt_cards)

    def count_on_deal(self, callback):
        """ Will call `callback` with a list of the cards being dealt as arguments
            every time something visible is dealt. The callback will be
            passed the string "shuffle" when the deck is shuffled.
        """
        self._on_deal.append(callback)

