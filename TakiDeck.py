# import
from random import shuffle

def create_deck():
    # Function creates deck of cards for the game and returns it.
    card_colors = ['blue', 'red', 'yellow', 'green']
    # Card types that have several colors.
    card_types = list(range(1, 10))
    special_types = ['reverse', '+2', 'skip']
    card_types += special_types
    deck = [] # Create list of cards
    # Every cards is presented by dictionary, which has keys of 'card type' and 'color'
    for color in card_colors:
        for card_type in card_types:
            deck.append({'type': card_type, 'color': color})
            deck.append({'type': card_type, 'color': color})
    for i in range(0, 4):
        deck.append({'type': 'wild', 'color': 'black'})

    # Shuffle deck of cards
    shuffle(deck)
    return deck