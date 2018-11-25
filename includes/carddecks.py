#!/usr/bin/env python
"""
Create a playing card deck (normal 52 card deck) or virtual "Shoe" of
decks if more than one is defined.
When one ore more decks are created they will be shuffled.

Copyright (C) Torbjorn Hedqvist - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license. See LICENSE file in the project
root for full license information.

"""
from random import shuffle
from playingcard import PlayingCard


class CardDecks(object):
    """
    When instantiated holds a list of
    :meth:`lib.playingcard.PlayingCard` objects in random order.

    """

    def __init__(self, num_of_decks=1):
        """
        Create one or more playing card decks and shuffle them all
        together in a list.

        """
        self.__card_decks = []
        for num in range(0, num_of_decks):
            for suit in range(0, 4):
                for rank in range(1, 14):
                    instance = PlayingCard(rank, suit)
                    self.__card_decks.append(instance)
        self.shuffle()

    def shuffle(self):
        """
        Shuffle all the cards in this instance list.

        :return: None

        """
        shuffle(self.__card_decks)

    def pop(self):
        """
        Pop (pull and remove) the last card in the list.

        :return: A :meth:`lib.playingcard.PlayingCard` object.

        """
        return self.__card_decks.pop()

    def length(self):
        """
        :return: The length (the number of remaining cards) in the list.

        """
        return len(self.__card_decks)


class TestingCardDeck(object):
    """
    Used to create a pre-defined deck for testing purposes

    """

    def __init__(self):
        """
        Instantiate an instance of a deck containing
        :meth:`lib.playingcard.PlayingCard` objects
        which have pre-defined values to test specific
        scenarios in the Black Jack game

        """
        self.__card_decks = []

        for x in range(1, 52):  # Fill up a deck of dummies
            instance = PlayingCard(7, 1)
            self.__card_decks.append(instance)

        # Stay on 19 (ace + 8) and dealer gets two aces 1+1+4+(common value in deck above)
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(1, 0))
        self.__card_decks.append(PlayingCard(8, 3))
        self.__card_decks.append(PlayingCard(1, 3))
        self.__card_decks.append(PlayingCard(1, 2))

        # Two tens to player to be used for split, followed by two aces to see how a
        # double black jack is handled.
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(8, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(10, 0))

        # First hand for player is a BlackJack
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(10, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(1, 0))

        # Start with a low hand for player to test double down
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(2, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(2, 0))

        # Create a split, first hand ok and second busted
        self.__card_decks.append(PlayingCard(12, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(2, 0))
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(8, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(8, 0))

    def pop(self):
        """
        Pop (pull and remove) the last card in the list.

        :return: A :meth:`lib.playingcard.PlayingCard` object.

        """
        return self.__card_decks.pop()

    def length(self):
        """
        :return: The length (the number of remaining cards) in the list.

        """
        return len(self.__card_decks)
