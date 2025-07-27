from PIL import Image, ImageDraw, ImageFont

#3 output pngs of solved and unsolved grid
# take solved and unsolved grid and generate png with the information
def create_image_from_puzzle(puzzle, battleships, clues, file_name, pixel_width):
	# Assuming the puzzle is a 2D array with clues
	height = len(puzzle)
	width = len(puzzle[0])

	# Set cell size and image size based on your preference
	cell_size = 60
	image_width = width * cell_size + 60
	image_height = height * cell_size + 130

	# Create a blank white image
	img = Image.new("RGB", (image_width, image_height), "white")
	draw = ImageDraw.Draw(img)

	# Draw title at the top
	title_font = ImageFont.truetype("arial.ttf", 40)
	draw.text(((image_width-300) //2, 5), "Battleship Puzzle", fill="black", font=title_font)

	# Draw ship size report
	ship_report = "Hidden Ships: "
	for index, ship in enumerate(battleships):
		if ship != 0:
			ship_report += f"  Size {index + 1}: {ship}"

	ship_report_font = ImageFont.truetype("arial.ttf", 20)
	draw.text((15, 58), ship_report, fill="black", font=ship_report_font)

	clue_font = ImageFont.truetype("arial.ttf", 30)

	title_offset = 80
	for row in range(height):
		for col in range(width):
			# Draw filled cells based on the puzzle content
			cell_value = puzzle[row][col]
			if cell_value != "-":  # Assuming 1 represents a ship piece
				draw_ship_piece(draw, cell_value,col * cell_size, row * cell_size + title_offset, cell_size)
			# Draw grid lines
			draw.rectangle(
				[
					col * cell_size,
					row * cell_size + title_offset,
					(col + 1) * cell_size,
					(row + 1) * cell_size + title_offset,
				],
				outline="gray",
			)

	   # Print statements to check if the loop is reaching the drawing part
		draw.text((image_width - 35, title_offset + row * cell_size + cell_size//4), str(clues["row"][row]), fill="black", font=clue_font)

	# Draw column clues
	for col in range(width):
		draw.text((col * cell_size + cell_size//3, image_height - 35), str(clues["column"][col]), fill="black", font=clue_font)

	# resize image to desired size
	img = img.resize((pixel_width, int(pixel_width * image_height/image_width)))

	# Save the image
	img.save(file_name)

def draw_ship_piece(draw, piece_type, x, y, size):
	draw.rectangle([x, y, x + size, y + size], fill="#dddddd")
	if piece_type == "o":
		draw.ellipse([x, y, x + size, y + size], fill="black")
	elif piece_type == "+":
		draw.rectangle([x, y, x + size, y + size], fill="black")
	elif piece_type == "<":
		draw.ellipse([x, y, x + size, y + size], fill="black")
		draw.rectangle([x + size // 3, y, x + size * 5/3, y + size], fill="black")
		#draw.pieslice([x + size // 3, y, x + size * 5/3, y + size], start=90, end=270, fill="black")
	elif piece_type == ">":
		draw.ellipse([x, y, x + size, y + size], fill="black")
		draw.rectangle([x - size * 2/3, y, x + 2*size//3, y + size], fill="black")
		#draw.pieslice([x - size * 2/3, y, x + 2*size//3, y + size], start=270, end=90, fill="black")
	elif piece_type == "^":
		draw.ellipse([x, y, x + size, y + size], fill="black")
		draw.rectangle([x, y + size//3, x + size, y + size * 5/3], fill="black")
		#draw.pieslice([x, y + size//3, x + size, y + size * 5/3], start=180, end=360, fill="black")
	elif piece_type == "v":
		draw.ellipse([x, y, x + size, y + size], fill="black")
		draw.rectangle([x, y - 2*size//3, x + size, y + 2*size//3], fill="black")
		#draw.pieslice([x, y - 2*size//3, x + size, y + 2*size//3], start=0, end=180, fill="black")