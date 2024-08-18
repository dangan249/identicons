import hashlib
import numpy as np
from PIL import Image, ImageDraw
import time
import random
import argparse

# 25 cells...each cell need 24 bits (8 bit for each Red, Green and Blue channel)
def generate_600b_binary_string(data):
    # Generate multiple hashes
    md5_hash = hashlib.md5(data.encode('utf-8')).hexdigest()
    sha256_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    # Convert each hash to a binary string
    md5_binary = ''.join(format(int(c, 16), '04b') for c in md5_hash)
    sha256_binary = ''.join(format(int(c, 16), '04b') for c in sha256_hash)
    
    # Combine the binary strings (to get at least 600 bits)
    combined_binary = md5_binary + sha256_binary
    
    # Add more hashes to reach at least 600 bits
    while len(combined_binary) < 600:
        additional_hash = hashlib.sha256(combined_binary.encode('utf-8')).hexdigest()
        combined_binary += ''.join(format(int(c, 16), '04b') for c in additional_hash)
    
    # Return the first 600 bits
    return combined_binary[:600]

def binary_to_rgb_matrix(binary_str, white_cells=5):
    rgb_values = [
        (
            int(binary_str[i:i+8], 2),
            int(binary_str[i+8:i+16], 2),
            int(binary_str[i+16:i+24], 2)
        )
        for i in range(0, len(binary_str), 24) # Extract every 24 bit to get a color
    ]
    
    # Convert the list to a 5x5 NumPy array
    matrix = np.array(rgb_values).reshape(5, 5, 3)  # Shape as (5, 5, 3) for RGB
    matrix = reduce_colors(matrix)
    # Randomly select cells to be white
    white_indices = random.sample(range(25), white_cells)
    for index in white_indices:
        row = index // 5
        col = index % 5
        matrix[row, col] = [255, 255, 255]  # Set the cell to white
    

    matrix = choose_stylish_transformation(matrix)
    
    return matrix

def reduce_colors(rgb_array, bit_depth=2):
    factor = 2 ** (8 - bit_depth)
    # Reduce the color depth by keeping only the most significant bits
    reduced_rgb_array = (rgb_array // factor) * factor
    # Scale up to avoid the dark colors
    # Add factor//2 to increase the brightness after reduction
    reduced_rgb_array += factor // 2
    return np.clip(reduced_rgb_array, 0, 255)

# def apply_vertical_symmetry(matrix):
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i]) // 2):
#             matrix[i][len(matrix[i]) - 1 - j] = matrix[i][j]
#     return matrix

# def apply_horizontal_symmetry(matrix):
#     for i in range(len(matrix) // 2):
#         matrix[len(matrix) - 1 - i] = matrix[i]
#     return matrix

def apply_vertical_symmetry(matrix):
    cols = matrix.shape[1]
    if cols % 2 == 0:
        matrix[:, cols//2:] = np.flip(matrix[:, :cols//2], axis=1)
    else:
        matrix[:, cols//2+1:] = np.flip(matrix[:, :cols//2], axis=1)
    return matrix

def apply_horizontal_symmetry(matrix):
    rows = matrix.shape[0]
    if rows % 2 == 0:
        matrix[rows//2:, :] = np.flip(matrix[:rows//2, :], axis=0)
    else:
        matrix[rows//2+1:, :] = np.flip(matrix[:rows//2, :], axis=0)
    return matrix

def calculate_symmetry_score(matrix):
    # A simple heuristic to score how "symmetrical" the matrix is
    vertical_symmetry_score = np.sum(matrix == np.flip(matrix, axis=1))
    horizontal_symmetry_score = np.sum(matrix == np.flip(matrix, axis=0))
    return vertical_symmetry_score + horizontal_symmetry_score

def choose_stylish_transformation(matrix):
    transformations = {
        "vertical_symmetry": apply_vertical_symmetry(np.copy(matrix)),
        "horizontal_symmetry": apply_horizontal_symmetry(np.copy(matrix))
    }
    
    best_transformation = None
    best_score = -1
    
    for name, transformed_matrix in transformations.items():
        symmetry_score = calculate_symmetry_score(transformed_matrix)
        # Pick the transformation with the highest symmetry score
        if symmetry_score > best_score:
            best_score = symmetry_score
            best_transformation = transformed_matrix
    
    return best_transformation if best_transformation is not None else matrix

def generate_image(matrix, cell_size=25):
    # Create a new image with the appropriate size
    img_size = cell_size * 5  # 5x5 grid
    image = Image.new('RGB', (img_size, img_size))
    draw = ImageDraw.Draw(image)
    
    # Draw each cell with its RGB color
    for y in range(5):
        for x in range(5):
            color = tuple(matrix[y, x])  # Extract the RGB tuple
            top_left = (x * cell_size, y * cell_size)
            bottom_right = ((x + 1) * cell_size, (y + 1) * cell_size)
            draw.rectangle([top_left, bottom_right], fill=color)
    
    return image

def save_image(image, base_filename="identicon", username="user"):
    current_time = int(time.time())
    filename = f"{base_filename}_{username}_{current_time}.png"
    image.save(filename)
    print(f"Image saved as: {filename}")

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Generate identicons based on a username.")
    parser.add_argument('--username', type=str, required=True, help='Username for generating the identicon')

    args = parser.parse_args()
    username = args.username

    binary_string = generate_600b_binary_string(username)
    matrix = binary_to_rgb_matrix(binary_string, white_cells=14)
    image = generate_image(matrix)
    save_image(image, username=username)

if __name__ == "__main__":
    main()
