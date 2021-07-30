from deck import Deck
from player import Player
from card import Card
import time

class Driver:
    def __init__(self):
        self.community_cards = []
        self.players = []
        self.players_in_hand = []
        self.pot = 0
        self.current_max_bet = 0
        self.players_all_in = 0
        self.hand_over = False

    def populate_first_community_cards(self, deck):
        '''Puts the first three community cards on the table'''
        for i in range(3):
            self.community_cards.append(deck.deal_card())
        print("The first three community cards are: ")
        for i in self.community_cards:
            time.sleep(1)
            print(i)
        time.sleep(1)
        print()

    def populate_additional_community_card(self, deck):
        '''Puts the first three community cards on the table'''
        self.community_cards.append(deck.deal_card())
        print("The next community card is the " + str(self.community_cards[-1]) + "\n")
        print("The community cards are now: ")
        for i in self.community_cards:
            time.sleep(1)
            print(i)
        time.sleep(1)
        print()

    def generate_players(self):
        player_amount = 0
        while player_amount < 2 or player_amount > 8:
            try:
                print("How many players would you like to play against?")
                player_amount = int(input("Opponents: ")) + 1
                print()
            except:
                pass
            if player_amount < 2 or player_amount > 8:
                print()
                print("Please enter an amount of players between 1 and 7")
                print()

        for i in range(0, player_amount):
            self.players.append(Player(i))

    def determine_winner(self):
        '''Determines the winner of the hand'''
        if len(self.players_in_hand) == 1:
            return self.players_in_hand[0]
        else:
            current_highest = 0
            player_hand_scores = []
            for i in range(len(self.players_in_hand)):
                self.players_in_hand[i].made_to_end = True
                player_hand_scores.append(self.players_in_hand[i].evaluate_hand(self.community_cards, driver))
                if player_hand_scores[i] > current_highest:
                    current_highest = player_hand_scores[i]
            for i in range(len(self.players_in_hand) - 1, -1, -1):
                if player_hand_scores[i] < current_highest:
                    self.players_in_hand.pop(i)
            if len(self.players_in_hand) == 1:
                return self.players_in_hand[0]
            else:
                return self.tiebraker()

    def reward_winner(self, winning_player):
        '''Rewards the winning player of the hand'''
        if winning_player.is_all_in == False:
            winning_player.chip_count += self.pot
            pot = 0
            if winning_player.player_tag == 0:
                print("You won the hand\n")
            else:
                print("Computer Player " + str(winning_player.player_tag) + " won the hand\n")
        else:
            for i in self.players:
                if i.made_to_end == True and i.player_tag != winning_player.player_tag:
                    i.chip_count -= winning_player.bet_amount

    def all_players_action(self): #sometimes checking doesn't advance the turn
        '''Performs all of the actions of the players in a given round'''
        all_highest = False
        folded_counter = 0
        while all_highest == False and self.players_all_in < len(self.players_in_hand) - 1:
            for i in self.players_in_hand:
                i.reset_turn = True
                while i.reset_turn == True and i.is_all_in == False:
                    if i.player_tag == 0:
                        i.player_action(driver)
                    else:
                        i.computer_action(driver)
                if i.is_all_in == True:
                    self.players_all_in += 1
                if i.folded == True:
                    folded_counter += 1
                if folded_counter == len(self.players_in_hand) - 1:
                    break
                for j in range(len(self.players_in_hand)):
                    if self.players_in_hand[j].highest_better == False:
                        break
                    if j == len(self.players_in_hand) - 1:
                        all_highest = True
                if all_highest == True:
                    break
            for i in range(len(self.players_in_hand) - 1, -1, -1):
                if self.players_in_hand[i].folded == True:
                    self.players_in_hand.pop(i)
                if len(self.players_in_hand) == 1:
                    all_highest = True
                    self.hand_over = True
        for i in self.players_in_hand:
            i.highest_better = False

    def tiebraker(self):
        '''Determines the winnner of a hand if two or more players have the same hand value'''
        for i in self.players_in_hand:
            combined_cards = i.combine_cards(self.community_cards)
            for j in i.important_cards:
                for k in range(len(combined_cards) - 1, -1, -1):
                    if j.suit == combined_cards[k].suit and j.value == combined_cards[k].value:
                        combined_cards.pop(k)
            while len(i.important_cards) < 5:
                i.important_cards.append(Card(suit = combined_cards[0].suit, value = combined_cards[0].value))
                combined_cards.pop(0)
        winner_decided = False
        counter = 0
        while winner_decided == False:
            comparing_cards = []
            for i in self.players_in_hand:
                comparing_cards.append(i.important_cards[counter])
            comparing_cards.sort(key = lambda card: card.value, reverse = True)
            for i in range(len(comparing_cards) - 1, -1, -1):
                if comparing_cards[0] != comparing_cards[i - 1]:
                    self.players_in_hand.pop(i)
            if len(self.players_in_hand) == 1:
                winner_decided = True
            counter += 1
        return self.players_in_hand[0]

    def run_game(self):
        '''This is the main method that runs the entire game loop'''
        run_game_again = True
        while run_game_again == True:
            current_deck = Deck()
            self.generate_players()
            while len(self.players) > 1:
                self.run_hand(current_deck)
            print("Do you want to play again? (type y or n)")
            decision = input("Decision: ")
            if decision == "n":
                run_game_again = False

    def run_hand(self, deck):
        '''This method runs an entire hand'''
        self.hand_over = False
        self.community_cards = []
        self.current_max_bet = 0
        self.players_all_in = 0
        deck.reset_deck()
        self.players_in_hand = self.players.copy()
        for i in range(len(self.players_in_hand) - 1, -1, -1):
            if self.players_in_hand[i].chip_count == 0:
                self.players_in_hand.pop(i)
                self.players.pop(i)
        for i in self.players_in_hand:
            i.populate_hand(deck)
            i.evaluate_hand(self.community_cards, driver)
        self.all_players_action()
        if self.hand_over == True:
            self.reward_winner(self.determine_winner())            
            return
        self.populate_first_community_cards(deck)
        for i in self.players_in_hand:
            i.evaluate_hand(self.community_cards, driver)
        self.all_players_action()
        if self.hand_over == True:
            self.reward_winner(self.determine_winner())
            return
        self.populate_additional_community_card(deck)
        for i in self.players_in_hand:
            i.evaluate_hand(self.community_cards, driver)
        self.all_players_action()
        if self.hand_over == True:
            self.reward_winner(self.determine_winner())
            return
        self.populate_additional_community_card(deck)
        for i in self.players_in_hand:
            i.evaluate_hand(self.community_cards, driver)
        self.all_players_action()
        if self.hand_over == True:
            self.reward_winner(self.determine_winner())
            return
        self.hand_over = True
        self.reward_winner(self.determine_winner())
    
driver = Driver()
driver.run_game()