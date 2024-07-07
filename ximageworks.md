# Image Works - Effects

This application applies image effects such as 'Pixel Prism', Posterize, Voronoi, and Blur to an image.

It allows users to open an image, apply the desired effect with adjustable parameters, and save the output image.

## Description of Functions

- **`pixel_prism_window(image, block_size=25)`**: Applies the Pixel Prism effect by averaging pixel blocks and resizing the image accordingly.
- **`halftone_effect(image, dot_size=10)`**: Simulates a halftone printing process by converting the image into a series of dots of varying sizes and spacing
- **`posterize_image(image, levels=4)`**: Applies the Posterize effect by reducing the number of color levels in the image.
- **`voronoi_prism_effect(image, num_points=100)`**: Applies the Voronoi Prism effect by dividing the image into Voronoi cells and filling each cell with the average color.
- **`blur_image(image, radius=2)`**: Applies a Gaussian blur to the image with the specified radius.
- **`lima_effect(image, grain_amount=50)`**: Converts the image to greyscale and applies a variable grain effect by adding noise to the image.
- **`open_image()`**: Opens an image file and updates the displayed image.
- **`save_image()`**: Saves the processed image to a file, supporting both JPEG and PNG formats.
- **`update_output_image(*args)`**: Updates the output image based on the selected effect and parameters.
- **`process_image(image)`**: Processes the image based on the selected effect.
- **`update_sliders(*args)`**: Updates the visibility of the sliders based on the selected effect.

## UI Components

- **`root`**: The main Tkinter window.
- **`input_frame`**: Frame for displaying the input image.
- **`output_frame`**: Frame for displaying the output image.
- **`input_img_label`**: Label for the input image.
- **`output_img_label`**: Label for the output image.
- **`effect_menu`**: Option menu for selecting the effect.
- **`block_size_slider`**: Slider for adjusting the block size for the Pixel Prism effect.
- **`levels_slider`**: Slider for adjusting the number of levels for the Posterize effect.
- **`num_points_slider`**: Slider for adjusting the number of points for the Voronoi effect.
- **`blur_radius_slider`**: Slider for adjusting the blur radius for the Blur effect.
- **`dot_size_slider`**: For adjusting the dot size for the "Halftone" effect.
- **`grain_amount_slider`**: For adjusting the grain amount for the "Lima" effect.
- **`open_button`**: Button

## Code

```python

import numpy as np
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFilter
import tkinter as tk
from tkinter import filedialog, Scale
from scipy.spatial import Voronoi

def pixel_prism_window(image, block_size=25):

def halftone_effect(image, dot_size=10):

def posterize_image(image, levels=4):

def voronoi_prism_effect(image, num_points=100):

def blur_image(image, radius=2):

def open_image():

def save_image():

def update_output_image(*args):

def process_image(image):

def update_sliders(*args):

# Initialize the main window
root = tk.Tk()
root.title("Image Effects")

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

# Option menu to select effect
effect_var = tk.StringVar(root)
effect_var.set("Pixel Prism")
effect_menu = tk.OptionMenu(root, effect_var, "Pixel Prism", "Halftone", "Posterize", "Voronoi", "Blur", command=update_sliders)
effect_menu.pack(side=tk.TOP, pady=10)

# Sliders for adjustable parameters

# Buttons to open and save images
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(side=tk.TOP, pady=10)

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(side=tk.TOP, pady=10)

# Initialize global variables
input_image = None
output_image = None

# Run the main loop
root.mainloop()

```
