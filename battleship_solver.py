import random
import copy

def is_solvable(unsolved_grid, clues, battleships):
	grid = copy.deepcopy(unsolved_grid)
	fill_original_ship_pieces(grid)
	try_count = 0
	while try_count <= len(unsolved_grid)*2 and check_empty_cells(grid):
		fill_by_columns(grid, clues["column"])
		fill_by_rows(grid, clues["row"])
		try_count += 1
	
	if try_count > len(unsolved_grid)*2:
		return False
	return True

def check_empty_cells(grid):
	for row in grid:
		if "-" in row:
			return True
	return False

def fill_by_columns(grid, col_clues):
	# loop through each column
	for index, clue in enumerate(col_clues):
		# count ship pieces
		ship_pieces = 0
		empty_cells = 0
		for row in grid:
			if row[index] != "-" and row[index] != "~":
				ship_pieces += 1
			elif row[index] == "-":
				empty_cells += 1

		# check if ship pieces == number of clues
		if clue == ship_pieces:
			# then fill in rest of water:
			for row in grid:
				if row[index] == "-":
					row[index] = "~"
		# check if number of empty == number of remaining pieces
		elif empty_cells == clue - ship_pieces:
			for row in grid:
				if row[index] == "-":
					row[index] = "+"
					if not check_boat(grid, grid.index(row), index):
						fill_surroundings(grid, grid.index(row), index)

def check_boat(grid, row, column):
	# if there is boat piece to the left or right, fill top and bottom
	if (row + 1 < len(grid) and grid[row + 1][column] != "~" or "-") or (row - 1 >= 0 and grid[row - 1][column] != "~" or "-"):
		fill_top_bottom(grid, row, column)
		return True
	# if there is a boat piece above or below, fill left and right
	elif (column + 1 < len(grid) and grid[row][column + 1] != "~" or "-") or (column - 1 >= 0 and grid[row][column - 1] != "~" or "-"):
		fill_left_right(grid, row, column)
		return True
	# if the edge of grid is left of right and water on the other side, fill left and right
	elif (column + 1 >= len(grid) and grid[row][column - 1] == "~") or (column - 1 <= 0 and grid[row][column + 1] == "~"):
		fill_left_right(grid, row, column)
		return True
	# if the edge of the grid is above or below and water on the other side, fill top and bottom
	elif (row + 1 >= len(grid) and grid[row - 1][column] == "~") or (row - 1 <= 0 and grid[row + 1][column] == "~"):
		fill_top_bottom(grid, row, column)
		return True
	else:
		return False

def fill_by_rows(grid, row_clues):
	# loop through each row clue
	for index, clue in enumerate(row_clues):
		# count ship pieces
		ship_pieces = 0
		empty_cells = 0
		for cell in grid[index]:
			if cell != "-" and cell != "~":
				ship_pieces += 1
			elif cell == "-":
				empty_cells += 1

		# check if ship pieces == number of clues
		if clue == ship_pieces:
			# then fill in rest of water:
			for column, cell in enumerate(grid[index]):
				if cell == "-":
					grid[index][column] = "~"
		# check if number of empty == number of remaining pieces
		elif empty_cells == clue - ship_pieces:
			for column, cell in enumerate(grid[index]):
				if cell == "-":
					grid[index][column] = "+"
					fill_surroundings(grid, index, column)

def fill_original_ship_pieces(grid):
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			cell = grid[i][j]
			if cell == ">" or cell == "<":
				if cell == ">":
					if coordinate_in_grid(grid, i, j + 1):
						grid[i][j + 1] = "~"
					grid[i][j - 1] = "+"
					fill_surroundings(grid, i, j - 1)
				else:
					if coordinate_in_grid(grid, i, j - 1):
						grid[i][j - 1] = "~"
					grid[i][j + 1] = "+"
					fill_surroundings(grid, i, j + 1)
				fill_top_bottom(grid, i, j)
			elif cell == "^" or cell == "v":
				if cell == "^":
					if coordinate_in_grid(grid, i - 1, j):
						grid[i - 1][j] = "~"
					grid[i + 1][j] = "+"
					fill_surroundings(grid, i + 1, j)
				else:
					if coordinate_in_grid(grid, i + 1, j):
						grid[i + 1][j] = "~"
					grid[i - 1][j] = "+"
					fill_surroundings(grid, i - 1, j)
				fill_left_right(grid, i, j)
			elif cell == "o":
				fill_left_right(grid, i, j)
				fill_top_bottom(grid, i, j)

def coordinate_in_grid(grid, row, column):
	return row < len(grid) and row >= 0 and column < len(grid[0]) and column >= 0

def fill_top_bottom(grid, row, column):
	to_fill = [[-1, -1], [-1, 0,], [-1, 1], [1, -1], [1, 0], [1, 1]]
	for c in to_fill:
		n_row = row + c[0]
		n_column = column + c[1]
		if coordinate_in_grid(grid, n_row, n_column):
			grid[n_row][n_column] = "~"

def fill_left_right(grid, row, column):
	to_fill = [[-1, -1], [0, -1], [1, -1], [-1, 1], [0, 1], [1, 1]]
	for c in to_fill:
		n_row = row + c[0]
		n_column = column + c[1]
		if coordinate_in_grid(grid, n_row, n_column):
			grid[n_row][n_column] = "~"

def fill_surroundings(grid, row, column,):
	corners = [[1, 1], [-1, -1], [1, -1], [-1, 1]]
	for c in corners:
		n_row = row + c[0]
		n_column = column + c[1]
		if coordinate_in_grid(grid, n_row, n_column):
			grid[n_row][n_column] = "~"

def print_grid(grid, clues):
	col_clues_string = "    "
	for clue in clues["column"]:
		col_clues_string += str(clue) + "    "
	print(col_clues_string)
	for index, row in enumerate(grid):
		print(clues["row"][index], row)