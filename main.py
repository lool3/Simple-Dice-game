import random, sqlite3, getpass, bcrypt, mmap

def Login():
    global loggedin

    try:  #Checks if database already exists
        login = sqlite3.connect('login.db')
        c = login.cursor()
        c.execute("""CREATE TABLE users ( 
                      username text,
                      password text,
                      wins integer
                      )""")  #Creates login.db database
        login.commit(); print("New database created.")
        login.close()
        Login()

    except:
        login = sqlite3.connect('login.db'); print("Connected to database.")
        c = login.cursor()

        usern = str(
            input(
                "Please enter the username of an existing account or type 'signup' to create a new account: "
            ))

        if usern == 'signup':
            usern = str(
                input("Please enter the username for your new account: "))
            statement = c.execute("SELECT username FROM users")

            for row in statement:
                if usern in row:
                    login.close()
                    print("Username:", usern, "is already taken.")
                    return

            while True:
                passw = getpass.getpass(
                    "Enter password (Input will be hidden for your security, must contain numbers and must be at least 6 characters long.): "
                )
                if len(passw) <= 6:
                    print(
                        "Password is too short and is therefore insecure, please choose a new, longer password. (We reccomend above 8 characters)"
                    )

                passhasnum = False
                for character in passw:
                    if character.isdigit():
                        passhasnum = True
                
                if not passhasnum:
                    print("Password needs a number in it")

                else:
                    with open('commonpsw.txt', 'rb', 0) as file, \
                        mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                        if s.find(
                                str.encode(passw)
                        ) != -1:  #Checks for password in a list of common passwords
                            print(
                                "Password is commonly used and is therefore insecure, please choose a new password"
                            )
                        else:
                            break

            passwcheck = str(
                getpass.getpass("Confirm password for {}: ".format(usern)))
            if passw != passwcheck:
                print("Passwords do not match.")
                login.close()
                return
            else:
                del passwcheck

            pwhash = bcrypt.hashpw(passw.encode('utf-8'),
                                   bcrypt.gensalt())  #Hash password

            c.execute("INSERT INTO users VALUES (?, ?, 0)", (
                usern,
                pwhash.decode('utf-8'),
            ))  #Inserts login info into database and sets wins to 0
            login.commit()
            login.close()

        else:
            passw = str(
                getpass.getpass(
                    "Enter password for {} (Input will be hidden for your security): "
                    .format(usern)))

            try:
                login = sqlite3.connect('login.db')
                c = login.cursor()
                statement = c.execute("SELECT username FROM users")

                user_found = False
                for row in statement:
                    if usern in row:
                        user_found = True
                        c.execute(
                            "SELECT password FROM users WHERE username = ?",
                            (usern, ))
                        psw_check = c.fetchone()[0]
                        login.close()

                        if bcrypt.checkpw(
                                passw.encode('utf-8'),
                                psw_check.encode('utf-8')
                        ):  #Check password against hashed pass in database
                            print("Logged in")
                            del passw
                            loggedin = True
                            return

                        else:
                            print("Login failed. Password incorrect.")
                if user_found == False:
                    login.close()
                    print("Login failed. User does not exist."
                          )  #User not found in database

            except:
                login.close()


#>----------


def Game():
    global dice1, dice2
    player1score = 0  #Player 1's score.
    player2score = 0  #Player 2's score.
    rounds_left = 10  #Round's left in game.

    player = True  # player True = Player 1, player False = Player 2
    for i in range(rounds_left):
        if player == True:
            playernum = 1
        else:
            playernum = 2

        print("Player", playernum, ", press enter to roll the dice")
        input()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)  #Roll Dice

        if ((dice1 + dice2) % 2) == 0:  #Checks if number is even.
            if playernum == 1:
                player1score += 10  #Adds 10 points to player 1's score.
            else:
                player2score += 10  #Adds 10 points to player 2's score.

        else:  #Else if number is odd.
            if playernum == 1:
                if player1score >= 5:  #Ensures that score doesn't fall below 0.
                    player1score -= 5  #Sutracts 5 points from player 1's score.
            else:
                if player2score >= 5:  #Ensures that score doesn't fall below 0.
                    player2score -= 5  #Sutracts 5 points from player 2's score.

        print("Player", playernum, ", you rolled a", dice1, "and a", dice2,
              ". In total you rolled a", dice1 + dice2)
        if playernum == 1:
            print("Player", playernum, "score:", player1score)
        else:
            print("Player", playernum, "score:", player2score)

        player = not player  #Reverses boolean statement so that the next player can go
    if player1score > player2score:
        print("Player 1 wins!")
    elif player1score < player2score:
        print("Player 2 wins!")
    else:
        print("Draw! Keep playing to see who wins.")
        Game()


#>----------

#Start

loggedin = False
while not loggedin:
    Login()

while True:
    Game()
    input("Press enter to play again")
