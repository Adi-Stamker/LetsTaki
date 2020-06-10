# Imports
from tkinter import *
import tkinter.ttk as ttk
from TakiClient import TakiClient
import threading
import tkinter.messagebox as messagebox
import tkinter.font as tkFont

class Windows:
    # class gui starting windows for players
    def __init__(self, num, taki_client,):
        # recieves number of window and 'taki_client' which is in charge of connection to client.
        # function also opens window according to the variable 'num'

        # class variables
        self.taki_client = taki_client
        #self.closed = False
        self.num = num # num of window to open
        self.connection_is_made = False # shows if there is a connection
        if num == "1":
            self.home_page() # open home window
        if num == "2":
            self.login() # open login window
        if num == "3":
            self.register() # open register window
        if num == "4":
            self.game_instructions() # open window of the instructions of the game
        if num == "5":
            global closed
            closed = True
        #del self

    def home_page(self):
        # function creates a home window
        mainscreen = Tk()
        mainscreen.geometry("350x350")  # set the configuration of GUI window
        mainscreen.title("LET'S TAKI")  # set the title of GUI window
        # create a Form label
        Label(text="Welcome to LET'S TAKI!\nCard Game", bg="MediumPurple1", width="300", height="3",
              font=("Calibri", 15)).pack()
        Label(text="").pack()

        # create login button
        main_login_button = Button(text="Login", bg="MediumPurple1", height="2", width="30", command= lambda: \
            self.open_next_window(mainscreen, "2"))
        main_login_button.pack()
        Label(text="").pack()

        # create a register button
        Button(text="Register", bg="MediumPurple1", height="2", width="30", command= lambda: \
        self.open_next_window(mainscreen, "3")).pack()
        Label(text="").pack()

        # create an instructions button
        instruction_button = Button(text="Instructions", bg="MediumPurple1", height="2", width="30", command= lambda: \
        self.open_next_window(mainscreen, "4"))
        instruction_button.pack()
        Label(text="").pack()

        # create an escape button
        Button(text='Quit', bg="light sky blue", height="2", width="30", command=quit).pack()
        mainscreen.protocol("WM_DELETE_WINDOW", lambda: self.close_x(mainscreen))
        mainscreen.mainloop() # start the GUI

    def close_x(self, mainscreen):
        # function receives window and closes it.
        # closes connection between client and server
        mainscreen.destroy()
        self.taki_client.close_connection()
        self.__init__('5', self.taki_client)

    def open_next_window(self, mainscreen, num):
        # function receives window and closes it. also, receives a number of window to open next
        mainscreen.destroy()
        object2 = Windows(num, self.taki_client)

    def game_instructions(self):
        # function creates an instruction window
        mainscreen4 = Tk()  # create a GUI window
        mainscreen4.geometry("500x500")  # set the configuration of GUI wind
        mainscreen4.title("Instruction Page")  # set the title of GUI window
        Label(text="LET'S TAKI!\nCard Game\nGame Instructions", bg="turquoise", width="300", height="3",
              font=("Calibri", 15)).pack()

        # instructions label
        Label(text="""NOTE: EMAIL MUST BE A GMAIL ACCOUNT\nThis game consists of 2 or more players,
    the purpose of the game is to get rid of all the cards in your hand.
    At the start, each player gets 8 random cards.
    The game generate a first card, if the card consist an order
    the game ignores it and you should only relate to its color and his shape.
    The order of the players in determined by the order of connection to server.
    The player can get rid of his card only if the card is:
    * identical the the card shown.
    * in the same color.
    * in the same shape/number.
    * an action card: change color.
    A player who doesn't have a fitting card must draw a card from the pile
    and can use that card.

        SPECIAL ACTION CARDS
    * skip - skips the next player's turn.
    * +2 - requires the next player to get 2 new cards from the pile.
    * reverse - reverses the direction of the play.
    * wild - lets his user determine in which color the next player needs to put card.

        Who is the winner?
    The winner is the first player who gets rid of all of his cards.\n""",
              font=("Arial", 10), bg="white", width= "500").pack()

        # create button to get back to home page
        Button(mainscreen4, text="Back", bg="snow3", width="5", command= lambda: self.go_back(mainscreen4)).pack()
        mainscreen4.protocol("WM_DELETE_WINDOW", lambda: self.close_x(mainscreen4))
        mainscreen4.mainloop()

    def login(self):
        # function creates a login window
        mainscreen2 = Tk()  # create a GUI window
        mainscreen2.geometry("250x200")  # set the configuration of GUI wind
        mainscreen2.title("Login Page")  # set the title of GUI window
        # create labels
        Label(mainscreen2, text="User Name:", width="10", height="2", font=("Calibri", 13)).grid(row=0)
        Label(mainscreen2, text="Password:", width="10", height="2", font=("Calibri", 13)).grid(row=1)
        enter_username = Entry(mainscreen2)
        enter_password = Entry(mainscreen2)
        enter_username.grid(row=0, column=170)
        enter_password.grid(row=1, column=170)
        # create buttons for login and go back (to main screen)
        login_button = Button(mainscreen2, text="Login", bg="MediumPurple1", height="1", width="15",
                   command= lambda: self.log_in_player(enter_username, enter_password, mainscreen2))
        login_button.grid(row=3, column=170)
        Label(mainscreen2, height="1", width='23').grid(row=4, column=200)
        self.lback_button = Button(mainscreen2, text="Back", bg="snow3", width="5", command= lambda:
        self.go_back(mainscreen2))
        self.lback_button.grid(row=5, column=170)
        mainscreen2.protocol("WM_DELETE_WINDOW", lambda: self.close_x(mainscreen2))
        mainscreen2.mainloop()

    def register(self):
        # function create register window
        mainscreen3 = Tk()  # create a GUI window
        mainscreen3.geometry("300x250")  # set the configuration of GUI wind
        mainscreen3.title("Register Page")  # set the title of GUI window
        # create labels
        Label(mainscreen3, text="User Name:", width="15", height="2", font=("Calibri", 13)).grid(row=0)
        Label(mainscreen3, text="Email:", width="15",height="2", font=("Calibri", 13)).grid(row=1)
        Label(mainscreen3, text="Password:",width="15",height="2", font=("Calibri", 13)).grid(row=2)
        # create entries to enter information
        enter_username = Entry(mainscreen3)
        enter_email = Entry(mainscreen3)
        enter_password = Entry(mainscreen3)
        enter_username.grid(row=0, column=170)
        enter_email.grid(row=1, column=170)
        enter_password.grid(row=2, column=170)
        # create buttons for register and go back (to main screen)
        register_button = Button(mainscreen3, text="Register", bg="MediumPurple1", width="15", command= lambda:
        self.after_register(enter_username, enter_email, enter_password, mainscreen3))
        register_button.grid(row=3, column=170)
        Label(mainscreen3, height="1", width='23').grid(row=4, column=200)
        self.rback_button = Button(mainscreen3, text="Back", bg="snow3", width="5", command= lambda:
        self.go_back(mainscreen3))
        self.rback_button.grid(row=5, column=170)
        mainscreen3.protocol("WM_DELETE_WINDOW", lambda: self.close_x(mainscreen3))
        mainscreen3.mainloop()

    def log_in_player(self, e_user, e_password, that_mainscreen):
        # function receives entries for user and password, and the current main screen.
        # connect player if info is correct else show message.
        self.lback_button.configure(state="disabled")
        dits = {'user_name': e_user.get(), 'password': e_password.get(), 'login': 'now'}
        print("User Name: %s\nPassword: %s" % (e_user.get(), e_password.get()))
        is_connected = self.connect(dits) # is info correct
        if not is_connected:
            messagebox.showinfo("Incorrect Info!", "Incorrect Info! try again")
        if is_connected:
            that_mainscreen.destroy()

    def after_register(self, e_user, e_email, e_password, that_mainscreen):
        # function receives entries for user, email and password and the current main screen.
        # connect player if info is correct else show message.
        self.rback_button.configure(state="disabled")
        dits = {'user_name': e_user.get(), 'email': e_email.get(), 'password': e_password.get(), 'register': 'now'}
        print("User Name: %s\nEmail: %s\nPassword: %s" % (e_user.get(), e_email.get(), e_password.get()))
        is_connected = self.connect(dits) # is info correct
        if not is_connected:
            messagebox.showinfo("Incorrect Info!", "Incorrect Info! try again")
        if is_connected:
            that_mainscreen.destroy()

    def go_back(self, that_mainscreen):
        # function receives existing window, destroys it and goes to main screen
        that_mainscreen.destroy()
        self.__init__('1', self.taki_client)

    def connect(self, dits):
        # function receives details, create connection with server, if possible returns true, otherwise false
        if not self.connection_is_made:
            self.taki_client.create_socket()
            self.connection_is_made = True
        is_succeed = self.taki_client.join_game(dits)
        if not is_succeed:
            return False
        self.taki_client.start_game() # starts game
        print(self.taki_client.player)
        return True

class MainApp(Tk):
    # Class of main app
    def __init__(self, taki_client):
        Tk.__init__(self)
        #self.resizable(0, 0)
        self.taki_client = taki_client
        self.wm_title("PyTaki Client")
        # Main frame and config
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("1000x300")
        # Configure button styling
        style = ttk.Style()
        #font=('Helvetica', 12)
        style.configure("red.TButton", foreground="red", font=('Helvetica', 12))
        style.configure("blue.TButton", foreground="blue", font=('Helvetica', 12))
        style.configure("green.TButton", foreground="green", font=('Helvetica', 12))
        style.configure("yellow.TButton", foreground="yellow", font=('Helvetica', 12))
        style.configure("black.TButton", foreground="black", font=('Helvetica', 12))

        # Dictionary of frames in app.
        self.frames = {}

        # Loop through the frame tuple (windows) and add it to the frames dictionary
        frame = GameWindow(parent=container, controller=self, )
        self.frames[GameWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GameWindow)

    def show_frame(self, cont):
        # function shows chosen frame
        frame = self.frames[cont]
        frame.tkraise()

class GameWindow(Frame):
    # Class of the window in which the game is displayed
    def __init__(self, parent, controller,):
        Frame.__init__(self, parent)
        # Controller references the MainApp class. We use this to access its instance variables.
        self.controller = controller
        # Array of button handles
        self.buttons = []
        # iterator to determine which column to place the button in within the grid
        self.current_col = 0
        self.chosen_wildcard = {}

        self.grid_rowconfigure(1)
        self.grid_columnconfigure(1, weight=1)

        # Create labels
        fontStyle = tkFont.Font(family="Lucida Grande", size=13)
        title_label = ttk.Label(self, text="PyTaki", font = fontStyle)
        self.turn_label = ttk.Label(self, text="turn", font = fontStyle)
        self.currentcard_label = ttk.Label(self, text='Current card', font = fontStyle)
        self.currentcard_frame = ttk.Frame(self)
        card_label = ttk.Label(self, text="Cards in your hand", font = fontStyle)

        title_label.grid(row=0, column=1)
        self.turn_label.grid(row=1, column=1)
        self.currentcard_label.grid(row=2, column=1)
        self.currentcard_frame.grid(row=3, column=1)
        card_label.grid(row=4, column=1)
        # Button array needs its own frame
        self.button_frame = ttk.Frame(self)
        self.wildcolor_frame = ttk.Frame(self)
        # create button for skipping turn
        self.skipturn_button = ttk.Button(self, text='Skip your turn', command=self.skip_turn)
        self.buttons.append(self.skipturn_button)
        self.button_frame.grid(row=5, column=1)
        self.skipturn_button.grid(row=6, column=1)

        self.show_currentcard()

        self.generate_cardbuttons()
        self.generate_wildcolorbuttons()

        self.init_turn()
        self.change_cardstate()

        if not self.controller.taki_client.your_turn:
            # if it is not the player's turn create thread for waiting
            wait_thread = threading.Thread(target=self.done_wait)
            wait_thread.start()

    def generate_cardbuttons(self):
        # Function generates the initial hand as buttons.
        # Accessing player's hand
        hand = self.controller.taki_client.player['hand']

        # Iterate through cards in hand and create a new button.
        for card in hand:
            # Initialize Button control
            card_button = ttk.Button(self.button_frame, text=card['type'], style="%s.TButton" % card['color'], width=10,
                                    command=lambda current_card=card: self.button_action(current_card))
            # Append button control to array
            self.buttons.append(card_button)
            # Add button to grid dynamically
            card_button.grid(row=0, column=self.current_col, sticky='ew')
            # Increment for next button
            self.current_col += 1

    def button_action(self, card):
    # Function determines which action to send to the server depending on which button is clicked.
        taki_client = self.controller.taki_client

        if card['type'] == 'wild':
            self.chosen_wildcard = card
            self.wildcolor_frame.grid(row=7, column=1)

        else:
            if card['type'] == taki_client.current_card['type'] or card['color'] == taki_client.current_card['color']:
                taki_client.send_card(card)
                button = self.get_button(card)
                button.destroy()
                self.buttons.remove(button)

                self.next_turn()
            else:
                messagebox.showinfo("Incorrect match", "Incorrect card match! Please match by card type or color. "
                                    + "If you can't, skip your turn")

    def skip_turn(self):
        # Function skips the player's turn
        taki_client = self.controller.taki_client
        skipturn_card = {'type': 'skip turn'}
        taki_client.player['hand'].append(skipturn_card)
        taki_client.send_card(skipturn_card)

        self.next_turn()

    def next_turn(self):
        # Function wait till the player's turn if no one won yet and plays his turn.
        # If someone won shows a message.
        taki_client = self.controller.taki_client
        self.turn_label['text'] = 'Wait for your turn'
        taki_client.your_turn = False
        self.change_cardstate()

        self.update()

        taki_client.wait_turndata()
        if not taki_client.win:
            self.show_currentcard()
            self.add_draw()
            self.turn_label['text'] = 'Your turn'
            taki_client.your_turn = True
            self.change_cardstate()
        else:
            messagebox.showinfo("Game ended", "%s wins!" % taki_client.win)
            self.quit()

    def get_button(self, card):
        # Function receives card and returns it's button
        for button in self.buttons:
            if button['text'] == card['type'] and button['style'].startswith(card['color']):
                return button

    def show_currentcard(self):
        # Function shows current card on top of pile
        current_card = self.controller.taki_client.current_card
        card_button = ttk.Button(self.currentcard_frame, text=current_card['type'],
                                 style="%s.TButton" % current_card['color'], width=10)
        card_button.grid(row=0, column=0, sticky='ew')

    def add_draw(self):
        # Function add card buttons to the current player's hand
        taki_client = self.controller.taki_client
        cards = taki_client.cards_drawn
        for card in cards:
            card_button = ttk.Button(self.button_frame, text=card['type'], style="%s.TButton" % card['color'], width=10,
                                     command=lambda current_card=card: self.button_action(current_card))
            # Append button control to array
            self.buttons.append(card_button)
            # Add button to grid dynamically
            card_button.grid(row=0, column=self.current_col, sticky='ew')
            # Increment for next button
            self.current_col += 1

    def init_turn(self):
        # Function changes label to let the player know when it's his his turn
        taki_client = self.controller.taki_client
        player = taki_client.player
        turn = taki_client.turn
        if player['user_name'] == turn:
            self.turn_label['text'] = 'Your turn'
            taki_client.your_turn = True
        else:
            self.turn_label['text'] = 'Wait for your turn'

    def change_cardstate(self):
        # Function changes the state of the cards (normal/disables)
        state = 'normal' if self.controller.taki_client.your_turn else 'disabled'
        for button in self.buttons:
            button['state'] = state

    def done_wait(self):
        # Function is in charge of actions when the player's turn arrives
        self.controller.taki_client.wait_turndata()
        self.turn_label['text'] = 'Your turn'
        self.controller.taki_client.your_turn = True
        self.change_cardstate()
        self.show_currentcard()
        self.add_draw()

    def generate_wildcolorbuttons(self):
        # Function generates wild color button
        color_label = ttk.Label(self.wildcolor_frame, text='Choose wild card color:')
        color_label.grid(row=0, column=0)
        colors = ['yellow', 'green', 'red', 'blue']
        current_col = 1
        for color in colors:
            color_button = ttk.Button(self.wildcolor_frame, text=color, style="%s.TButton" % color, width=10,
                                      command=lambda wild_color=color: self.determine_wildcolor(wild_color))
            # Add button to grid dynamically
            color_button.grid(row=0, column=current_col)
            # Increment for next button
            current_col += 1
        print(self.wildcolor_frame)

    def determine_wildcolor(self, color):
        # Function determines wild color
        taki_client = self.controller.taki_client
        taki_client.change_cardcolor(self.chosen_wildcard, color)
        self.change_wildcard_buttoncolor(self.chosen_wildcard)
        self.wildcolor_frame.grid_remove()

        taki_client.send_card(self.chosen_wildcard)
        button = self.get_button(self.chosen_wildcard)
        button.destroy()
        self.buttons.remove(button)
        self.next_turn()

    def change_wildcard_buttoncolor(self, wild_card):
        # function changes color of wild color button
        for button in self.buttons:
            if button['text'] == wild_card['type']:
                button['style'] = '%s.TButton' % wild_card['color']

if __name__ == '__main__':
    closed = False
    taki_client = TakiClient()
    obj01 = Windows('1', taki_client)
    if not closed:
        client_app = MainApp(taki_client)
        client_app.mainloop()