#Imports
import os
import random as rm
import time as tm

#Constants
LETTERS :tuple[str, str, str] = ("abcd", "abcdefg", "abcdefghijklmno")
NUMBERS :tuple[str, str, str] = ("1234", "0123456", "0123456789")

points, playtime, sequence, new_record, start = 0, 0, "", 0, tm.perf_counter()

file = open("save_record.txt", "r")
current_record = int(file.read())
file.close()
del file

#Functions
clear = lambda: os.system('cls')
sleep_ = lambda i: tm.sleep(i)

def file_handling(num :int) -> None:
    file_1 = open("save_record.txt", "w")
    file_1.write(str(num))
    file_1.close()
    del file_1
    return None

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

def letters_mode(difficulty :str) -> None:
    actual_game(difficulty=int(difficulty), game_mode="letters")
    return None

def numbers_mode(difficulty :str) -> None:
    actual_game(difficulty=int(difficulty), game_mode="numbers")
    return None

def actual_game(difficulty :int, game_mode :str) -> None:
    global sequence
    global new_record
    global points
    global clear
    global sleep_
    while True:
        clear()
        if game_mode == "numbers":
            sequence += rm.choice(NUMBERS[difficulty-1])
        else:
            sequence += rm.choice(LETTERS[difficulty-1])

        for item in sequence:
            print(f"Current: {item}")
            sleep_(1)
            clear()
            sleep_(0.2)

        if input("Write the sequence you have seen, if you get it wrong or type everything except the correct sequence you will lose and exit!: ").lower().strip() != sequence:
            clear()
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
if __name__ == "__main__":
    main()
