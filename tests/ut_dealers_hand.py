#!/usr/bin/env python
"""
Copyright (C) Torbjorn Hedqvist - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license. See LICENSE file in the project
root for full license information.

"""
import unittest
import sys
import os
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from common import get_value_of_dealers_hand


class DealersHand(unittest.TestCase):

    def test_dealers_hand1(self):
        """
        Start with an ace which should stay on a hard (1) ace since the second
        card (5) doesn't give a value between 17 and 21 even if the ace are treated
        as a soft (11) ace.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        card = PlayingCard(5, 0)
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 6)

    def test_dealers_hand2(self):
        """
        Start with an ace which should be turned into a soft (11) ace as soon as the
        second card which is a face (10) card and should return 21.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        card = PlayingCard(11, 0)  # Knight which could collide with soft ace
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 21)

    def test_dealers_hand3(self):
        """
        Start with a Knight which could collide with soft ace and a second card which is
        second card which is an ace and should return 21.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(11, 0)  # Knight which could collide with soft ace
        cards.append(card)
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 21)

    def test_dealers_hand4(self):
        """
        Start with an ace followed by a 4, (gives 5) and yet another ace which will not
        be more than a total of 16 if treated as soft so stay on hard interpretation
        which give a result of 6

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        card = PlayingCard(4, 0)
        cards.append(card)
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 6)

    def test_dealers_hand5(self):
        """
        Start with an ace followed by a 5, (gives 6) and yet another ace which will
        be more than a total of 16 if treated as soft which give a result of 17

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        card = PlayingCard(5, 0)
        cards.append(card)
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 17)

    def test_dealers_hand6(self):
        """
        Start with an ace followed by a 2, (gives 3) and yet another ace which will
        still be less than 17. Then follow up with a 4 which will be 18 if the
        previous ace turns into soft.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Ace
        cards.append(card)
        card = PlayingCard(2, 0)  # 1 + 2 = 3
        cards.append(card)
        card = PlayingCard(1, 0)  # Ace + 3 = 4
        cards.append(card)
        card = PlayingCard(4, 0)  # Change previous Ace to 11 gives (1 + 2 + 11 + 4 = 18)
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 18)

    def test_dealers_hand7(self):
        """
        Start with an ace followed by 2 and face (10) which would be a bust (23) if
        the first ace was treated as soft. Should keep hard ace and result in 20.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        card = PlayingCard(2, 0)
        cards.append(card)
        card = PlayingCard(13, 0)
        cards.append(card)
        card = PlayingCard(7, 0)
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 20)


if __name__ == "__main__":
    unittest.main()
