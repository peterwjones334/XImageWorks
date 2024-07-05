import numpy as np
from PIL import Image

def pixel_prism_window(input_image_path, output_image_path):
    # Open the image
    image = Image.open(input_image_path)
    image = image.convert("RGB")
    
    # Resize the image to 25x25 for averaging
    small_image = image.resize((25, 25), Image.ANTIALIAS)
    
    # Create a new image with the same size as the original
    output_image = Image.new("RGB", image.size)
    
    # Get the original image size
    original_width, original_height = image.size
    
    # Calculate the size of each block
    block_width = original_width // 25
    block_height = original_height // 25
    
    # Load the pixels of the small and original images
    small_pixels = np.array(small_image)
    output_pixels = np.array(image)
    
    for i in range(25):
        for j in range(25):
            # Get the average color of the current block in the small image
            average_color = small_pixels[i, j]
            
            # Fill the corresponding block in the output image with the average color
            for x in range(block_width):
                for y in range(block_height):
                    x_pos = i * block_width + x
                    y_pos = j * block_height + y
                    if x_pos < original_width and y_pos < original_height:
                        output_pixels[y_pos, x_pos] = average_color
    
    # Create an output image from the modified pixels
    output_image = Image.fromarray(output_pixels)
    
    # Save the output image
    output_image.save(output_image_path)

# Example usage:
input_image_path = 'input.jpg'
output_image_path = 'output.jpg'
pixel_prism_window(input_image_path, output_image_path)
