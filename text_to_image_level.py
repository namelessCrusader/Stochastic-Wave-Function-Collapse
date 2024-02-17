from PIL import Image
import os

# Mapping between ASCII characters and image filenames
ascii_to_image = {
    "X": "floor.png",
    "-": "sky.png",
    "S" : "brick_floor_breakable.png",
    "?" : "question.png",
    "Q" : "spent_question.png",
    "E" : "mushroom_enemy.png",
    "<" : "pipe_top_left.png",
    ">" : "pipe_top_right.png",
    "[" : "pipe_left.png",
    "]" : "pipe_right.png",
    "o" : "coin.png",
    "B" : "cannon_top.png",
    "b" : "cannon_bottom.png"
}

# Load images
image_mapping = {char: Image.open("./tileset/" + filename) for char, filename in ascii_to_image.items()}

def generate_image_from_ascii(ascii_level, tile_size):
    width = len(ascii_level[0]) * tile_size
    height = len(ascii_level) * tile_size
    composite_image = Image.new('RGB', (width, height), (255, 255, 255))  # Create a blank white canvas

    for y, row in enumerate(ascii_level):
        for x, char in enumerate(row):
            if char in image_mapping:
                tile_image = image_mapping[char]
                composite_image.paste(tile_image, (x * tile_size, y * tile_size))

    return composite_image

# Example usage
for file_name in os.listdir("./Generated_Levels/"):
    with open("/home/nisargparikh/Desktop/CS 7170/Warmup/Generated_Levels/" + file_name) as level:
        ascii_level = str(level.read()).split("\n")

    tile_size = 16  # Adjust this based on your preference and image sizes
    result_image = generate_image_from_ascii(ascii_level, tile_size)
    result_image.save("./Generated_Levels_Images/"+file_name.split(".")[0]+".png")  # Save the image to a file
