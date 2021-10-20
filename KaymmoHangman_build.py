import random
import pickle
import pandas as pd


def get_solution():
    with open('solutions.pickle', 'rb') as handle:
        solutions = pickle.load(handle)
    solution = (solutions[random.randint(0, len(solutions))]).lower()
    return solution

def get_leaderboard():
    with open('leaderboard.pickle', 'rb') as handle:
        leaderboard = pickle.load(handle)
    return leaderboard


def gameplay(player_name):
    remaining_guesses = 6
    score = 0
    solved = False
    previous_guesses = []
    leaderboard = get_leaderboard()

    solution = get_solution()
    progress_display = '-' * len(solution)
    if ' ' in solution:
        idx = solution.find(' ')
        while idx != -1:
            progress_display = progress_display[0:idx] + ' ' + progress_display[idx + 1:]
            idx = solution.find(' ', idx + 1)

    input("Ready, hit 'Enter' to begin...")

    while not solved and remaining_guesses > 0:
        print(progress_display)
        guess = (input("Please guess a letter: ").lower())[:1]
        if guess in previous_guesses:
            print("You have already guessed this letter!")

        elif guess.isalpha():
            if guess in solution:
                print(f"Well done, '{guess}' is a correct letter!")
                previous_guesses.append(guess)
                progress_as_list = list(progress_display)
                indices = [i for i, letter in enumerate(solution) if letter == guess]
                for index in indices:
                    progress_as_list[index] = guess
                progress_display = "".join(progress_as_list)
                if "-" not in progress_display:
                    solved = True
                    score += 10
            else:
                print(f"Unlucky, '{guess}' was incorrect")
                remaining_guesses -= 1
                previous_guesses.append(guess)

        else:
            print("That is not a letter!")
            remaining_guesses -= 1
        print(f"You have {remaining_guesses} remaining guess(es)")

    if player_name in leaderboard:
        leaderboard[player_name] += score
    else:
        leaderboard[player_name] = score

    df = pd.DataFrame(list(leaderboard.items()), columns=['Player', 'Score'])
    df = df.sort_values(by='Score', ascending=False)
    df.insert(0, 'Ranking', range(1, 1 + len(df)))
    df = df.set_index('Ranking').head(10)

    with open('leaderboard.pickle', 'wb') as handle:
        pickle.dump(leaderboard, handle)

    if solved:
        print(f"Well done {player_name}, the puzzle has been solved! The word(s) were '{progress_display}'")
    else:
        print(f"Oh dear {player_name}, you have been hung! :( \nBetter luck next time!")

    print(f"Have a look at the Leaderboard:\n {df}"
          "\n\n Thanks for playing!")
    replay = input(f"Type 'y' to play again or any other key to exit: ").lower()
    if replay == 'y':
        gameplay(player_name)
    else:
        return


def main():
    leaderboard = get_leaderboard()

    print("This is Kaymmo classic Hangman!")
    player_name = input("Please enter your name: ").lower()

    if player_name in leaderboard:
        print(f'Welcome back {player_name}! Your current score is {leaderboard[player_name]}')
    else:
        print(f"Hello {player_name} the rules are as follows; you must work out the secret word(s) by\n"
              f"correctly guessing the letters it contains.\n"
              f"Six incorrect guesses means you will be hung.")

    gameplay(player_name)
