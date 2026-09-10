import random


def generate_mad_lib(adjective, noun, verb):
    """Return a nonempty story containing all three supplied words."""
    return f"Once upon a time, there was a {adjective} {noun} who loved to {verb} all day long."

def guessing_game():
    """Run an interactive number-guessing game."""
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guess = None

    print("Welcome to the guessing game! Try to guess the number between 1 and 100.")

    while guess != number_to_guess:
        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess < number_to_guess:
            print("Too low! Try again.")
        elif guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You've guessed the number {number_to_guess} in {attempts} attempts.")