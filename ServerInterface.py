# Main program of server
#import
from TakiServer import TakiServer

def start_server():
    # function starts server, asks how much players will be playing, accepts players and starts the game thread.
    taki_server = TakiServer()
    taki_server.create_socket()
    num_of_players = input('Number of players(2-4) (2 players are recommended): ')
    possible = False
    while not possible:
        try:
            num_of_players = int(num_of_players)
            if num_of_players > 1 and num_of_players < 5:
                print("waiting for players..")
                break
            else:
                print("try again")
        except:
            print("try again")
        num_of_players = input('Number of players(2-4) (2 players are recommended): ')

    taki_server.accept_players(int(num_of_players))
    print(taki_server.players)
    taki_server = taki_server
    taki_server.start_gamethread()

if __name__ == '__main__':
    start_server()