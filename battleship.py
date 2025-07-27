import sys
import random
from battleship_generator import *
from battleship_solver import *
from battleship_image_generator import *

#1 taking inputs from command line and separating them into grid size and boat size
# if arguements are incorrect, display a message and terminate program

def validate_arguments(args):
	if len(arguments) != 3:
		print("Incorrect number of arguments!")
		print("Required: row_size column_size image_width")
		sys.exit()
	elif not check_arguments_are_integer(arguments):
		print("Arguments should all be integers!")
		sys.exit()

def check_arguments_are_integer(args):
	for arg in args:
		try:
			int(arg)
		except:
			return False
	return True

def produce_puzzles(rows, columns, image_width):
	battleships = get_battleships(rows, columns)
	while True:
		try:
			solved_puzzle, clues = generate_battleship_puzzle(rows, columns, battleships)
			break
		except:
			pass

	solved_puzzle = get_string_of_puzzle(solved_puzzle)

	unsolved_puzzle = copy.deepcopy(solved_puzzle)

	failed = 0
	while failed < 30:
		potential_removes = []
		for i in range(rows):
			for j in range(columns):
				if unsolved_puzzle[i][j] != "-":
					potential_removes.append([i,j])

		if len(potential_removes) == 0:
			break

		random_row, random_column = random.choice(potential_removes)
		unsolved_puzzle[random_row][random_column] = "-"
		if not is_solvable(unsolved_puzzle, clues, battleships):
			failed += 1
			unsolved_puzzle[random_row][random_column] = solved_puzzle[random_row][random_column]
		else:
			failed = 0

	create_image_from_puzzle(solved_puzzle, battleships, clues, "solved_puzzle.png", image_width)
	create_image_from_puzzle(unsolved_puzzle, battleships, clues, "unsolved_puzzle.png", image_width)

if __name__ == "__main__":
	arguments = sys.argv[1:]
	validate_arguments(arguments)
	row_size, column_size, image_width = [int(arg) for arg in arguments]
	produce_puzzles(row_size, column_size, image_width)