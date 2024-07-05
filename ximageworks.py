import numpy as np
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import filedialog
import os
from scipy.spatial import Voronoi

def pixel_prism_window(image):
    # (Existing pixel prism window code)
    pass

def posterize_image(image, levels=4):
    levels = max(2, min(256, levels))
    step = 256 // levels
    posterized_image = ImageOps.posterize(image, 8 - levels.bit_length())
    return posterized_image

def voronoi_prism_effect(image, num_points=100):
    width, height = image.size
    np_image = np.array(image)
    points = np.random.rand(num_points, 2) * [width, height]
    vor = Voronoi(points)
    output_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(output_image)
    
    for region in vor.regions:
        if not -1 in region and len(region) > 0:
            polygon = [vor.vertices[i] for i in region]
            polygon = [(int(x), int(y)) for x, y in polygon]
            x_coords = [p[0] for p in polygon]
            y_coords = [p[1] for p in polygon]
            centroid_x = int(sum(x_coords) / len(x_coords))
            centroid_y = int(sum(y_coords) / len(y_coords))
            if 0 <= centroid_x < width and 0 <= centroid_y < height:
                color = tuple(np_image[centroid_y, centroid_x])
                draw.polygon(polygon, fill=color)
    
    return output_image

def open_image():
    global input_image, output_image, input_img_label, output_img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = Image.open(file_path)
        output_image = process_image(input_image)
        
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

def process_image(image):
    effect = effect_var.get()
    if effect == "Pixel Prism":
        return pixel_prism_window(image)
    elif effect == "Posterize":
        return posterize_image(image, levels=4)
    elif effect == "Voronoi":
        return voronoi_prism_effect(image, num_points=100)
    else:
        return image

# Initialize the main window
root = tk.Tk()
root.title("Prism Effects")

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
effect_menu = tk.OptionMenu(root, effect_var, "Pixel Prism", "Posterize", "Voronoi")
effect_menu.pack(side=tk.TOP, pady=10)

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
