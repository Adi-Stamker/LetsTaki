# imports
from socket import *
import threading
import json
"""
NOTE: EMAIL MUST BE A GMAIL ACCOUNT
"""

# Class creates connection with server
class TakiClient:
    def __init__(self):
        # class variables
        self.player = {}
        self.client_socket = None
        self.turn = {}
        self.current_card = {}
        self.win = {}
        self.your_turn = False
        self.cards_drawn = []

    def create_socket(self):
        # function creates connection with server if possible
        ip = '10.0.0.12'
        port = 8007
        try:
            self.client_socket = socket()
            self.client_socket.connect((ip, port))
            print("Connected to host successfully!")
        except:
            print("problem with connection")

    def join_game(self, details):
        # function receives player details and joins the player via login or register to the game.
        # returns true if possible, otherwise false.
        is_register = "register" in details.keys()
        is_login = "login" in details.keys()
        self.player = {'user_name': details['user_name']}
        self.client_socket.send(json.dumps(details).encode())
        msg = json.loads(self.client_socket.recv(1024).decode())
        if is_login and msg['login'] == 'failed':
            return False
        if is_register and msg['register'] == 'failed':
            return False
        return True

    def start_game(self):
        # function starts game
        start_dict = json.loads(self.client_socket.recv(1024).decode())
        self.turn = start_dict['turn']
        self.player['hand'] = start_dict['hand']
        self.current_card = start_dict['current_card']

    def send_card(self, card):
        # function receives a card and removes it from thr player's hand and sends card details to server.
        self.player['hand'].remove(card)
        self.client_socket.send(json.dumps({'card': card,
                                            'hand': self.player['hand']}).encode())

    def wait_turndata(self):
        # function makes the player wait till it is his turn
        turn_data = json.loads(self.client_socket.recv(1024).decode())
        self.win = turn_data['win']
        if not self.win:
            self.current_card = turn_data['current_card']
            self.cards_drawn = turn_data['draw_cards']
            self.draw_cards(self.cards_drawn)
  
    def draw_cards(self, cards):
        # function recieves cards and adds them to player's hand
        for card in cards:
            self.player['hand'].append(card)

    def receive_card(self):
        # function returns the card that was chosen by other players
        return json.loads(self.client_socket.recv(1024).decode())

    def change_cardcolor(self, wild_card, color):
        # function receives wild card and color
        # and changes the color of the wild card into the color that was chosen by player who used card.
        for card in self.player['hand']:
            if card['type'] == wild_card['type']:
                card['color'] = color

    def close_connection(self):
        # function closes connection with server
        if self.client_socket != None:
            self.client_socket.close()