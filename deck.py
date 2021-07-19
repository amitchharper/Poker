import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
    
    def __str__(self):
        all_cards = ""
        for i in self.cards:
            all_cards += str(i) + ", "
        return all_cards
    
    def deal_card(self):
        '''Selects a random card out of the deck, removes it, and returns that card'''
        card_index = random.choice(range(len(self.cards)))
        return_card = self.cards.pop(card_index)
        return return_card

    def reset_deck(self):
        suits = ["♠", "♣", "♥", "♦"]
        values = list(range(2, 15))
        self.cards = []
        for i in suits:
            for j in values:
                self.cards.append(Card(i, j))