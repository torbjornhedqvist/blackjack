#!/usr/bin/env python
"""
All common support functions and classes used in the black jack game

Copyright (C) Torbjorn Hedqvist - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license. See LICENSE file in the project
root for full license information.

"""

# Standard imports
import sys
import os
import pygame
import inspect  # To be used to print function name in log statements

# Local imports
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from globals import *
from playingcard import PlayingCard

############################
# Common support functions #
############################


def plot_players_hands(screen,
                       player_pos_start,
                       player_hands,
                       double_downs,
                       hands_status):
    """
    Plot the players all card on the game table.

    :param screen:
    :param player_pos_start:
    :param player_hands:
    :param double_downs:
    :param hands_status:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    player_x_pos, player_y_pos = player_pos_start
    image_db = ImageDB.get_instance()
    for index_x, hand in enumerate(player_hands):
        for index_y, card in enumerate(hand):
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)

            if index_y == 2 and len(hand) == 3 and double_downs[index_x]:
                # rotate the third card if we have a double down in current hand
                screen.blit(pygame.transform.rotate(image_db.get_image(image), 90),
                            (player_x_pos, player_y_pos))
            else:
                screen.blit(image_db.get_image(image), (player_x_pos, player_y_pos))
            player_x_pos += GAP_BETWEEN_CARDS
            player_y_pos -= 14

        x_offset = -50
        y_offset = -40
        if index_x == 0:
            hand = 'first_hand_'
        else:
            hand = 'second_hand_'

        if hands_status[hand + 'blackjack']:
            screen.blit(image_db.get_image(IMAGE_PATH + "blackjack.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'win']:
            screen.blit(image_db.get_image(IMAGE_PATH + "you_win.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'push']:
            screen.blit(image_db.get_image(IMAGE_PATH + "push.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'loose']:
            screen.blit(image_db.get_image(IMAGE_PATH + "you_loose.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'busted']:
            screen.blit(image_db.get_image(IMAGE_PATH + "busted.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        player_x_pos, player_y_pos = player_pos_start
        player_x_pos += GAP_BETWEEN_SPLIT


def plot_dealers_hand(screen,
                      dealer_card_start_pos,
                      dealer_cards,
                      first_card_hidden):
    """
    Plot the dealers all card on the game table and if the first card
    should be hidden plot a card back for that card.

    :param screen:
    :param dealer_card_start_pos:
    :param dealer_cards:
    :param first_card_hidden:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    dealer_x_pos, dealer_y_pos = dealer_card_start_pos
    image_db = ImageDB.get_instance()
    for card in dealer_cards:
        if first_card_hidden is True:
            # Show first dealer card hidden
            screen.blit(image_db.get_image(IMAGE_PATH_CARDS + CARDBACK_FILENAME),
                        (dealer_x_pos, dealer_y_pos))
        else:
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)
            screen.blit(image_db.get_image(image), (dealer_x_pos, dealer_y_pos))
        first_card_hidden = False
        dealer_x_pos += GAP_BETWEEN_CARDS
        dealer_y_pos += 14


def plot_chips(screen,
               player_cash,
               chips_image_width,
               visible):
    """
    Plot the chips on the game board that will be used by the player to
    click and place the bets from.

    :param screen:
    :param player_cash:
    :param chips_image_width:
    :param visible: True is enabled and False is disabled (faded).
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    chips_x_pos, chips_y_pos = CHIPS_START_POS
    gap = chips_image_width + GAP_BETWEEN_CHIPS
    image_db = ImageDB.get_instance()
    if visible:
        if player_cash >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
    else:
        if player_cash >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))


def plot_bets(screen, player_bets):
    """
    Plot all the bet 'piles' which are available in the players bet stack.
    It can be one to four piles dependent if there has been a split or
    number of double down's.

    TODO: Should I make the positions smarter and connected to board scaling?

    :param screen:
    :param player_bets:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    image_db = ImageDB.get_instance()
    chip_x_pos = 30
    chip_y_pos = 360
    for bet in player_bets:
        for chip in bet:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + 'chip_{0}_w85h85.png'.format(chip)),
                        (chip_x_pos, chip_y_pos))
            chip_y_pos += 8
        chip_y_pos = 360
        chip_x_pos += 50


def plot_buttons(screen, button_status):
    """
    Plot all the buttons on the game board and based on the button_status
    plot them as visible and clickable or shaddowed/faded indicating not
    clickable.

    :param screen:
    :param button_status: True is enabled and False is disabled (faded).
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    button_x_pos, button_y_pos = BUTTONS_START_POS
    image_db = ImageDB.get_instance()
    if button_status.play is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.undo_bet is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.hit is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.stand is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.split is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.double_down is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS


# def plot_status_box(screen, text_font, player_cash, game_rounds):
#     account_text = text_font.render('Credits: {0}, Rounds: {1}'.format(player_cash, game_rounds), False, YELLOW_COLOR)
#     screen.blit(account_text, (620, GAME_BOARD_Y_SIZE - 33))


def plot_results(screen, text_font, message):
    """
    Plot a text message down in the status bar at the same location
    as where the buttons are plotted.
    To be able to see them you have to introduce a pause otherwise
    the message will instantly be overwritten by the buttons.

    :param screen:
    :param text_font:
    :param message:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    assert isinstance(message, str)
    text_to_plot = text_font.render(message, False, GOLD_COLOR)
    x_pos, y_pos = STATUS_START_POS
    screen.blit(text_to_plot, (x_pos, y_pos + 50))


def get_value_of_players_hand(hand):
    """
    Calculate the value of the players hand according to the Black Jack
    rules. First of all treat all face cards as 10.
    If the player gets an ace and the value of the rest of the
    hand is equal or lower than 10 the ace will be treated as a
    "Soft ace" with value 11. If the player has an ace or more and gets
    busted, aces will be changed to hard aces with value 1 one by
    one if a new bust occurs.

    :param hand: A list of :meth:`lib.playingcard.PlayingCard` objects.
    :return: Total value of the hand as an integer.

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    assert isinstance(hand, list)
    summary = 0
    num_of_soft_aces = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            # Treat all face cards as 10
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': face')
        elif rank == 1 and summary <= 10:
            # If an ace, start treating as Soft hand "high ace"
            summary += 11
            num_of_soft_aces += 1
            logging.debug(inspect.stack()[0][3] + ': soft ace')
        else:
            summary += rank
            logging.debug(inspect.stack()[0][3] + ': add rank {0} to summary givs {1}'.format(rank, summary))

        if num_of_soft_aces and summary > 21:
            # turn soft to hard ace , decrease with 10 since we already accounted for 11
            summary -= 10
            num_of_soft_aces -= 1
            logging.debug(inspect.stack()[0][3] + ': busted, toggle soft to hard ace')

    return summary


def get_value_of_dealers_hand(hand):
    """
    Calculate the value of the dealers hand according to the Black Jack
    rules. First of all treat all face cards as 10.
    If the card is an ace and if the total summary of the current hand
    will be 17 or more but less than 21 the dealer has to count the ace
    as a "soft" ace.

    :param hand: A list of :meth:`lib.playingcard.PlayingCard` objects.
    :return: Total value of the hand as an integer.

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    assert isinstance(hand, list)
    summary = 0
    hard_ace = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            # Treat all face cards as 10
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': face')
        elif rank == 1:
            # If the card is an ace and if the total summary of the current hand will be 17 or more
            # but less than 21 the dealer has to count the ace as a "soft" ace.
            if 17 <= (summary + 11) < 22:
                summary += 11
                logging.debug(inspect.stack()[0][3] + ': soft ace')
            else:
                # Save the ace for later evaluation when more cards are added to the summary
                hard_ace = 1
                summary += 1
                logging.debug(inspect.stack()[0][3] + ': hard ace')
                continue
        else:
            summary += rank
            logging.debug(inspect.stack()[0][3] + ': add rank {0} to summary givs {1}'.format(rank, summary))

        if hard_ace and 17 <= (summary + hard_ace * 10) < 22:
            # turn hard ace to soft, increase with 10 since 1 is already in the summary, total 11
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': toggle hard to soft ace')

    return summary


def is_cut_passed(shoe_of_decks):
    """
    Check that we haven't passed the "cut" in the shoe of decks where
    cut should be approx 18% of total shoe size.

    :param shoe_of_decks:
    :return: True if cut is passed else False.

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    status = False
    if shoe_of_decks is None or shoe_of_decks.length() < (NUM_OF_DECKS * 52 * 0.18):
        logging.debug(inspect.stack()[0][3] + 'Passed the "cut" in the shoe')
        status = True
    return status


def is_possible_split(player_cards):
    """
    Compare the first and second card in the players hand and if the
    rank of both cards are equal return True else return False.

    :param player_cards:
    :return: True or False

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    if len(player_cards) != 2:
        return False
    if player_cards[0].get_rank() != player_cards[1].get_rank():
        return False
    else:
        return True


def can_double_bet(player_bets, player_cash):
    """
    If the player has at least the amount of money as the first bet
    return True else return False

    :param player_bets:
    :param player_cash:
    :return: True or False

    """
    if player_cash < sum(player_bets[0]):
        return False
    else:
        return True


##########################
# Common support classes #
##########################


class ImageDB:
    """
    Instantiating this class into an object will create a singleton object
    which contains a library (dict) that stores the images when loaded.
    This will avoid reloading the image every time the function is called
    in the main game loop.
    Usage:
    instance = ImageDB.get_instance()
    image = instance.get_image(path)
    Or:
    image = ImageDB.get_instance().get_image(path)

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :return: An ImageDB instance.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        logging.info(inspect.stack()[0][3] + ':' + 'ImageDb instance created')
        self.image_library = {}

    def get_image(self, path):
        """
        If the image exists in the dictionary it will be returned.
        If image is not found in the dictionary it will be loaded from
        the file system or throw exception if not found.

        :param path: <string> containing the absolute directory path \
        to where the expected image is located.
        :return: An image in pygame Surface object format.

        """
        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        image = self.image_library.get(path)
        if image is None:
            logging.info(inspect.stack()[0][3] + ':' + path)
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            self.image_library[path] = image
        return image


class SoundDB:
    """
    Instantiating this class into an object will create a singleton object
    which contains a library (dict) that stores the sounds when loaded.
    This will avoid reloading the sound every time the function is called
    in the main game loop.
    Usage:
    instance = SoundDB.get_instance()
    sound = instance.get_sound(path)
    Or:
    sound = SoundDB.get_instance().get_sound(path)

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :return: An SoundDB instance.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        logging.info(inspect.stack()[0][3] + ':' + 'SoundDb instance created')
        self.sound_library = {}

    def get_sound(self, path):
        """
        If the sound exists in the dictionary it will be returned.
        If sound is not found in the dictionary it will be loaded from
        the file system or throw exception if not found.

        :param path: <string> containing the absolute directory path \
        to where the expected sound is located.
        :return: An sound in pygame Surface object format.

        """
        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        sound = self.sound_library.get(path)
        if sound is None:
            logging.info(inspect.stack()[0][3] + ':' + path)
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(canonicalized_path)
            self.sound_library[path] = sound
        return sound


class BlackJackCardFormatter:
    """
    A class which collects common methods which will manipulate data of
    the PlayingCard object to be used for a Black Jack game.

    """
    instance = None

    @classmethod
    def get_instance(cls, path=''):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :param path: Optional path to where the image is stored and will
        be prepended to the image name if provided.
        :return: A BlackJackCardFormatter instance.

        """
        if cls.instance is None:
            cls.instance = cls(path)
        return cls.instance

    def __init__(self, path):
        """
        Instantiate a singleton object and rank and suit attributes
        which holds a mapping between the integer values and corresponding
        string as a number or name.

        :param path:
        """
        logging.info(inspect.stack()[0][3] + ':' + 'BlackJackCardFormatter instance created')
        self.path = path
        self.card_rank = ["Invalid", "ace", "2", "3", "4", "5", "6", "7",
                          "8", "9", "10", "jack", "queen", "king"]
        self.card_suit = ["spades", "clubs", "diamonds", "hearts"]

    def get_string(self, card):
        """
        Convert the cards integer values for rank and suit to a string with
        the format <rank>_of_<suit>.png.
        If path has been provided to this instance creation it will be
        prepended to the image name with the format <path>/<rank>_of_<suit>.png.

        :param card: of type :meth:`lib.playingcard.PlayingCard`
        :return: <string>

        """
        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        image = self.path + self.card_rank[card.get_rank()] + "_of_" \
            + self.card_suit[card.get_suit()] + ".png"
        return image


class ButtonCollideArea:
    """
    Instantiating this class into an object will create a singleton object
    containing the defined collide areas for all the buttons.
    Since this will be called for every lap in the main game loop we will
    minimize the number of re-declarations.

    """
    instance = None

    @classmethod
    def get_instance(cls, common_vars):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :param common_vars:
        :return: A ButtonCollideArea instance.

        """
        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):
        """
        Instantiate a singleton object and create Pygame Rect area objects
        for all buttons to be able to detect when mouse is clicked in any of
        these areas.

        :param common_vars:
        """
        logging.info(inspect.stack()[0][3] + ':' + 'ButtonCollideArea instance created')
        button_x_pos, button_y_pos = BUTTONS_START_POS

        self.play_button_area = pygame.Rect(button_x_pos,
                                            button_y_pos,
                                            common_vars.button_image_width,
                                            common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.undo_bet_button_area = pygame.Rect(button_x_pos,
                                                button_y_pos,
                                                common_vars.button_image_width,
                                                common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.hit_button_area = pygame.Rect(button_x_pos,
                                           button_y_pos,
                                           common_vars.button_image_width,
                                           common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.stand_button_area = pygame.Rect(button_x_pos,
                                             button_y_pos,
                                             common_vars.button_image_width,
                                             common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.split_button_area = pygame.Rect(button_x_pos,
                                             button_y_pos,
                                             common_vars.button_image_width,
                                             common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.double_down_button_area = pygame.Rect(button_x_pos,
                                                   button_y_pos,
                                                   common_vars.button_image_width,
                                                   common_vars.button_image_height)


class ChipsCollideArea:
    """
    Instantiating this class into an object will create a singleton object
    containing the defined collide areas for all the chips.
    Since this will be called for every lap in the main game loop we will
    minimize the number of re-declarations.

    """
    instance = None

    @classmethod
    def get_instance(cls, common_vars):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :param common_vars:
        :return: A ChipsCollideArea instance.

        """
        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):
        """
        Instantiate a singleton object and create Pygame Rect area objects
        for all chips to be able to detect when mouse is clicked in any of
        these areas.

        :param common_vars:
        """
        logging.info(inspect.stack()[0][3] + ':' + 'ChipsCollideArea instance created')
        chips_x_pos, chips_y_pos = CHIPS_START_POS
        gap = common_vars.chips_image_width + GAP_BETWEEN_CHIPS
        self.chip_5_area = pygame.Rect(chips_x_pos,
                                       chips_y_pos,
                                       common_vars.chips_image_width,
                                       common_vars.chips_image_height)
        chips_x_pos += gap
        self.chip_10_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)
        chips_x_pos -= gap
        chips_y_pos += gap
        self.chip_50_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)
        chips_x_pos += gap
        self.chip_100_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)


class CommonVariables:
    """
    Instantiating this class into an object will create a singleton object
    containing all common variables to be passed around by reference
    between the main game loop and the various fsm states.

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :return: A CommonVariables instance.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        """
        Instantiate a singleton object with all attributes set to None.
        To be populated by the caller.

        """
        self.done = None
        self.screen = None
        self.shoe_of_decks = None
        self.player_hands = None
        self.hands_status = None
        self.double_downs = None
        self.dealer_cards = None
        self.dealer_last_hand = None
        self.player_deal = None
        self.player_hit = None
        self.player_cash = None
        self.player_bets = None
        self.bets_pos = None
        self.game_rounds = None
        self.text_font = None
        self.first_card_hidden = None
        self.pause_time = None
        self.button_image_width = None
        self.button_image_height = None
        self.chips_image_width = None
        self.chips_image_height = None


class ButtonStatus:
    """
    Instantiating this class into an object will create a singleton object
    containing a bool attribute for each button if it should be plotted
    visible or shadowed/faded to indicate if it can be clicked or not.

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        If instance is None create an instance of this class
        and return it, else return the existing instance.

        :return: A ButtonStatus instance.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        """
        Instantiate a singleton object with all attributes set to False.

        """
        self.play = False
        self.undo_bet = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False

    def reset(self):
        """
        Set all class attributes value to False.

        :return: None

        """
        self.play = False
        self.undo_bet = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False
