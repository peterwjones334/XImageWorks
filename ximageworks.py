import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import os

def pixel_prism_window(image):
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
    
    return output_image

def open_image():
    global input_image, output_image, input_img_label, output_img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = Image.open(file_path)
        output_image = pixel_prism_window(input_image)
        
        input_image_tk = ImageTk.PhotoImage(input_image)
        output_image_tk = ImageTk.PhotoImage(output_image)
        
        input_img_label.config(image=input_image_tk)
        input_img_label.image = input_image_tk
        
        output_img_label.config(image=output_image_tk)
        output_img_label.image = output_image_tk

def save_image():
    global output_image
    if output_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if save_path:
            output_image.save(save_path)

# Initialize the main window
root = tk.Tk()
root.title("Pixel Prism Window")

# Create frames for input and output images
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=10, pady=10)

output_frame = tk.Frame(root)
output_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Labels to display images
input_img_label = tk.Label(input_frame)
input_img_label.pack()

output_img_label = tk.Label(output_frame)
output_img_label.pack()

# Buttons to open and save images
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(side=tk.TOP, pady=10)

save_button = tk.Button(root, text="Save Output Image", command=save_image)
save_button.pack(side=tk.TOP, pady=10)

# Initialize global variables
input_image = None
output_image = None

# Run the main loop
root.mainloop()