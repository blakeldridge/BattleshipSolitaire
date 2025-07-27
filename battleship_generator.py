import pandas as pd
import random

def get_battleships(row_size, column_size):
	settings = pd.read_csv("settings.csv")
	boat_row = settings.loc[(settings["Width"] == column_size) & (settings["Height"] == row_size)].index
	return settings.loc[boat_row].values.tolist()[0][2:]

# returns True if coordinate is in grid
# retursn False if coordinate is out of grid
def coordinate_in_grid(grid, row, column):
	return row < len(grid) and row >= 0 and column < len(grid[0]) and column >= 0

# replaces each of the surrouding coordinates in a 3x3 grid with -1
# this shows that the cell is unables to have boats places on it
def surround_ship(grid, ship_locations):
	for coordinate in ship_locations:
		# gets coordinate top left corner of 3x3 grid
		start_i = coordinate[0] - 1
		start_j = coordinate[1] - 1
		# loops through each cell in 3x3
		for i in range(3):
			for j in range(3):
				# get coordinate of cell
				cell = [start_i + i, start_j + j]
				# check if coordinate is in grid and is not one of the boats coordinates
				if coordinate_in_grid(grid, cell[0], cell[1]) and cell not in ship_locations:
					# replace cell with -1 (invalid cell)
					grid[cell[0]][cell[1]] = -1

# function to check if cell can have a boat placed upon it
def check_valid_placement(grid, ship_size, row, column, direction):
	# check each cell that the boat will be placed on
	for i in range(ship_size):
		# if the cell is invalid (-1, 1)
		# return false
		if direction == "vertical":
			if grid[row + i][column] != 0:
				return False
		else:
			if grid[row][column + i] != 0:
				return False
	# if all is valid, return true
	return True

# funtion to place a ship on the grid
def place_ship(grid, ship_size):
	if ship_size > 1:
		horizontal_possible_locations = []
		for i in range(len(grid)):
		
			for j in range(len(grid[0]) - (ship_size - 1)):
				if check_valid_placement(grid, ship_size, i, j, "horizontal"):
					horizontal_possible_locations.append([i, j, "horizontal"])

		vertical_possible_locations = []
		for i in range(len(grid) - (ship_size - 1)):
			for j in range(len(grid[0])):
				if check_valid_placement(grid, ship_size, i, j, "vertical"):
					vertical_possible_locations.append([i, j, "vertical"])

		ship_row, ship_column, direction = random.choice([random.choice(vertical_possible_locations), random.choice(horizontal_possible_locations)])
		ship_locations = []
		for i in range(ship_size):
			if direction == "vertical":
				if i == 0:
					ship_piece = 5
				elif i == ship_size - 1:
					ship_piece = 6
				else:
					ship_piece = 2
				grid[ship_row + i][ship_column] = ship_piece
				ship_locations.append([ship_row + i, ship_column])
			else:
				if i == 0:
					ship_piece = 3
				elif i == ship_size - 1:
					ship_piece = 4
				else:
					ship_piece = 2
				grid[ship_row][ship_column + i] = ship_piece
				ship_locations.append([ship_row, ship_column + i])

		surround_ship(grid, ship_locations)
	else:
		possible_locations = []
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 0:
					possible_locations.append([i, j])

		ship_location = random.choice(possible_locations)
		grid[ship_location[0]][ship_location[1]] = 1
		surround_ship(grid, [ship_location])

def generate_clues(grid):
	row_clues = [sum(1 if row[i] >= 1 else 0 for i in range(len(grid[0]))) for row in grid]
	column_clues = [sum(1 if row[i] >= 1 else 0 for row in grid) for i in range(len(grid[0]))]

	return {"row":row_clues, "column":column_clues}

def print_grid(grid, clues):
	col_clues_string = "   "
	for clue in clues["column"]:
		col_clues_string += str(clue) + "  "
	print(col_clues_string)
	for index, row in enumerate(grid):
		print(clues["row"][index], row)

def generate_battleship_puzzle(row_size, column_size, boats):
	grid = [[0 for i in range(column_size)] for j in range(row_size)]

	grid_size = f"{row_size}x{column_size}"
	for boat_size, number_of_ships in enumerate(reversed(boats)):
		boat_size = len(boats) - boat_size
		for i in range(number_of_ships):
			place_ship(grid, boat_size)

	grid = [[0 if item <= 0 else item for item in row] for row in grid]

	clues = generate_clues(grid)

	return grid, clues

def get_string_of_puzzle(grid):
	cell_pieces = ["~", "o", "+", "<", ">", "^", "v"]
	return [[cell_pieces[cell] for cell in row] for row in grid]