import numpy as np
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFilter
import tkinter as tk
from tkinter import filedialog, Scale
from scipy.spatial import Voronoi

def pixel_prism_window(image, block_size=25):
    small_image = image.resize((block_size, block_size), Image.LANCZOS)
    output_image = Image.new("RGB", image.size)
    original_width, original_height = image.size
    block_width = original_width // block_size
    block_height = original_height // block_size
    small_pixels = np.array(small_image)
    output_pixels = np.array(image)
    
    for i in range(block_size):
        for j in range(block_size):
            average_color = small_pixels[i, j]
            for x in range(block_width):
                for y in range(block_height):
                    x_pos = i * block_width + x
                    y_pos = j * block_height + y
                    if x_pos < original_width and y_pos < original_height:
                        output_pixels[y_pos, x_pos] = average_color
    
    return Image.fromarray(output_pixels)

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

def blur_image(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))

def open_image():
    global input_image, output_image, input_img_label, output_img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = Image.open(file_path)
        update_output_image()

def save_image():
    global output_image
    if output_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if save_path:
            output_image.save(save_path)

def update_output_image(*args):
    global output_image, input_image
    if input_image:
        output_image = process_image(input_image)
        output_image_tk = ImageTk.PhotoImage(output_image)
        output_img_label.config(image=output_image_tk)
        output_img_label.image = output_image_tk

def process_image(image):
    effect = effect_var.get()
    if effect == "Pixel Prism":
        return pixel_prism_window(image, block_size=block_size_slider.get())
    elif effect == "Posterize":
        return posterize_image(image, levels=levels_slider.get())
    elif effect == "Voronoi":
        return voronoi_prism_effect(image, num_points=num_points_slider.get())
    elif effect == "Blur":
        return blur_image(image, radius=blur_radius_slider.get())
    else:
        return image

def update_sliders(*args):
    effect = effect_var.get()
    if effect == "Pixel Prism":
        block_size_slider.pack(side=tk.TOP, pady=10)
        levels_slider.pack_forget()
        num_points_slider.pack_forget()
        blur_radius_slider.pack_forget()
    elif effect == "Posterize":
        block_size_slider.pack_forget()
        levels_slider.pack(side=tk.TOP, pady=10)
        num_points_slider.pack_forget()
        blur_radius_slider.pack_forget()
    elif effect == "Voronoi":
        block_size_slider.pack_forget()
        levels_slider.pack_forget()
        num_points_slider.pack(side=tk.TOP, pady=10)
        blur_radius_slider.pack_forget()
    elif effect == "Blur":
        block_size_slider.pack_forget()
        levels_slider.pack_forget()
        num_points_slider.pack_forget()
        blur_radius_slider.pack(side=tk.TOP, pady=10)
    update_output_image()

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
effect_menu = tk.OptionMenu(root, effect_var, "Pixel Prism", "Posterize", "Voronoi", "Blur", command=update_sliders)
effect_menu.pack(side=tk.TOP, pady=10)

# Sliders for adjustable parameters
block_size_slider = Scale(root, from_=5, to=50, orient=tk.HORIZONTAL, label="Block Size (Pixel Prism)", command=update_output_image)
block_size_slider.set(25)
block_size_slider.pack(side=tk.TOP, pady=10)

levels_slider = Scale(root, from_=2, to=256, orient=tk.HORIZONTAL, label="Levels (Posterize)", command=update_output_image)
levels_slider.set(4)
levels_slider.pack(side=tk.TOP, pady=10)
levels_slider.pack_forget()

num_points_slider = Scale(root, from_=10, to=500, orient=tk.HORIZONTAL, label="Number of Points (Voronoi)", command=update_output_image)
num_points_slider.set(100)
num_points_slider.pack(side=tk.TOP, pady=10)
num_points_slider.pack_forget()

blur_radius_slider = Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="Blur Radius", command=update_output_image)
blur_radius_slider.set(2)
blur_radius_slider.pack(side=tk.TOP, pady=10)
blur_radius_slider.pack_forget()

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