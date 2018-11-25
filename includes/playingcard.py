#!/usr/bin/env python
"""
Class Playing Card

This class creates an instance of a playing card with the valid
value of rank in range 1 to 13 and suit in range of 0 to 3

Copyright (C) Torbjorn Hedqvist - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license. See LICENSE file in the project
root for full license information.

"""
import sys
import traceback


class PlayingCard(object):
    """
    TODO: Write comment
    """
    def __init__(self, rank, suit):
        try:
            if not isinstance(rank, int):
                raise ValueError("Error: rank has to be integer: "
                                 + str(rank))
            elif rank < 1 or rank > 13:
                raise ValueError("Error: rank out of range (1-13): "
                                 + str(rank))
            else:
                self.__rank = rank
        except ValueError:
            traceback.print_exc()
            sys.exit()

        try:
            if not isinstance(suit, int):
                raise ValueError("Error: suit has to be integer: "
                                 + str(suit))
            elif suit < 0 or suit > 3:
                raise ValueError("Error: suit out of range (0-3): "
                                 + str(suit))
            else:
                self.__suit = suit
        except ValueError:
            traceback.print_exc()
            sys.exit()

    def get_rank(self):
        """
        :return: The rank of this instance.

        """
        return self.__rank

    def get_suit(self):
        """
        :return: The suit of this instance.

        """
        return self.__suit

# Experimental
# class PlayingCardError(BaseException):
#    """ Error handling class """
#    def __init__(self, rank):
#        super(PlayingCardError, self).__init__(rank)
#        self.rank = rank
#
#    def __str__(self):
#        return repr(self.rank)
