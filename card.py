import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        cards = []

    def __str__(self): 
        if self.value == 11:
            return f"Jack of {self.suit}" 
        elif self.value == 12:
            return f"Queen of {self.suit}" 
        elif self.value == 13:
            return f"King of {self.suit}" 
        elif self.value == 14:
            return f"Ace of {self.suit}" 
        elif self.value == 1:
            return f"Ace of {self.suit}"
        return f"{self.value} of {self.suit}"