from pybj import Player


class SimplePlayer(Player):
    """ Simple strategy from http://wizardofodds.com/games/blackjack """
    def play(self, hand_idx=0):
        hand = self.hands[hand_idx]
        dealer_symbol = self.table.dealer.visible_card.symbol
        high = dealer_symbol in '7 8 9 10 J Q K A'.split()

        can_double = self.table.can_double(hand)
        can_split = self.table.can_split(hand)

        # Pair
        if hand.pair:
            if hand[0].symbol in '8A':
                if can_split:
                    return self._split(hand_idx)
            elif hand[0].symbol in ['4', '5', '10']:
                # treat it as if not a pair
                pass
            else:
                if not high:
                    if can_split:
                        return self._split(hand_idx)
                # else: doing as if not a pair

        # Here we don't have a pair
        # Soft hand?
        if hand.soft:
            if hand.sum >= 19:
                return 'stand'
            elif hand.sum <= 13:
                return 'hit'
            else:
                if not high and can_double:
                    return self._double(hand_idx)
                else:
                    return 'hit'

        # Hard hand
        else:
            if hand.sum <= 8:
                return 'hit'
            elif hand.sum >= 17:
                return 'stand'
            elif hand.sum >= 12:
                if not high and can_double:
                    return self._double(hand_idx)
                else:
                    return 'hit'
            elif hand.sum >= 10:
                if dealer_symbol not in '10 J Q K A'.split() and can_double:
                    return self._double(hand_idx)
                else:
                    return 'hit'

            # We have a 9
            else:
                if not high and can_double:
                    return self._double(hand_idx)
                else:
                    return 'hit'
