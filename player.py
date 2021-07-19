from card import Card

class Player:
    def __init__(self, player_tag):
        self.hand = []

        #Store the cards of the relevant hand ranking, i.e. if the highest rank is a straight, store the five cards that make
        #up the straight.
        self.important_cards = [] 

        self.hand_value = 0
        self.player_tag = player_tag
        self.chip_count = 1000
        self.bet_amount = 0
        self.highest_better = False
        self.folded = False
        self.reset_turn = False
        self.is_all_in = False
        self.made_to_end = False
    
    def __str__(self):
        if self.player_tag == 0:
            return "You"
        else:
            return "Computer Player " + str(self.player_tag)

    def player_action(self, driver): #make it so you can all in at any time
        '''This method performs an individual player action'''
        decision = -1
        self.reset_turn = False
        self.highest_better = False
        self.folded = False
        self.is_all_in = False
        while decision not in range(1, 8):
            try:
                if self.bet_amount == driver.current_max_bet:
                    if self.player_tag == 0:
                        decision = print("You, choose action: \n1. Fold\n2. Check\n3. Raise\n4. All In\n5. Check Cards\n6. Check Chip Counts\n7. Check Players in Hand\n")
                    else:
                        decision = print("Computer Player " + str(self.player_tag) + ", choose action: \n1. Fold\n2. Check\n3. Raise\n4. All In\n5. Check Cards\n6. Check Chip Counts\n7. Check Players in Hand\n")
                    decision = int(input("Choice: "))
                    print()
                elif self.bet_amount != driver.current_max_bet and driver.current_max_bet < self.chip_count:
                    print("The amount needed to call is " + str((driver.current_max_bet - self.bet_amount)) + "\n")
                    if self.player_tag == 0:
                        decision = print("You, choose action: \n1. Fold\n2. Call\n3. Raise\n4. All In\n5. Check Cards\n6. Check Chip Counts\n7. Check Players in Hand\n")
                    else:
                        decision = print("Computer Player " + str(self.player_tag) + ", choose action: \n1. Fold\n2. Call\n3. Raise\n4. All In\n5. Check Cards\n6. Check Chip Counts\n7. Check Players in Hand\n")
                    decision = int(input("Choice: "))
                    print()
                else:
                    if self.player_tag == 0:
                        decision = print("You, choose action: \n1. Fold\n2. All In\n3. Check Cards\n4. Check Chip Counts\n5. Check Players in Hand\n")
                    else:
                        decision = print("Computer Player " + str(self.player_tag) + ", choose action: \n1. Fold\n2. All In\n3. Check Cards\n4. Check Chip Counts\n5. Check Players in Hand\n")
                    decision = int(input("Choice: "))
                    print()
            except:
                pass
            if self.is_all_in == True and decision > 5:
                decision = -1
            if decision not in range(1, 7):
                print()
                print("Please choose a number between 1 and 5 to make a decision")
                print()
        if decision == 1:
            self.fold(driver)
        elif decision == 2:
            if self.is_all_in == True: #rename is_all_in to something more properly descriptive
                self.all_in(driver)
            else:
                self.check_or_call(driver)
        elif decision == 3:
            if self.is_all_in == True:
                self.check_cards(driver)
            else:
                self.raise_bet(driver)
        elif decision == 4:
            if self.is_all_in == True:
                self.check_chips(driver)
            else:
                self.all_in(driver)
        elif decision == 5:
            if self.is_all_in == True:
                self.check_players_in_hand(driver)
            else:
                self.check_cards(driver)
        elif decision == 6:
            self.check_chips(driver)
        elif decision == 7:
            self.check_players_in_hand(driver)

    def fold(self, driver):
        for i in range(len(driver.players_in_hand) - 1, -1, -1):
            if driver.players_in_hand[i].player_tag == self.player_tag:
                self.highest_better = True
                self.folded = True

    def check_or_call(self, driver):
        difference = driver.current_max_bet - self.bet_amount
        self.bet_amount += difference
        driver.pot += difference
        self.chip_count -= difference
        self.highest_better = True

    def raise_bet(self, driver):
        difference = driver.current_max_bet - self.bet_amount
        raise_amount = 0
        while raise_amount <= difference or raise_amount < 0 or raise_amount > self.chip_count:
            try:
                print("How much would you like to raise?")
                raise_amount = int(input("Amount: "))
                print()
            except:
                pass
            if raise_amount <= difference or raise_amount < 0 or raise_amount > self.chip_count:
                print("Please enter a valid amount (more than " + str(difference) + ") and below your remaining chip count (" + str(self.chip_count) + ")")
        self.bet_amount += raise_amount
        driver.pot += raise_amount
        self.chip_count -= raise_amount
        for i in driver.players_in_hand:
            i.highest_better = False
        self.highest_better = True
        driver.current_max_bet = self.bet_amount

    def all_in(self, driver):
        self.bet_amount += self.chip_count
        driver.pot += self.bet_amount
        self.chip_count = 0
        self.is_all_in = True
        if self.bet_amount > driver.current_max_bet:
            for i in driver.players_in_hand:
                i.highest_better = False
            self.highest_better = True
            driver.current_max_bet = self.bet_amount
        elif self.bet_amount == driver.current_max_bet:
            self.highest_better = True
        print("After all in: " + str(self.chip_count))

    def check_cards(self, driver):
        print("Your cards are:")
        for i in self.hand:
            print(i)
        print()
        if len(driver.community_cards) > 0:
            print("The community cards are:")
            for i in driver.community_cards:
                print(i)
            print()
        else:
            print("There are no community cards\n")
        self.reset_turn = True

    def check_chips(self, driver):
        for i in driver.players:
            if i.player_tag == 0:
                print("You have " + str(i.chip_count) + " chips")
            else:
                print("Computer Player " + str(i.player_tag) + " has " + str(i.chip_count) + " chips")
        print()
        self.reset_turn = True

    def check_players_in_hand(self, driver):
        print("The following players are still in the hand:\n")
        for i in driver.players_in_hand:
            print(i)
        print()
        self.reset_turn = True

    def populate_hand(self, deck):
        '''Gives the player starting cards, not including community cards'''
        self.hand = []
        self.important_cards = []
        self.bet_amount = 0
        for i in range(2):
            self.hand.append(deck.deal_card())
        if self.player_tag == 0:
            print("You have the following cards:")
        else: 
            print("Computer Player " + str(self.player_tag) + " has the following cards:")
        for i in self.hand:
            print(i)
        print()

    def combine_cards(self, community_cards):
        '''Combines that cards from the player's hand and the community cards and sorts them by value'''
        combined_cards = self.hand + community_cards
        combined_cards.sort(key = lambda card: card.value, reverse = True)
        return combined_cards

    def evaluate_hand(self, community_cards, driver):
        '''Determines the value of the player's hand combined with the community cards'''
        combined_cards = self.combine_cards(community_cards)
        if self.royal_flush(combined_cards) == True:
            self.hand_value = 10
        elif self.straight_flush(combined_cards) == True:
            self.hand_value = 9
        elif self.four_of_a_kind(combined_cards) == True:
            self.hand_value = 8
        elif self.full_house(combined_cards) == True:
            self.hand_value = 7
        elif self.flush(combined_cards) == True:
            self.hand_value = 6
        elif self.straight(combined_cards) == True:
            self.hand_value = 5
        elif self.three_of_a_kind(combined_cards) == True:
            self.hand_value = 4
        elif self.two_pair(combined_cards) == True:
            self.hand_value = 3
        elif self.pair(combined_cards) == True:
            self.hand_value = 2
        else:
            self.important_cards.append(Card(suit = combined_cards[0].suit, value = combined_cards[0].value))
            self.hand_value = 1
        if driver.hand_over == False:
            if self.player_tag == 0:
                print(str(self) + " have a " + self.translateRank() + "\n")
        else:
            if self.player_tag == 0:
                print(str(self) + " have a " + self.translateRank() + "\n")
            else:
                print(str(self) + " has a " + self.translateRank() + "\n")
        return self.hand_value


    def translateRank(self):
        '''Translates the player's hand rank to the hand type'''
        if self.hand_value == 1:
            return "High Card"
        elif self.hand_value == 2:
            return "Pair"
        elif self.hand_value == 3:
            return "Two Pair"
        elif self.hand_value == 4:
            return "Three Of A Kind"
        elif self.hand_value == 5:
            return "Straight"
        elif self.hand_value == 6:
            return "Flush"
        elif self.hand_value == 7:
            return "Full House"
        elif self.hand_value == 8:
            return "Four Of A Kind"
        elif self.hand_value == 9:
            return "Straight Flush"
        elif self.hand_value == 10:
            return "Royal Flush"
        
    def pair(self, combined_cards):
        '''Determines if the player has a pair'''
        for i in range(0, len(combined_cards) - 1):
            if combined_cards[i].value == combined_cards[i + 1].value:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                return True
        return False

    def two_pair(self, combined_cards):
        '''Determines if the player has a two pair'''
        pair_counter = 0
        i = 0
        while i < len(combined_cards) - 1:
            if combined_cards[i].value == combined_cards[i + 1].value:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                pair_counter = pair_counter + 1
                i += 2
            else:
                i += 1
            if pair_counter >= 2:
                return True
        self.important_cards = []
        return False

    def three_of_a_kind(self, combined_cards):
        '''Determines if the player has a three of a kind'''
        for i in range(0, len(combined_cards) - 2):
            if combined_cards[i].value == combined_cards[i + 2].value:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                self.important_cards.append(Card(suit = combined_cards[i + 2].suit, value = combined_cards[i + 2].value))
                return True
        return False

    def straight(self, combined_cards):
        '''Determines if the player has a straight'''
        straight_counter = 0
        if combined_cards[0].value == 14:
            combined_cards.append(Card(combined_cards[0].suit, 1))
        for i in range(0, len(combined_cards) - 1):
            if combined_cards[i].value == combined_cards[i + 1].value + 1:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                straight_counter += 1
            elif combined_cards[i].value == combined_cards[i + 1].value:
                pass
            else:
                self.important_cards = []
                straight_counter = 0
            if straight_counter == 5:
                if combined_cards[-1].value == 14:
                    combined_cards.pop(0)
                return True
        if combined_cards[0].value == 14:
            combined_cards.pop(-1)
        self.important_cards = []
        return False
    
    def flush(self, combined_cards):
        '''Determines if the player has a flush'''
        combined_cards.sort(key = lambda card: card.suit, reverse = True)
        for i in range(0, len(combined_cards) - 4): 
            if combined_cards[i].suit == combined_cards[i + 4].suit:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                self.important_cards.append(Card(suit = combined_cards[i + 2].suit, value = combined_cards[i + 2].value))
                self.important_cards.append(Card(suit = combined_cards[i + 3].suit, value = combined_cards[i + 3].value))
                self.important_cards.append(Card(suit = combined_cards[i + 4].suit, value = combined_cards[i + 4].value))
                combined_cards.sort(key = lambda card: card.value)
                self.important_cards.sort(key = lambda card: card.value, reverse = True)
                return True
        combined_cards.sort(key = lambda card: card.value, reverse = True)
        return False

    def full_house(self, combined_cards):
        '''Determines if the player has a full house'''
        got_pair = False
        got_three_of_a_kind = False
        i = 0
        while i < len(combined_cards) - 2:
            if combined_cards[i].value == combined_cards[i + 2].value:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                self.important_cards.append(Card(suit = combined_cards[i + 2].suit, value = combined_cards[i + 2].value))
                got_three_of_a_kind = True
                i += 3
            elif combined_cards[i].value == combined_cards[i + 1].value:
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                got_pair = True
                i += 2
            else:
                i += 1
            if got_pair == True and got_three_of_a_kind == True:
                return True
        if len(self.hand) > 2:
            if combined_cards[-1].value == combined_cards[-2].value and combined_cards[-1].value != combined_cards[-3].value:
                self.important_cards.append(Card(suit = combined_cards[-1].suit, value = combined_cards[-1].value))
                self.important_cards.append(Card(suit = combined_cards[-2].suit, value = combined_cards[-2].value))
                got_pair = True
        if got_pair == True and got_three_of_a_kind == True:
            return True
        self.important_cards = []
        return False

    def four_of_a_kind(self, combined_cards):
        '''Determines if the player has a four of a kind'''
        combined_cards.sort(key = lambda card: card.value, reverse = True)
        for i in range(0, len(combined_cards) - 3):
            if combined_cards[i].value == combined_cards[i + 3].value :
                self.important_cards.append(Card(suit = combined_cards[i].suit, value = combined_cards[i].value))
                self.important_cards.append(Card(suit = combined_cards[i + 1].suit, value = combined_cards[i + 1].value))
                self.important_cards.append(Card(suit = combined_cards[i + 2].suit, value = combined_cards[i + 2].value))
                self.important_cards.append(Card(suit = combined_cards[i + 3].suit, value = combined_cards[i + 3].value))
                return True
        return False

    def straight_flush(self, combined_cards):
        '''Determines if the player has a straight flush'''
        temp_combined_cards = []
        combined_cards.sort(key = lambda card: card.suit, reverse = True)
        counter = 1
        for i in range(0, len(combined_cards) - 4): 
            if combined_cards[i].suit == combined_cards[i + 4].suit:
                for j in range(i, len(combined_cards)):
                    if combined_cards[i].suit == combined_cards[j].suit:
                        temp_combined_cards.append(Card(suit = combined_cards[j].suit, value = combined_cards[j].value))
                break
        if len(temp_combined_cards) > 4:
            straight_counter = 1
            temp_combined_cards.sort(key = lambda card: card.value, reverse = True)
            if temp_combined_cards[0].value == 14:
                temp_combined_cards.append(Card(temp_combined_cards[0].suit, 1))
            for i in range(0, len(temp_combined_cards) - 1):
                if temp_combined_cards[i].value == temp_combined_cards[i + 1].value + 1:
                    self.important_cards.append(Card(suit = temp_combined_cards[i].suit, value = temp_combined_cards[i].value))
                    straight_counter += 1
                elif temp_combined_cards[i].value == temp_combined_cards[i + 1].value:
                    pass
                else:
                    self.important_cards = []
                    straight_counter = 1
                if straight_counter == 5:
                    self.important_cards.append(Card(suit = temp_combined_cards[i + 1].suit, value = temp_combined_cards[i + 1].value))
                    if temp_combined_cards[-1].value == 14:
                        temp_combined_cards.pop(0)
                    return True
            if temp_combined_cards[0].value == 14:
                temp_combined_cards.pop(-1)
            self.important_cards = []
        return False
        

    def royal_flush(self, combined_cards):
        '''Determines if the player has a royal flush'''
        if self.straight_flush(combined_cards) == True:
            if self.important_cards[0].value == 14:
                return True
        self.important_cards = []
        return False