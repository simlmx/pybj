from ..cards import Card
import logging
logger = logging.getLogger(__name__)

class Hand(object):
    """A blackjack hand of `Card`."""

    def __init__(self, *cards, **kwargs):
        """
            kwargs:
                is_split
                    If the hand is from a split. Defaults to False.
        """
        self.cards = list(cards)
        self.is_split = False
        if 'is_split' in kwargs and kwargs['is_split']:
            self.is_split = True

    def hit(self, card):
        self.cards.append(card)

    def split(self):
        if not self.pair:
            raise ValueError('You cannot split a {}'.format(self.name))
        return Hand(self.cards[0], is_split=True), Hand(self.cards[1], is_split=True)

    def _soft_sum(self):
        """ Utility function that returns a tuple containing the soft sum
            and a boolean indicating the presence of aces.
        """
        sum_ = 0
        has_aces = False
        for c in self.cards:
            if c.symbol in 'JQK':
                sum_ += 10
            elif c.symbol == 'A':
                has_aces = True
                sum_ += 1
            else:
                sum_ += int(c.symbol)

        return sum_, has_aces

    @property
    def sum(self):
        sum_, has_aces = self._soft_sum()
        # If the total is less than 21, one ace counts as a 11
        # note that it will count as a soft hand
        if has_aces and sum_ + 10 <= 21:
            sum_ += 10
        return sum_

    @property
    def soft(self):
        """ Here "soft" means a hand for which `self.sum - 10` is also a valid
            value for the hand.
        """
        soft_sum, has_aces = self._soft_sum()
        if has_aces and soft_sum + 10 <= 21:
            return True
        return False

    @property
    def blackjack(self):
        if len(self.cards) == 2:
            ten = ['J', 'Q', 'K', '10']
            if self.cards[0].symbol in ten and self.cards[1].symbol == 'A':
                return True
            if self.cards[0].symbol == 'A' and self.cards[1].symbol in ten:
                return True
        return False

    @property
    def bust(self):
        """Check if the hand busts (> 21)"""
        return self.sum > 21 and not self.soft

    @property
    def pair(self):
        symbols = sorted(['10' if c.symbol in 'JKQ' else c.symbol for c in self.cards])
        return len(self.cards) == 2 and symbols[0] == symbols[1]

    @property
    def name(self):
        """Pretty name"""
        symbols = sorted(['10' if c.symbol in 'JKQ' else c.symbol for c in self.cards])
        if len(symbols) == 2:
            # pairs
            if symbols[0] == symbols[1]:
                return 'pair of ' + symbols[0]
            # blackjack
            if symbols[0] == '10' and symbols[1] == 'A':
                return 'blackjack'

        # special case
        if len(symbols) == 1 and symbols[0] == 'A':
            return 'A'

        s = str(self.sum)
        if self.soft:
            s = 'soft ' + s
        return s

    # Note that ==, <= and >= are *not* overwrited
    def __gt__(self, other):
        if self.blackjack and not other.blackjack:
            return True
        if not self.bust and other.bust:
            return True
        if self.sum > other.sum:
            return True
        return False

    def __lt__(self, other):
        if self.bust and not other.bust:
            return True
        if other.blackjack and not self.blackjack:
            return True
        if self.sum != other.sum and not self > other:
            return True
        return False

    def __getitem__(self, i):
        return self.cards[i]

    def __str__(self):
        return self.name
    __repr__ = __str__


class Player(object):
    def __init__(self, stash=100., default_bet=5., table = None):
        self.stash = stash
        self._hands = []
        self.default_bet = default_bet
        self._bet = []
        self.table = table

    def _set_hands(self, hands_or_cards):
        """ If you pass Cards, will make one hand out of those. """
        # If we were given a hand
        if isinstance(hands_or_cards, Hand):
            self._hands = [hands_or_cards]
        # A single card
        elif isinstance(hands_or_cards, Card):
            self._hands = [Hand(hands_or_cards)]
        # list of Hands
        elif isinstance(hands_or_cards[0], Hand):
            self._hands = hands_or_cards
        # list of Cards
        else:
            self._hands = [Hand(*hands_or_cards)]

    def _get_hands(self):
        return self._hands

    hands = property(_get_hands, _set_hands, doc="Get/sets the player's hands")

    def _set_hand(self, hands_or_cards):
        self._set_hands(hands_or_cards)

    def _get_hand(self):
        if len(self.hands) >= 2:
            raise ValueError('This player has more than one hand, use self.hands not self.hand.')
        return self.hands[0]

    hand = property(_get_hand, _set_hand, doc="Get/sets the player's hand *when he has only one*.")

    def ask(self, hand_idx=0):
        """ Ask what to do for the players' "hand_idx" hand.
            This is what you want to override for custom strategies

            Don't forget that if you double, you need to call `double` yourself.
            Same for split.
        """
        hand = self.hands[hand_idx]
        if hand.sum < 17 or hand.soft:
            return 'hit'
        else:
            return 'stand'

    def bet(self, amount=None):
        """ Bet something to receive cards. Your might want to override this
            if you want some betting strategy.
        """
        if len(self.hands) > 0:
            raise ValueError('You can not bet if you already have cards.')
        if amount is None:
            amount = self.default_bet
        if self.stash - amount < 0:
            raise ValueError('You can not bet less than you have')
        self.stash -= amount
        self._bet = [amount]
        return amount

    def _double(self, hand_idx=0):
        self._bet[hand_idx] *= 2.
        return 'double'

    def _split(self, hand_idx=0):
        """Inserts the new hand at position hand_idx+1 in our hands."""
        hand = self.hands.pop(hand_idx)
        new_hands = hand.split()
        self.hands.insert(hand_idx, new_hands[0])
        self.hands.insert(hand_idx, new_hands[1])
        self._bet.insert(hand_idx, self._bet[hand_idx])
        return 'split'

    def _surrender(self, hand_idx=0):
        self.stash += self._bet[hand_idx] / 2.
        del self._bet[hand_idx]
        del self.hands[hand_idx]
        return 'surrender'

    def win(self, hand_idx=0, how_many_times_your_bet=1.):
        """Gives the player back his bet + some gain."""
        self.stash += self._bet[hand_idx]
        self.stash += how_many_times_your_bet * self._bet[hand_idx]
        del self._bet[hand_idx]
        del self.hands[hand_idx]

    def loose(self, hand_idx=0):
        self.stash -= self._bet[hand_idx]
        del self._bet[hand_idx]
        del self.hands[hand_idx]

    def tie(self, hand_idx=0):
        self.stash += self._bet[hand_idx]
        del self._bet[hand_idx]
        del self.hands[hand_idx]

    def count(self, cards):
        """ Will count what's going out of the deck.
            Register this method on the deck.
        """
        pass


class Dealer(Player):

    def ask(self, hand_idx=0):
        if self.hand.sum < 17:
            return 'hit'
        if self.hand.sum == 17 and self.hand.soft and \
                not self.table.rules['dealer_stands_on_soft_17']:
            return 'hit'
        return 'stand'

    @property
    def visible_card(self):
        return self.hand[0]

default_rules = {
    'dealer_stands_on_soft_17': False,
    'surrender': False,
    'double_after_split': False,
    # TODO make those effective
    'hitting_split_aces': False,
    'gain_for_blackjack': 1.5,
}


class Table(object):
    def __init__(self, players, dealer, deck, **rules):

        self.players = players
        for p in self.players:
            p.table = self
        self.dealer = dealer
        self.dealer.table = self
        self.deck = deck
        self.rules = dict(default_rules)
        self.rules.update(rules)

    def turn(self):
        logger.debug('starting turn')
        # Deal first cards
        self.dealer.hand = self.deck.deal(2)
        logger.debug('The dealer as a {} (visible) and a {} (hidden)'.format(
            self.dealer.hand[0], self.dealer.hand[1]))
        for i, p in enumerate(self.players):
            b = p.bet()
            logger.debug('Player {} bet {:.2f}$'.format(i, b))
            p.hand = self.deck.deal(2)
            logger.debug('Player {} received a {}'.format(i, p.hand.name))

        # Players (and than dealer) play
        players_and_dealer = self.players + [self.dealer]
        for k in xrange(len(players_and_dealer)):
            p = players_and_dealer[k]
            if k == len(self.players):
                k = 'dealer'
            logger.debug('Player {}\'s turn'.format(k))
            i = 0
            while i < len(p.hands):
                h = p.hands[i]
                action = 'hit'
                if len(p.hands) > 1:
                    logger.debug('Hand {}'.format(i))
                while action == 'hit':
                    action = p.ask(i)
                    if action == 'hit':
                        h.hit(self.deck.deal_one())
                        logger.debug('Hit: hand is now {}'.format(h))
                    elif action == 'split':
                        p.hands[i].hit(self.deck.deal_one())
                        p.hands[i + 1].hit(self.deck.deal_one())
                        logger.debug('Splits')
                    elif action == 'surrender':
                        if not self.rules['surrender_allowed']:
                            raise ValueError('Surrender not allowed')
                        logger.debug('Surrenders')
                        i += 1
                    elif action == 'double':
                        if len(h.cards) != 2 or h.is_split:
                            raise ValueError('You can only double on your initial hand.')
                        h.hit(self.deck.deal_one())
                        logger.debug('Doubles: hand is now {}'.format(h))
                        i += 1
                    elif action == 'stand':
                        logger.debug('Stands')
                        i += 1
                    else:
                        raise NotImplementedError(
                            'action "{}" is not valid/implemented'.format(action))

        # Resolve bets
        for k,p in enumerate(self.players):
            logger.debug('Player {}\'s resolution'.format(k))
            # Remember that Every resolution removes the hand
            while len(p.hands) > 0:
                h = p.hands[0]
                if len(p.hands) > 1:
                    logger.debug('Hand {}'.format(0))
                if h.bust:
                    p.loose(0)
                    logger.debug('Busts with {}.'.format(h))
                elif h < self.dealer.hand:
                    p.loose(0)
                    logger.debug('Looses {}'.format(h))
                elif h.blackjack and not self.dealer.hand.blackjack:
                    p.win(0, self.rules['gain_for_blackjack'])
                    logger.debug('Wins with {}'.format(h))
                elif h > self.dealer.hand:
                    p.win(0)
                    logger.debug('Wins with {}'.format(h))
                else:
                    p.tie(0)
                    logger.debug('Ties with {}'.format(h))
                logger.debug('Stash is now ${:.2f}'.format(p.stash))


