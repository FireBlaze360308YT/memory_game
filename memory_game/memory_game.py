import os
import random as rm
import time as tm
import logging
from typing import Callable
import winsound  # For Windows sound support (beeps, buzzers)
import sys

# Constants
LETTERS = ("abcd", "abcdefg", "abcdefghijklmno")
NUMBERS = ("1234", "0123456", "0123456789")
RECORD_FILE = "save_record.txt"
LEADERBOARD_FILE = "leaderboard.txt"
DIFFICULTY_CHOICES = ["1", "2", "3"]
MAX_RETRIES = 3  # Max retries for invalid inputs

# Achievements (example)
ACHIEVEMENTS = {
    "First_10": 10,  # Reach a score of 10
    "First_50": 50,  # Reach a score of 50
    "First_100": 100  # Reach a score of 100
}

# Setup logging for debugging and error tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Functions
def clear() -> None:
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def sleep_(duration: float) -> None:
    """Sleep for the given duration."""
    tm.sleep(duration)

def beep_correct() -> None:
    """Plays a short beep sound for a correct sequence."""
    winsound.Beep(1000, 300)  # Frequency: 1000Hz, Duration: 300ms

def beep_incorrect() -> None:
    """Plays a buzzer sound for an incorrect sequence."""
    winsound.Beep(500, 500)  # Frequency: 500Hz, Duration: 500ms

def read_record() -> int:
    """Read the current high score from the file, handling any errors."""
    try:
        with open(RECORD_FILE, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        logging.warning(f"No record file found, starting from 0.")
        return 0
    except ValueError as e:
        logging.error(f"Error reading record file: {e}, starting from 0.")
        return 0

def update_record(new_score: int) -> None:
    """Update the record in the file."""
    try:
        with open(RECORD_FILE, "w") as file:
            file.write(str(new_score))
    except IOError as e:
        logging.error(f"Failed to write to the record file: {e}")

def load_leaderboard() -> list:
    """Load the leaderboard from the file."""
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return [line.strip().split(',') for line in file.readlines()]
    except FileNotFoundError:
        logging.warning(f"No leaderboard file found, creating a new one.")
        return []
    except ValueError as e:
        logging.error(f"Error reading leaderboard file: {e}, creating a new one.")
        return []

def update_leaderboard(name: str, score: int) -> None:
    """Update the leaderboard with a new score."""
    leaderboard = load_leaderboard()
    leaderboard.append([name, score])
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:5]  # Keep top 5 scores
    with open(LEADERBOARD_FILE, "w") as file:
        for entry in leaderboard:
            file.write(f"{entry[0]},{entry[1]}\n")
    logging.info(f"Leaderboard updated: {leaderboard}")

def display_opening_screen() -> None:
    """Displays the opening screen animation with colors."""
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
        print(f"\033[1;32;40m{line}\033[0m")  # Green-colored text
        sleep_(0.25)
    sleep_(0.5)

def select_difficulty() -> int:
    """Prompts the user to select the game difficulty, retries on invalid input."""
    retries = 0
    while retries < MAX_RETRIES:
        choice = input("\nEnter 1 for easy, 2 for medium, or 3 for high difficulty: ").strip()
        if choice in DIFFICULTY_CHOICES:
            return int(choice)
        retries += 1
        print(f"Invalid choice, please try again. ({retries}/{MAX_RETRIES})")
    logging.warning("Max retries reached for difficulty selection.")
    raise ValueError("Max retries reached for difficulty selection.")

def get_game_mode() -> Callable:
    """Prompts the user to select a game mode and returns the corresponding function."""
    retries = 0
    while retries < MAX_RETRIES:
        mode = input("\nSelect game mode (letters, numbers, mixed, or q to quit): ").lower().strip()
        if mode == "q":
            return None
        elif mode == "letters":
            return letters_mode
        elif mode == "numbers":
            return numbers_mode
        elif mode == "mixed":
            return mixed_mode
        retries += 1
        print(f"Invalid choice, try again. ({retries}/{MAX_RETRIES})")
    logging.warning("Max retries reached for game mode selection.")
    raise ValueError("Max retries reached for game mode selection.")

def check_achievements(score: int) -> None:
    """Check if any achievements are unlocked."""
    for achievement, goal in ACHIEVEMENTS.items():
        if score >= goal:
            print(f"Achievement Unlocked: {achievement}!")

def start_game(difficulty: int, game_mode: Callable, time_limit: float = 0) -> None:
    """Starts the actual game logic."""
    points, sequence, start_time = 0, "", tm.perf_counter()

    while True:
        clear()

        # Generate the sequence based on the difficulty and game mode
        sequence += rm.choice(LETTERS[difficulty - 1] if game_mode == letters_mode else NUMBERS[difficulty - 1]) if game_mode != mixed_mode else rm.choice(LETTERS[difficulty - 1] + NUMBERS[difficulty - 1])

        # Display the sequence
        for item in sequence:
            print(f"Current: {item}")
            sleep_(1)
            clear()
            sleep_(0.2)

        # Time check (if time limit is set)
        if time_limit and tm.perf_counter() - start_time >= time_limit:
            print(f"Time's up! Your score: {points}")
            update_leaderboard(points)
            break

        # Check if the user input matches the sequence
        user_input = input("Write the sequence you have seen, or type anything else to lose: ").lower().strip()
        if user_input != sequence:
            beep_incorrect()  # Play buzzer sound on failure
            clear()
            game_time = tm.perf_counter() - start_time
            print(f"Game Over! Your score: {points}")
            print(f"You played for {game_time:.2f} seconds.")
            check_achievements(points)
            update_leaderboard("Player", points)  # Use a default name, or modify for multiplayer
            break

        points += 1
        beep_correct()  # Play correct sound
        print("Correct!")

def letters_mode(difficulty: int) -> None:
    """Handles the letters mode game."""
    start_game(difficulty, letters_mode)

def numbers_mode(difficulty: int) -> None:
    """Handles the numbers mode game."""
    start_game(difficulty, numbers_mode)

def mixed_mode(difficulty: int) -> None:
    """Handles the mixed mode game, where letters and numbers alternate."""
    start_game(difficulty, mixed_mode, time_limit=30)  # 30 seconds limit for a more extreme challenge

def main() -> None:
    """Main entry point for the game."""
    display_opening_screen()
    while True:
        try:
            game_mode = get_game_mode()
            if game_mode is None:
                print("Exiting the game. Goodbye!")
                break

            difficulty = select_difficulty()
            game_mode(difficulty)
        except (ValueError, KeyboardInterrupt) as e:
            logging.error(f"Error occurred: {e}")
            print("An error occurred. Exiting the game.")
            break

# Start the program
if __name__ == "__main__":
    main()
