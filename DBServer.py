# Data Base for server
# import
import sqlite3

class My_Data_Base:
   # Class create data base table and performs actions on it.
   def __init__(self, file_name='Players.db', table_name='Users'):
       # class variables
       self.__file_name = file_name
       self.__table_name = table_name
       self.make_new_table()

   def connect(self):
       # connect to table
       self.__conn = sqlite3.connect(self.__file_name)
       self.__c = self.__conn.cursor()

   def close(self):
       # close the table
       self.__conn.commit()
       self.__conn.close()

   def make_new_table(self):
       # creates a table
       self.connect()
       str = "CREATE TABLE IF NOT EXISTS" + " " + self.__table_name + \
            """( User_Name TEXT PRIMARY KEY NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            Win INTEGER,
            Num_of_games INTEGER)"""

       self.__c.execute(str)
       self.close()

   def new_user(self, user_name, password, email):
       # Receives user's details and saves his information
       # Returns true if is added ti data base else false
       self.connect()
       added = False
       if self.is_valid_input(email):
           str = "INSERT INTO " + self.__table_name + " (User_Name, Email, Password, Win, Num_of_games) VALUES ('"\
                 + user_name + "','" + email + "','" + password + "', 0, 1);"
           try:
               self.__c.execute(str)
               print('The user name is added to the data base')
               added = True
           except sqlite3.IntegrityError:
               print('The user name is taken')
           except:
               print('There is a problem')
       self.close()
       return added

   def is_valid_input(self, email):
       # Receives the user's email and Checks if the email is valid,
       # returns true if is valid else false
        if email.find('@gmail.com') != -1:
                return True
        else:
            print('email is wrong')
        return False

   def check_password(self, user_name):
       # Receives the user name and returns the user's password if user exists in the data base
       self.connect()
       password = ''
       try:
           print('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
           self.__c.execute('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
           password = self.__c.fetchone()[2]  # password
           print(password)
       except:
           print('data is incorrect, probably the user name is incorrect')
       self.close()
       return password

   def update_num_games(self, user_name):
       # Receives the user name and updates the user's number of games
       self.connect()
       try:
           print('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
           self.__c.execute('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
           player_info = self.__c.fetchone()
           num_of_games = player_info[4]
           num_of_games += 1
           print(num_of_games)
           self.__c.execute('UPDATE Users SET "Num_of_games" = ? WHERE "User_Name" = ?', (num_of_games, user_name,))
       except:
           print('data is incorrect')
       self.close()

   def update_wins(self, user_name):
        # Receives the user name and updates the user's number of wins
       self.connect()
       try:
           print('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
           self.__c.execute('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
           player_info = self.__c.fetchone()
           num_of_wins = player_info[3]
           num_of_wins += 1
           print(num_of_wins)
           self.__c.execute('UPDATE Users SET "Win" = ? WHERE "User_Name" = ?', (num_of_wins, user_name,))
       except:
           print('data is incorrect')
       self.close()