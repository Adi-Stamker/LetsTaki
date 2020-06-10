# imports
from socket import *
from TakiDeck import *
from DBServer import *
import threading
import json

# Class create connection with client
class TakiServer:
    def __init__(self):
        # class variables
        self.DB = My_Data_Base()
        self.server_socket = socket()
        self.num_of_players = 2
        self.players = []
        self.deck = create_deck()
        self.card_pile = []
        self.player_index = 0
        self.plus_two = 0

    def create_socket(self):
        # function create socket, connects with clients
        self.server_socket = socket()
        self.server_socket.bind(('0.0.0.0', 8007))
        self.server_socket.listen(4)
        print ("the server is connected")

    def accept_players(self, num_of_players):
        # function accepts players according to num of players
        self.num_of_players = num_of_players
        while len(self.players) < self.num_of_players:
            (client_socket, client_address) = self.server_socket.accept()
            player = json.loads(client_socket.recv(1024).decode())
            print (player)
            player['socket'] = client_socket
            succeed = False
            msg =''
            while not succeed:
                connected_already = False
                for connect_player in self.players:
                        if connect_player['user_name'] == player['user_name']:
                            print("player is conncted already")
                            connected_already = True
                            player['socket'].send(json.dumps({'login':'failed'}).encode())
                if not connected_already:
                    if 'register' in player.keys() and player['register'] == 'now':
                        if self.DB.new_user(player['user_name'], player['password'], player['email']):
                            msg = {'register' : 'success'}
                            break
                        else:
                            player['socket'].send(json.dumps({'register':'failed'}).encode())
                    elif 'login' in player.keys() and player['login'] == 'now':
                        if self.DB.check_password(player['user_name']) != '' and \
                        self.DB.check_password(player['user_name']) == player['password']:
                            msg = {'login' : 'success'}
                            break
                        else:
                            player['socket'].send(json.dumps({'login':'failed'}).encode())
                player = json.loads(client_socket.recv(1024).decode())
                player['socket'] = client_socket
                print (player)

            if 'login' in msg.keys() and msg['login'] == 'success':
                    self.DB.update_num_games(player['user_name'])

            player['socket'].send(json.dumps(msg).encode())
            player['socket'] = client_socket
            self.players.append(player)
        self.start_game()

    def start_game(self):
        # function starts game, gives starting cards to each player
        first_card = self.deck.pop()
        if first_card['type'] == 'wild': #or first_card['type'] == 'SuperTaki'
            first_card['color'] = 'red'
        self.card_pile.append(first_card)
        for player in self.players:
            hand = []
            for i in range(0, 8):
                card = self.deck.pop()
                hand.append(card)
            player['hand'] = hand
            player['turn'] = self.players[0]['user_name']
            player['socket'].send(json.dumps({'hand': player['hand'],
                                              'turn': player['turn'],
                                              'current_card': self.card_pile[len(self.card_pile) - 1]
                                              }).encode())

    def start_gamethread(self):
        # starts game thread
        game_thread = threading.Thread(target=self.run_game)
        game_thread.start()

    def run_game(self):
        # function runs game
        winner = False
        winning_player = {}
        while not winner: # game runs while no player won
            self.receive_card()
            (winner, winning_player) = self.check_winner()
            (draw_cards, self.player_index) = self.process_card()
            self.send_turndata(draw_cards)
        self.DB.update_wins(winning_player)
        self.send_winner(winning_player)

    def receive_card(self):
        # function receives card from player
        player = self.players[self.player_index]
        object_sent = json.loads(player['socket'].recv(1024).decode())
        card = object_sent['card']
        player['hand'] = object_sent['hand']
        if card['type'] != 'skip turn': # if player chose 'skip turn', skip to the next player's turn
            self.card_pile.append(card)

    def process_card(self):
        # function processes the card that was received,
        # returns index of next player and drawn cards
        current_card = self.card_pile[len(self.card_pile) - 1]
        type = current_card['type']
        color = current_card['color']
        draw_cards = []
        player_index = (self.player_index + 1) % len(self.players)
        if type == '+2': # adds to next player 2 cards
            count = 0
            while count < 2 and self.deck != []:
                draw_cards.append(self.deck.pop())
                count += 1
        elif type == 'reverse': # reverses the order of players
            self.players = self.players[::-1]
        elif type == 'skip': # skips next player's turn
            player_index = (self.player_index + 2) % len(self.players)

        player = self.players[player_index]
        has_card = False
        all_cards = player['hand'] + draw_cards
        # checks if player who has to play next has a suiting card
        for card in all_cards:
            if card['type'] == type or card['color'] == color:
                has_card = True
                break
        if not has_card and self.deck != []: # if he doesn't gives him a card from pile
            draw_cards.append(self.deck.pop())

        return draw_cards, player_index

    def send_turndata(self, draw_cards):
        # function receives drawn cards and sends them to player
        player = self.players[self.player_index]
        current_card = self.card_pile[len(self.card_pile) - 1]
        player['socket'].send(json.dumps({'current_card': current_card,
                                          'win': '',
                                          'draw_cards': draw_cards}).encode())

    def check_winner(self):
        # function checks if any player won the game
        # returns the winning player and true if there is a winner, else false
        winner = False
        winning_player = {}

        # List is empty
        for player in self.players:
            if len(player['hand']) == 0:
                winner = True
                winning_player = player['user_name']

        return winner, winning_player

    def send_winner(self, winning_player):
        # function sends the winner to the players
        for player in self.players:
            player['socket'].send(json.dumps({'win': winning_player}).encode())

    def close_server(self):
        # function closes connection with clients and closes server
        for player in self.players:
            player['socket'].close()
        self.server_socket.close()