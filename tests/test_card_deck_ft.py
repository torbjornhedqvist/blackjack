#!/usr/bin/env python
"""
Simple test of the card deck and playing card classes

Copyright (C) Torbjorn Hedqvist - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license. See LICENSE file in the project
root for full license information.

"""
import sys
import os

MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from carddecks import CardDecks

CARD_RANK = ["Invalid", "Ace", "Two", "Three", "Four", "Five", "Six",
             "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
CARD_SUIT = ["Spades", "Clubs", "Diamonds", "Hearts"]

DECK = CardDecks(2)
COUNT = 0
while DECK.length():
    COUNT += 1
    CARD = DECK.pop()
    print(str(COUNT) + ": " + CARD_RANK[CARD.get_rank()] + " of " + CARD_SUIT[CARD.get_suit()])
