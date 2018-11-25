#!/usr/bin/env python
"""
The Finite State Machine (FSM) used in the Black Jack game.

Copyright (C) Torbjorn Hedqvist - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license. See LICENSE file in the project
root for full license information.

"""

# Standard imports
import sys
import os

# Local imports
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from common import *
from carddecks import CardDecks  # , TestingCardDeck


class State(object):
    """
    Base Finite State Machine (FSM) class.

    """
    def next_state(self, state):
        """

        :param state:
        :return: None

        """
        self.__class__ = state

    def get_state(self):
        """

        :return: Name of current state as a string.

        """
        temp = str(self.__class__).strip('\'>').split('.')
        return temp[2]


class InitialState(State):
    """
    Initialize and reset all needed variables to be used in each round.

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.info(type(self).__name__ + ': Credits: {0}'.format(common_vars.player_cash))

        common_vars.hands_status = {'first_hand_blackjack': False,
                                    'first_hand_win': False,
                                    'first_hand_push': False,
                                    'first_hand_loose': False,
                                    'first_hand_busted': False,
                                    'second_hand_blackjack': False,
                                    'second_hand_win': False,
                                    'second_hand_push': False,
                                    'second_hand_loose': False,
                                    'second_hand_busted': False}
        common_vars.player_hands = []
        hand_instance = []
        common_vars.player_hands.append(hand_instance)
        common_vars.player_bets = []
        common_vars.bets_pos = []  # [(x,y), (x,y), ...]
        common_vars.game_rounds += 1
        common_vars.double_downs = [False, False]  # Flag for each possible hand
        common_vars.first_card_hidden = True
        button_status.reset()
        self.next_state(BettingState)


class BettingState(State):
    """
    Add or delete bets until player click on hit button,
    or exit to 'FinalState' if entering this state without
    cash enough to place a bet.

    """

    # Static class variables
    _current_bet = []
    _chips_visible = True
    # TODO: chips_visible as class variable?

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if common_vars.player_cash >= LOWEST_BET or sum(self._current_bet) > 0:
            plot_chips(common_vars.screen,
                       common_vars.player_cash,
                       common_vars.chips_image_width,
                       self._chips_visible)

            if sum(self._current_bet) > 0:
                button_status.play = True
                button_status.undo_bet = True
            else:
                button_status.play = False
                button_status.undo_bet = False
            plot_buttons(common_vars.screen, button_status)

            # Create detectable areas for the buttons and chips, used when mouse is clicked
            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            chips_collide_instance = ChipsCollideArea.get_instance(common_vars)

            sound_db = SoundDB.get_instance()
            chip_sound = sound_db.get_sound(SOUND_PATH + 'chipsstack.wav')

            temp_bet_list = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                    if button_collide_instance.play_button_area.collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet) > 0:
                        # Time to play
                        logging.info(type(self).__name__ + ': [Play] pressed')
                        logging.info(type(self).__name__ + ': Current bet is {0}'.format(self._current_bet))
                        logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                        # Initiate all needed variables for the next state
                        common_vars.player_bets.append(self._current_bet)
                        common_vars.dealer_cards = []
                        common_vars.first_card_hidden = True
                        common_vars.player_deal = False
                        common_vars.player_hit = False
                        button_status.play = False
                        button_status.undo_bet = False
                        # Reset local static state variables
                        self._current_bet = []
                        self._chips_visible = True
                        self.next_state(DealingState)
                    elif button_collide_instance.undo_bet_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet) > 0:
                        chip_sound.play()
                        common_vars.player_cash += self._current_bet.pop()
                        logging.info(type(self).__name__ + ': [Undo bet] pressed, remaining credits {0}'.
                                     format(common_vars.player_cash))

                    if len(self._current_bet) < 14:
                        self._chips_visible = True
                        if chips_collide_instance.chip_5_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 5:
                            chip_sound.play()
                            self._current_bet.append(5)
                            common_vars.player_cash -= 5
                        elif chips_collide_instance.chip_10_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 10:
                            chip_sound.play()
                            self._current_bet.append(10)
                            common_vars.player_cash -= 10
                        elif chips_collide_instance.chip_50_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 50:
                            chip_sound.play()
                            self._current_bet.append(50)
                            common_vars.player_cash -= 50
                        elif chips_collide_instance.chip_100_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 100:
                            chip_sound.play()
                            self._current_bet.append(100)
                            common_vars.player_cash -= 100
                    else:
                        self._chips_visible = False

            temp_bet_list.append(self._current_bet)
            plot_bets(common_vars.screen, temp_bet_list)
        else:
            # Out of cash, end the game
            self.next_state(FinalState)


class DealingState(State):
    """
    Deal the first two cards for both dealer and player.

    The first four iterations of entering this state will pull
    1. A card for the player + pause,
    2. A card for the dealer + pause,
    3. A second card for the player + pause
    4. A second card for the dealer + pause
    5. Check if BlackJack for player and if not,
    wait for player to push hit, stand or possibly split.

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
            # common_vars.shoe_of_decks = TestingCardDeck()

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0  # We have only one hand for the player in this state
        if len(common_vars.dealer_cards) < 2:
            # Create a short pause between the dealt first two cards
            common_vars.pause_time = PAUSE_TIMER1

            if not common_vars.player_hands[first_hand]:
                # Empty hand, pull first card for the player
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)

            elif not common_vars.dealer_cards:
                # Empty hand, pull first card for the dealer
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)

            elif len(common_vars.player_hands[first_hand]) == 1:
                # Pull second card for the player
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)

            elif len(common_vars.dealer_cards) == 1:
                # Pull second card for the dealer
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)
        elif not button_status.hit:
            # Two cards picked for both player and dealer, let's evaluate if
            # BlackJack, Tie or possible Split.
            logging.info(type(self).__name__ + ': Two cards dealt, first evaluation')
            common_vars.pause_time = 0
            value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
            for hand in common_vars.player_hands:
                value_of_players_hand = get_value_of_players_hand(hand)
                if value_of_players_hand == 21 and len(common_vars.player_hands) != 2:  # Not in split mode
                    # Let's evaluate and compare towards dealers hand
                    common_vars.first_card_hidden = False
                    if value_of_dealers_hand == 21:
                        # A Tie or push, bets going back to player
                        logging.info(type(self).__name__ + ':' + 'Push')
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results(common_vars.screen, common_vars.text_font, 'Push')
                        common_vars.hands_status['first_hand_push'] = True
                        common_vars.player_cash += sum(common_vars.player_bets[0])
                    else:
                        # A BlackJack, pay 3/2 (1.5)
                        logging.info(type(self).__name__ + ':' + 'Black Jack!!!')
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results(common_vars.screen, common_vars.text_font, 'Black Jack!!!')
                        common_vars.hands_status['first_hand_blackjack'] = True
                        common_vars.player_cash += sum(common_vars.player_bets[0])  # First get the bet back
                        common_vars.player_cash += int(sum(common_vars.player_bets[0]) * 1.5)

                    common_vars.dealer_last_hand = value_of_dealers_hand
                    # Create a short pause to present the result of the hand
                    common_vars.pause_time = PAUSE_TIMER3
                    button_status.reset()
                    self.next_state(InitialState)
                elif len(common_vars.player_hands) != 2 and is_possible_split(hand):
                    # Not in split already and two equal cards
                    button_status.split = can_double_bet(common_vars.player_bets, common_vars.player_cash)
                    button_status.hit = True
                else:
                    button_status.hit = True
        else:
            button_status.hit = True
            button_status.stand = True
            button_status.double_down = can_double_bet(common_vars.player_bets, common_vars.player_cash)

        # Create detectable areas for the buttons, used when mouse is clicked
        button_collide_instance = ButtonCollideArea.get_instance(common_vars)

        plot_buttons(common_vars.screen, button_status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                if button_status.hit and button_collide_instance.hit_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Hit] pressed')
                    card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands[first_hand].append(card)
                    button_status.split = False
                    button_status.double_down = False
                    self.next_state(PlayerHitState)
                elif button_status.stand and button_collide_instance.stand_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Stand] pressed')
                    self.next_state(DealerInitState)
                elif button_status.double_down and button_collide_instance.double_down_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Double down] pressed')
                    # Double the bet before going to DealerInitState
                    common_vars.player_cash -= sum(common_vars.player_bets[0])
                    common_vars.player_bets.append(common_vars.player_bets[0])
                    logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                    card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands[first_hand].append(card)  # Pull a third card
                    common_vars.double_downs[first_hand] = True
                    button_status.double_down = False
                    self.next_state(DealerInitState)
                elif button_status.split and button_collide_instance.split_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    # Double the bet before going to SplitState
                    logging.info(type(self).__name__ + ': [Split] pressed')
                    common_vars.player_cash -= sum(common_vars.player_bets[0])
                    common_vars.player_bets.append(common_vars.player_bets[0])
                    # button_status.split = False
                    button_status.reset()
                    logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                    self.next_state(SplitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class SplitState(State):
    """
    Split the players first two cards into two hands.
    Pull a new card to each of the hands and if the player is lucky enough
    to get 21 in both hands evaluate it towards the dealers hand for a
    double Black Jack or Tie.
    Else, head on to next state 'PlayerHitState'.

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)
        plot_buttons(common_vars.screen, button_status)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0
        second_hand = 1
        if len(common_vars.player_hands) == 1:
            hand_instance = []
            common_vars.player_hands.append(hand_instance)
            common_vars.player_hands[second_hand].append(common_vars.player_hands[first_hand].pop())

        logging.info(type(self).__name__ + ': {0}:{1}'.
                     format(len(common_vars.player_hands[first_hand]),
                            len(common_vars.player_hands[second_hand])))

        if len(common_vars.player_hands[second_hand]) != 2:
            # Fill up each hand with one additional card
            common_vars.pause_time = PAUSE_TIMER1
            if len(common_vars.player_hands[first_hand]) < 2:
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)
            elif len(common_vars.player_hands[second_hand]) < 2:
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[second_hand].append(card)
        else:
            # Both hands have now two cards, let's evaluate
            value_of_players_hands = 0
            for hand in common_vars.player_hands:
                value_of_players_hands += get_value_of_players_hand(hand)
            if value_of_players_hands != 42:
                # Not two times 21 or the answer to the meaning of life, continue to next state
                button_status.hit = True
                button_status.stand = True
                button_status.double_down = can_double_bet(common_vars.player_bets, common_vars.player_cash)
                self.next_state(PlayerHitState)
            else:
                # WOW!!! The player got two two-card hands with 21, what's the chance for this
                value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
                common_vars.dealer_last_hand = value_of_dealers_hand
                sum_of_bets = 0
                for bet in common_vars.player_bets:
                    sum_of_bets += sum(bet)
                logging.info(type(self).__name__ + ':' + 'sum_of_bets = {0}'.format(sum_of_bets))
                if value_of_dealers_hand == 21:
                    # A Tie or push, bets going back to player
                    logging.info(type(self).__name__ + ':' + 'Push')
                    plot_results(common_vars.screen, common_vars.text_font, 'Push')
                    common_vars.player_hands['first_hand_push'] = True
                    common_vars.player_hands['second_hand_push'] = True
                    common_vars.player_cash += sum_of_bets
                else:
                    # Double BlackJack, pay 3/2 (1.5)
                    logging.info(type(self).__name__ + ':' + 'Double BlackJack!!!')
                    plot_results(common_vars.screen, common_vars.text_font, 'Double Black Jack!!!')
                    common_vars.player_hands['first_hand_blackjack'] = True
                    common_vars.player_hands['second_hand_blackjack'] = True
                    common_vars.player_cash += sum_of_bets  # First get the bet back
                    common_vars.player_cash += int(sum_of_bets * 1.5)

                # Create a short pause to present the result of the hand
                common_vars.pause_time = PAUSE_TIMER3
                button_status.reset()
                self.next_state(InitialState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class PlayerHitState(State):
    """
    Remain in this state until player is satisfied (stand) or busted.

    Pull cards if player push 'hit', check the results, bail out back to
    'InitialState' if player are busted or head on to next state if
    player push 'stand'.

    Black Jack rules:
    The value of cards two through ten is their pip value (2 through 10).
    Face cards (Jack, Queen, and King) are all worth ten.
    Aces can be worth one or eleven.
    As normal casino rules this game does not allow 5-Charlie or 7-Charlie.

    """

    # Static class variables
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands = len(common_vars.player_hands)
        if num_of_hands == 2:
            image_db = ImageDB.get_instance()
            if self._current_hand == 0:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100, 315))
            else:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100 + GAP_BETWEEN_SPLIT, 315))

        value_of_players_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])
        if value_of_players_hand > 21:
            logging.info(type(self).__name__ + ': Player is busted {0}'.format(value_of_players_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Player is busted {0}'.format(value_of_players_hand))
            if num_of_hands == 1:
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            elif self._current_hand == 0:
                # In split mode and first hand busted
                common_vars.hands_status['first_hand_busted'] = True
                button_status.double_down = True
                self._current_hand += 1
            elif self._current_hand == 1 and common_vars.hands_status['first_hand_busted']:
                # In split mode and both hands busted
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # In split mode and first hand ok, but second hand busted
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                self.next_state(DealerInitState)
        elif value_of_players_hand == 21:
            if num_of_hands == 2 and self._current_hand == 0:
                logging.info(type(self).__name__ + ': first hand has ' + '21, save this hand for later evaluation')
                self._current_hand += 1
            else:
                logging.info(type(self).__name__ + ': second hand has ' + '21, lets see what the dealer has')
                self._current_hand = 0
                self.next_state(DealerInitState)
        else:
            # Create detectable areas for the buttons, used when mouse is clicked
            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            plot_buttons(common_vars.screen, button_status)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                    if button_collide_instance.hit_button_area.collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Hit] pressed')
                        card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands[self._current_hand].append(card)
                        button_status.double_down = False
                    elif button_status.double_down and button_collide_instance.double_down_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Double down] pressed')
                        common_vars.double_downs[self._current_hand] = True
                        common_vars.player_cash -= sum(common_vars.player_bets[0])
                        common_vars.player_bets.append(common_vars.player_bets[0])
                        logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                        card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands[self._current_hand].append(card)
                        if num_of_hands == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                        else:
                            self._current_hand = 0
                            button_status.double_down = False
                            self.next_state(DealerInitState)
                    elif button_collide_instance.stand_button_area.collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Stands] pressed, player has {0}'.
                                     format(value_of_players_hand))
                        if num_of_hands == 2 and self._current_hand == 0:
                            # One hand left to handle
                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class DealerInitState(State):
    """
    Based on the two pulled cards for the dealer and the cards that have
    been pulled for the player in previous states,
    check if the dealer wins any of the hands or if we have any draw's.
    If not head on to the next state 'DealerHitState'.

    """

    # Static class variables
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        common_vars.first_card_hidden = False  # Show the dealers second card
        num_of_hands = len(common_vars.player_hands)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])

        if value_of_dealer_hand == 21:
            logging.info(type(self).__name__ +
                         ': Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_hand))
            if value_of_player_hand < 21:
                # Player's current hand loose against dealer
                common_vars.pause_time = PAUSE_TIMER3
                plot_results(common_vars.screen, common_vars.text_font,
                             'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_hand))
                if num_of_hands == 1:
                    # Only one player hand
                    common_vars.hands_status['first_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands == 2 and self._current_hand == 0:
                    # Pop one bet pile from the player which is lost
                    common_vars.player_bets.pop()
                    # First hand in split mode, step to next hand
                    self._current_hand += 1
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    # Second hand in a split mode
                    common_vars.hands_status['second_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
            else:
                logging.info(type(self).__name__ + ': Both dealer and player has 21, a push')
                common_vars.pause_time = PAUSE_TIMER3
                plot_results(common_vars.screen, common_vars.text_font,
                             'Both dealer and player has 21, a push')
                # Pay back one bet to player
                common_vars.player_cash += sum(common_vars.player_bets.pop())
                if num_of_hands == 1 or self._current_hand == 1:
                    # Only one player hand or last hand evaluated
                    common_vars.hands_status['first_hand_push'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    # First hand in split mode, step to next hand
                    self._current_hand += 1
                    common_vars.hands_status['first_hand_push'] = True
        elif value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_hand:
            # Dealer has at least 16 and more than the player and the dealer wins
            logging.info(type(self).__name__ +
                         ': Dealer wins with {0} over player {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Dealer wins with {0} over player {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            if num_of_hands == 1 or self._current_hand == 1:
                # Only one player hand or last hand evaluated
                common_vars.hands_status['first_hand_loose'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status['first_hand_loose'] = True
        elif value_of_player_hand > 21:
            # Player is busted from previous state (possibly at a double down)
            logging.info(type(self).__name__ +
                         ': Player is busted with {0}'.format(value_of_player_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Player is busted with {0}'.format(value_of_player_hand))
            if num_of_hands == 1 or self._current_hand == 1:
                # Only one player hand or last hand evaluated
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode, step to next hand
                self._current_hand += 1
                common_vars.hands_status['first_hand_busted'] = True
        else:
            self._current_hand = 0
            self.next_state(DealerHitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class DealerHitState(State):
    """
    Player is ready with his/her hand(s) and the dealers two first cards
    did not beat the players cards in previous state 'DealerInitState'.
    Time for the dealer to pull cards until he wins or gets busted,
    according to the rules of 16 & 17.

    """

    # Static class variables
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands = len(common_vars.player_hands)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])

        if value_of_dealer_hand < 16:
            # Dealer is forced to hit until 16, no matter what hand the player has
            card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = 1.0
        elif value_of_dealer_hand < 17 and value_of_dealer_hand < value_of_player_hand:
            # Dealer has less than 17 and less than the players current hand
            card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = 1.0
        elif value_of_player_hand > 21 or 22 > value_of_dealer_hand > value_of_player_hand:
            # Dealer wins this hand
            common_vars.pause_time = PAUSE_TIMER3
            if value_of_player_hand > 21:
                logging.info(type(self).__name__ +
                             ': Player is busted {0}'.format(value_of_player_hand))
                plot_results(common_vars.screen, common_vars.text_font,
                             'Player is busted {0}'.format(value_of_player_hand))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_busted'] = True
                else:
                    common_vars.hands_status['second_hand_busted'] = True
            else:
                logging.info(type(self).__name__ +
                             ': Dealer wins with {0} over player {1}'.
                             format(value_of_dealer_hand, value_of_player_hand))
                plot_results(common_vars.screen, common_vars.text_font,
                             'Dealer wins with {0} over player {1}'.
                             format(value_of_dealer_hand, value_of_player_hand))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    common_vars.hands_status['second_hand_loose'] = True
            # Pop one bet pile from the player which is lost
            common_vars.player_bets.pop()
            if common_vars.double_downs[self._current_hand]:
                # Pop the second bet pile for this hand which has been doubled down'ed
                common_vars.player_bets.pop()
            common_vars.pause_time = PAUSE_TIMER3
            if num_of_hands == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode evaluated, let's switch to second hand
                self._current_hand += 1
        elif value_of_dealer_hand == value_of_player_hand:
            # Both dealer and player has the same value, a push
            common_vars.pause_time = PAUSE_TIMER3
            logging.info(type(self).__name__ +
                         ': A push, dealer has {0}, player has {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            plot_results(common_vars.screen, common_vars.text_font,
                         'A push dealer has {0}, player has {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            if self._current_hand == 0:
                common_vars.hands_status['first_hand_push'] = True
            else:
                common_vars.hands_status['second_hand_push'] = True

            if num_of_hands == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode evaluated, let's switch to second hand
                self._current_hand += 1

            # Pay back one bet to player
            common_vars.player_cash += sum(common_vars.player_bets.pop())
            if common_vars.double_downs[self._current_hand]:
                # And pay back the second bet pile for this hand which has been doubled down'ed
                common_vars.player_cash += sum(common_vars.player_bets.pop())

        else:
            # Player wins this hand
            if self._current_hand == 0:
                common_vars.hands_status['first_hand_win'] = True
            else:
                common_vars.hands_status['second_hand_win'] = True
            logging.info(type(self).__name__ +
                         ': Player wins with {0} over dealer {1}, bet is {2}'.
                         format(value_of_player_hand, value_of_dealer_hand, common_vars.player_bets[0]))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         "Player wins with {0} over dealer {1}".format(value_of_player_hand, value_of_dealer_hand))
            common_vars.player_cash += sum(common_vars.player_bets.pop()) * 2
            if common_vars.double_downs[self._current_hand]:
                # Doubled down hand, add additional win
                logging.info(type(self).__name__ +
                             ': Double down, add additional win {0}'.
                             format(common_vars.player_bets[0]))
                common_vars.player_cash += sum(common_vars.player_bets.pop()) * 2
            common_vars.dealer_last_hand = value_of_dealer_hand
            if num_of_hands == 1 or self._current_hand == 1:
                # We're done if there is one player hand only or second hand has been evaluated
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # First hand in split mode evaluated, let's switch to second hand
                self._current_hand += 1

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class FinalState(State):
    """
    The player is out of money.
    Remain in this state until he/she hits the quit [x] button.

    TODO: Need some fancier handling with menus and stuff when the game is over.

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        # Plot the players current account value
        account_text = common_vars.text_font.render("Game Over, you're out of money", False, GOLD_COLOR)
        common_vars.screen.blit(account_text, (5, GAME_BOARD_Y_SIZE - 30))

        # React on mouse click on [x]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
