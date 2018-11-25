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
from common import get_value_of_players_hand


class PlayersHand(unittest.TestCase):

    def test_players_hand1(self):
        """
        Check that "face cards are turned into 10

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(12, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 10)

    def test_players_hand2(self):
        """
        Check that ace is treated as soft (11)

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 11)

    def test_players_hand3(self):
        """
        Check that initial soft ace (11) is turned into hard ace (1)
        when hand becomes busted.

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 11)
        card = PlayingCard(5, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 16)
        card = PlayingCard(8, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 14)

    def test_players_hand4(self):
        """
        Another check that initial soft ace (11) is turned into hard ace (1)
        when hand becomes busted.

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 11)
        card = PlayingCard(3, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 14)
        card = PlayingCard(13, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 14)


if __name__ == "__main__":
    unittest.main()
