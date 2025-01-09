#Imports
import os
import random as rm
import time as tm

#Constants
"""these two tuples contain the groups of values ​​from which the values ​​that will be remembered during the game will be selected"""
LETTERS :tuple[str, str, str] = ("abcd", "abcdefg", "abcdefghijklmno")
NUMBERS :tuple[str, str, str] = ("1234", "0123456", "0123456789")

"""This ones are the variables that will be used during the program"""
points, playtime, sequence, new_record, start = 0, 0, "", 0, tm.perf_counter()

"""With this lines we import the record stored in the .txt file"""
file = open("save_record.txt", "r")
current_record = int(file.read())
file.close()
del file

#Functions
"""This two lambdas are only because of personal preference"""
clear = lambda: os.system('cls')
sleep_ = lambda i: tm.sleep(i)

"""This function handles the updating of the .txt file"""
def file_handling(num :int) -> None:
    file_1 = open("save_record.txt", "w")
    file_1.write(str(num))
    file_1.close()
    del file_1
    return None

"""This function contains the initial animation"""
def opening_screen() -> None:
    clear()
    print("################################################################################################")
    print("███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗     ██████╗  █████╗ ███╗   ███╗███████╗")
    sleep_(0.25)
    print("████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝")
    sleep_(0.25)
    print("██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝ ╚████╔╝     ██║  ███╗███████║██╔████╔██║█████╗  ")
    sleep_(0.25)
    print("██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗  ╚██╔╝      ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ")
    sleep_(0.25)
    print("██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║       ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗")
    sleep_(0.25)
    print("╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝")
    print("################################################################################################")
    sleep_(0.5)
    return None

"""The next two functions specify the gamemode during the programme"""
def letters_mode(difficulty :str) -> None:
    actual_game(difficulty=int(difficulty), game_mode="letters")
    return None

def numbers_mode(difficulty :str) -> None:
    actual_game(difficulty=int(difficulty), game_mode="numbers")
    return None

"""in this function the actual game is executed"""
def actual_game(difficulty :int, game_mode :str) -> None:
    """Now we can use the functions created at the start of the script"""
    global sequence
    global new_record
    global points
    global clear
    global sleep_

    """main loop"""
    while True:
        clear()

        """With this if we handle the different gamemodes and difficultys selected """
        if game_mode == "numbers":
            sequence += rm.choice(NUMBERS[difficulty-1])
        else:
            sequence += rm.choice(LETTERS[difficulty-1])

        """With this we print the characters"""
        for item in sequence:
            print(f"Current: {item}")
            sleep_(1)
            clear()
            sleep_(0.2)

        """We check if the answer is correct"""
        if input("Write the sequence you have seen, if you get it wrong or type everything except the correct sequence you will lose and exit!: ").lower().strip() != sequence:
            clear()

            """calculation of game time"""
            end = tm.perf_counter()
            game_time = end - start
            
            print(f"Game Over, your score is: {points}")
            print(f"you played for {game_time} second")
            if points > current_record:
                print(f"Your record has been increased to your new score: {points}")
                file_handling(points)
            else:
                print(f"Your score of {points} points is lower than or equal to your record of {current_record} points, so the record hasn't been changed!")
            break
        print("Correct answer")
        points += 1
        continue
    return None

"""the main function contains the calls of all the other functions"""
def main() -> None:
    opening_screen()
    while True:
        game_mode :str = input("\nSelect game mode (letters, numbers or q to quit!): ").lower().strip()
        if game_mode == "q":
            return None
        elif game_mode == "letters":
            while True:
                choice = input("\nEnter 1 for easy, 2 for medium or 3 for high difficulty!: ").strip()
                if not(choice != "1" and choice != "2" and choice != "3"):
                    letters_mode(difficulty=choice)
                    return None
                print("Invalid value, try again")
                continue
        elif game_mode == "numbers":
            while True:
                choice = input("\nEnter 1 for easy, 2 for medium or 3 for high difficulty!: ").strip()
                if not (choice != "1" and choice != "2" and choice != "3"):
                    numbers_mode(difficulty=choice)
                    return None
                print("Invalid value, try again")
                continue
        print("Invalid value, try again")
        continue

#Start of the program
"""HELLO!"""
if __name__ == "__main__":
    main()
