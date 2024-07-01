""" Source header """

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
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
"\nAcross"
"\nDown"
"\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
"Invalid option/arguments. Type 'H' for help."
"Enter your guess (use _ for blanks): "
"This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")

class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):
        """
        Change the guess at the specified row and column
        clue: object representing the clue for which the user is guessing
        new_guess: New guess to be placed in the crossword
        """
        if len(new_guess) != len(clue.answer):
            raise RuntimeError("Guess length does not match the length of the clue.\n")


        new_guess_upper = new_guess.upper()

        if not all(char in GUESS_CHARS for char in new_guess_upper):
            raise RuntimeError("Guess contains invalid characters.\n")

        row, col = clue.indices
        if clue.down_across == 'A':
            for i in range(len(new_guess_upper)):
                self.board[row][col + i] = new_guess_upper[i]
        else:
            for i in range(len(new_guess_upper)):
                self.board[row + i][col] = new_guess_upper[i]

    def reveal_answer(self, clue):
        """
        Reveal the answer at the clue position
        clue: Clue object representing clue for which the answer is to be revaled
        """
        row, col = clue.indices
        if clue.down_across == 'A':
            for i in range(len(clue.answer)):
                self.board[row][col + i] = clue.answer[i]
        else:
            for i in range(len(clue.answer)):
                self.board[row + i][col] = clue.answer[i]

    def find_wrong_letter(self, clue):
        """
        Find the first wrong letter in the current guess for the given clue
        clue: Clue object representing the clue for which to find the wrong letter
        Index of the first wrong letter is returned, or -1 if the guess is rigt
        """
        row, col = clue.indices
        for i in range(len(clue.answer)):
            if clue.down_across == 'A':
                if self.board[row][col + i] != clue.answer[i]:
                    return i
            else:
                if self.board[row + i][col] != clue.answer[i]:
                    return i
        return -1

    def is_solved(self):
        """
        Check if the crossword puzzle is solved
        returns True if the puzzle is solved else False
        """
        for key, clue in self.clues.items():
            if self.find_wrong_letter(clue) != -1:
                return False
        return True
