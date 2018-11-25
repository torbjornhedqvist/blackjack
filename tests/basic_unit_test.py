#!/usr/bin/env python
"""
Basic test for the black jack game.

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


class UnitTests(unittest.TestCase):

    def test_can_import_playingcard(self):
        # Raises import error if the package cannot be imported
        from playingcard import PlayingCard

    def test_can_import_carddeck(self):
        # Raises import error if the package cannot be imported
        from carddecks import CardDecks
        
    def test_invalid_card_rank_type(self):
        # Raises SystemExit if rank type is not integer (using float)
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1.0, 0)
            
    def test_invalid_card_rank_range_low(self):
        # Raises SystemExit if rank type is below 1
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(0, 0)
            
    def test_invalid_card_rank_range_high(self):
        # Raises SystemExit if rank type is above 13
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(14, 0)
           
    def test_invalid_card_suit_type(self):
        # Raises SystemExit if rank type is not integer (using string)
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1, "Diamonds")
 
    def test_invalid_card_suit_range_low(self):
        # Raises SystemExit if rank type is below 0
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1, -1)

    def test_invalid_card_suit_range_high(self):
        # Raises SystemExit if rank type is above 3
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1, 4)

    def test_card_get_rank(self):
        # Assert if instance created rank is not returned by get_rank() 
        from playingcard import PlayingCard
        card = PlayingCard(1, 0)
        self.assertTrue(card.get_rank() == 1)

    def test_card_get_suit(self):
        # Assert if instance created suit is not returned by get_suit() 
        from playingcard import PlayingCard
        card = PlayingCard(1, 0)
        self.assertTrue(card.get_suit() == 0)        
            
    def test_size_of_new_carddeck(self):
        # Asserts if the default size of newly created card deck is not 52 cards
        from carddecks import CardDecks
        deck = CardDecks()
        self.assertTrue(deck.length() == 52)

    def test_size_of_new_double_carddeck(self):
        # Asserts if the default size of newly created card deck with 2 decks doesnt contain 104 cards
        from carddecks import CardDecks
        decks = CardDecks(2)
        self.assertTrue(decks.length() == 104)
        
    def test_new_carddeck_pop(self):
        # Asserts if pop doesn't remove card from deck
        from carddecks import CardDecks
        deck = CardDecks()  # length 52
        deck.pop()
        self.assertTrue(deck.length() == 51)


if __name__ == "__main__":
    unittest.main()
