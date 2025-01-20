import os
import random as rm
import time as tm

# Constants
LETTERS = ("abcd", "abcdefg", "abcdefghijklmno")
NUMBERS = ("1234", "0123456", "0123456789")

# Variables used during the game
points, playtime, sequence, new_record, start = 0, 0, "", 0, tm.perf_counter()

# Load the current record from the file
with open("save_record.txt", "r") as file:
    current_record = int(file.read())

# Functions
clear = lambda: os.system('cls')
sleep_ = lambda i: tm.sleep(i)

# Updates the record in the file
def file_handling(num: int) -> None:
    with open("save_record.txt", "w") as file:
        file.write(str(num))

# Displays the opening screen animation
def opening_screen() -> None:
    clear()
    intro_text = [
        "################################################################################################",
        "███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗     ██████╗  █████╗ ███╗   ███╗███████╗",
        "████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝",
        "██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝ ╚████╔╝     ██║  ███╗███████║██╔████╔██║█████╗  ",
        "██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗  ╚██╔╝      ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ",
        "██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║       ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗",
        "╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝",
        "################################################################################################"
    ]
    for line in intro_text:
        print(line)
        sleep_(0.25)
    sleep_(0.5)

# Handles the game mode selection and starts the game
def select_difficulty(game_mode: str) -> None:
    while True:
        choice = input(f"\nEnter 1 for easy, 2 for medium, or 3 for high difficulty: ").strip()
        if choice in ["1", "2", "3"]:
            game_mode(difficulty=choice)
            return
        print("Invalid value, try again.")

# Starts the letters mode game
def letters_mode(difficulty: str) -> None:
    actual_game(difficulty=int(difficulty), game_mode="letters")

# Starts the numbers mode game
def numbers_mode(difficulty: str) -> None:
    actual_game(difficulty=int(difficulty), game_mode="numbers")

# The main game logic
def actual_game(difficulty: int, game_mode: str) -> None:
    global sequence, new_record, points, start

    while True:
        clear()

        # Generate the sequence based on the difficulty and game mode
        sequence += rm.choice(LETTERS[difficulty - 1] if game_mode == "letters" else NUMBERS[difficulty - 1])

        # Display the sequence
        for item in sequence:
            print(f"Current: {item}")
            sleep_(1)
            clear()
            sleep_(0.2)

        # Check if the input matches the sequence
        if input("Write the sequence you have seen, or type anything else to lose: ").lower().strip() != sequence:
            clear()
            game_time = tm.perf_counter() - start
            print(f"Game Over, your score is: {points}")
            print(f"You played for {game_time:.2f} seconds.")
            if points > current_record:
                print(f"New record! Your score: {points}")
                file_handling(points)
            else:
                print(f"Your score of {points} is not higher than the record ({current_record}).")
            break

        # If the answer is correct, increment points
        print("Correct answer")
        points += 1

# Main function where everything starts
def main() -> None:
    opening_screen()
    while True:
        game_mode = input("\nSelect game mode (letters, numbers, or q to quit): ").lower().strip()
        if game_mode == "q":
            return
        elif game_mode == "letters":
            select_difficulty(letters_mode)
        elif game_mode == "numbers":
            select_difficulty(numbers_mode)
        else:
            print("Invalid value, try again.")

# Start the program
if __name__ == "__main__":
    main()
