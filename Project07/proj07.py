# ###########
# This program accepts file name from user and opens
# a puzzel of crossward. The user can enjoy this game
# as it follows all the rules. First it shows the hints for across a row and a column
# with proper star and end points. It checks if the guess is right
# or wrong and depending on that it allowes user to input in the crossward
# or rejects it and repromts. We can also request for hint or reveal answers
# by inputting approptiate start and end points. We have a help menue which has all the commands,
# and user can restart or quit the game. If the user succesfuly completes the game,
# He or she getsa congratulations message.
# ###########

from crossword import Crossword
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"

A = "\nAcross"
D = "\nDown"
WIN = "\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
INVALID = "Invalid option/arguments. Type 'H' for help."
GUESS = "Enter your guess (use _ for blanks): "
COR = "This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")

# def input( prompt=None ):
#     """
#         DO NOT MODIFY: Uncomment this function when submitting to Codio
#         or when using the run_file.py to test your code.
#         This function is needed for testing in Codio to echo the input to the output
#         Function to get user input from the standard input (stdin) with an optional prompt.
#         Args:
#             prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
#         Returns:
#             str: The user input received from stdin.
#     """
#
#     if prompt:
#         print( prompt, end="" )
#     aaa_str = sys.stdin.readline()
#     aaa_str = aaa_str.rstrip( "\n" )
#     print( aaa_str )
#     return aaa_str


def open_puzzle_file():
    '''Function to open file that user wants to open
    Returns the puzzle'''
    while True:
        filename = input(PUZZLE_PROMPT)
        try:
            puzzle = Crossword(filename)
            return puzzle
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)


def display_clues(puzzle, num_clues=0):
    '''Function to display clues depending on across a row or down a column'''
    across_clues = []
    down_clues = []

    for clue in puzzle.clues.values():
        if clue.down_across == 'A':
            across_clues.append(clue)
        elif clue.down_across == 'D':
            down_clues.append(clue)

    if across_clues:
        print(A)
        count = 0
        for clue in across_clues:
            print(clue)
            count = count + 1
            if num_clues and count == num_clues:
                break
    if down_clues:
        print(D)
        count = 0
        for clue in down_clues:
            print(clue)
            count = count + 1
            if num_clues and count == num_clues:
                break


def get_and_validate_command(puzzle, command):
    '''Check if command is valid or not'''
    command = command.split()
    option = command[0].upper()

    if option == 'C':
        if len(command) != 2 or not command[1].isdigit():
            return None
        return ('C', int(command[1]))

    elif option in ['G', 'R', 'T']:
        if len(command) != 4 or not command[1].isdigit() or not command[2].isdigit() \
                or len(command[3]) != 1 or command[3].upper() not in ['A', 'D']:
            return None
        row, col = map(int, command[1:3])
        direction = command[3].upper()
        if (row, col, direction) not in puzzle.clues:
            return None
        return (option, row, col, direction)

    elif option in ['H', 'S', 'Q']:
        if len(command) != 1:
            return None
        return (option)

    else:
        return None


def main():
    puzzle = open_puzzle_file()
    display_clues(puzzle)
    print(puzzle)
    print(HELP_MENU)

    while True:
        command = input(OPTION_PROMPT).strip()
        validated_command = get_and_validate_command(puzzle, command)

        if not validated_command:
            print(INVALID)
            continue

        option = validated_command[0]
        puzzle_solved = False

        if option == 'C':
            display_clues(puzzle, validated_command[1])
        elif option == 'H':
            print(HELP_MENU)
        elif option == 'S':
            main()
            break
        elif option == 'Q':
            break
        elif option in ['G', 'R', 'T']:
            row, col, direction = validated_command[1:]
            if option == 'G':
                while True:
                    guess = input(GUESS)
                    try:
                        puzzle.change_guess(puzzle.clues[(row, col, direction)], guess)
                        print(puzzle)
                        if puzzle.is_solved():
                            print(WIN)
                            puzzle_solved = True
                        break
                    except RuntimeError as e:
                        print(e)
            elif option == 'R':
                puzzle.reveal_answer(puzzle.clues[(row, col, direction)])
                print(puzzle)
                if puzzle.is_solved():
                    print(WIN)
                    puzzle_solved = True
            elif option == 'T':
                row, col, direction = validated_command[1:]
                key = (row, col, direction)
                clue = puzzle.clues[key]
                wrong_index = puzzle.find_wrong_letter(clue)
                if wrong_index != -1:
                    print(f"Letter {wrong_index + 1} is wrong, it should be {clue.answer[wrong_index]}")
                else:
                    print(COR)

        else:
            print(INVALID)

        if puzzle_solved:
            break


if __name__ == "__main__":
    main()
