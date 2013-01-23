from pybj import Player


class InteractivePlayer(Player):
    """You are the player!"""
    def play(self, hand_idx=0):
        hand = self.hands[hand_idx]
        cards = hand.cards
        cards_str = ', '.join(map(str, cards))

        print 'You have a {} ({})'.format(hand, cards_str)
        print 'The dealer has a {}'.format(self.table.dealer.visible_card)
        choice = ''

        text = 'You can either\n' \
            '  hit        (h)\n' \
            '  stand      (s)\n' \

        if self.table.can_double(hand):
            text += '  double     (d)\n'
        if self.table.can_split(hand):
            text += '  split     (sp)\n'
        if self.table.can_surrender(hand):
            text += '  surrender (su)\n'

        while choice not in 'sp h s su d'.split():
            choice = raw_input(text)
        if choice == 'h':
            return 'hit'
        elif choice == 's':
            return 'stand'
        elif choice == 'd':
            return self._double(hand_idx)
        elif choice == 'sp':
            return self._split(hand_idx)
        elif choice == 'su':
            return self._surrender(hand_idx)
        else:
            raise ValueError('oups')


