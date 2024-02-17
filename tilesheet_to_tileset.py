from PIL import Image

def split_tilesheet(tilesheet_path, tile_width, tile_height, output_path):
    tilesheet = Image.open(tilesheet_path)

    tile_count_x = tilesheet.width // tile_width
    tile_count_y = tilesheet.height // tile_height

    for y in range(tile_count_y):
        for x in range(tile_count_x):
            left = x * tile_width
            top = y * tile_height
            right = left + tile_width
            bottom = top + tile_height

            tile = tilesheet.crop((left, top, right, bottom))
            tile.save(f"{output_path}/tile_{x}_{y}.png")

# Example usage
tilesheet_path = "./Mario-AI-Framework-master/img/mapsheet.png"
tile_width = 16  # Adjust according to your tilesheet
tile_height = 16  # Adjust according to your tilesheet
output_path = "./tileset"

split_tilesheet(tilesheet_path, tile_width, tile_height, output_path)
