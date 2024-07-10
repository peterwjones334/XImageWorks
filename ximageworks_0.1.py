import numpy as np
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFilter, ImageEnhance
import tkinter as tk
from tkinter import filedialog, Scale
from scipy.spatial import Voronoi

def pixel_prism_window(image, block_size=25):
    small_image = image.resize((block_size, block_size), Image.LANCZOS)
    small_pixels = np.array(small_image)
    original_width, original_height = image.size
    
    # Create a new image with the same size as the original
    output_image = Image.new("RGB", image.size)
    output_pixels = np.array(output_image)

    # Calculate the size of each block
    block_width = original_width // block_size
    block_height = original_height // block_size

    for i in range(block_size):
        for j in range(block_size):
            average_color = small_pixels[j, i]
            x_start = i * block_width
            y_start = j * block_height
            x_end = x_start + block_width
            y_end = y_start + block_height
            for x in range(x_start, min(x_end, original_width)):
                for y in range(y_start, min(y_end, original_height)):
                    output_pixels[y, x] = average_color
    
    return Image.fromarray(output_pixels)


def halftone_effect(image, dot_size=10):
    width, height = image.size
    output_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(output_image)
    for x in range(0, width, dot_size):
        for y in range(0, height, dot_size):
            box = image.crop((x, y, x+dot_size, y+dot_size))
            average_luminance = int(np.mean(box.convert("L")))
            radius = (average_luminance / 255) * (dot_size / 2)
            center = (x + dot_size // 2, y + dot_size // 2)
            draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=box.getpixel((dot_size//2, dot_size//2)))
    return output_image

def posterize_image(image, levels=4):
    levels = max(2, min(256, levels))
    return ImageOps.posterize(image, 8 - levels.bit_length())

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

def acrylic_overlay_effect(image, blur_radius=10, overlay_color=(255, 255, 255, 128)):
    blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    overlay = Image.new("RGBA", image.size, overlay_color)
    combined = Image.alpha_composite(blurred_image.convert("RGBA"), overlay)
    return combined.convert("RGB")

def lima_effect(image, grain_amount=50):
    grayscale_image = image.convert("L")
    np_image = np.array(grayscale_image)
    noise = np.random.normal(0, grain_amount, np_image.shape).astype(np.uint8)
    noisy_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

def movie_film_effect(image):
    # Apply a warm color tone and increase contrast
    # Convert the image to RGB if it's not already in that mode
    image = image.convert("RGB")
    
    # Apply a warm filter
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    return image

def polaroid_effect(image):
    # Apply a faded, vintage look with a slight greenish tint
    # Convert the image to RGB if it's not already in that mode
    image = image.convert("RGB")
    
    # Apply a faded filter
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 1.3)
    image = Image.merge("RGB", (r, g, b))
    
    # Decrease contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(0.8)
    
    # Apply a slight greenish tint
    green_overlay = Image.new("RGB", image.size, (0, 50, 0, 50))
    image = Image.blend(image, green_overlay, alpha=0.2)
    
    return image

def sepia_filter(image):
    width, height = image.size
    pixels = image.load()  # create the pixel map

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    return image

def cool_filter(image):
    r, g, b = image.split()
    r = r.point(lambda i: i * 0.9)
    b = b.point(lambda i: i * 1.2)
    return Image.merge("RGB", (r, g, b))

def warm_filter(image):
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    b = b.point(lambda i: i * 0.9)
    return Image.merge("RGB", (r, g, b))

def vintage_filter(image):
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    return Image.merge("RGB", (r, g, b))

def open_image():
    global input_image, output_image, input_img_label, output_img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = Image.open(file_path)
        update_output_image()

def save_image():
    global output_image
    if output_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
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
    elif effect == "Mosaic":
        return mosaic_effect(image, block_size=block_size_slider.get())
    elif effect == "Halftone":
        return halftone_effect(image, dot_size=dot_size_slider.get())
    elif effect == "Posterize":
        return posterize_image(image, levels=levels_slider.get())
    elif effect == "Voronoi":
        return voronoi_prism_effect(image, num_points=num_points_slider.get())
    elif effect == "Blur":
        return blur_image(image, radius=blur_radius_slider.get())
    elif effect == "Acrylic Overlay":
        return acrylic_overlay_effect(image, blur_radius=blur_radius_slider.get(), overlay_color=(255, 255, 255, 128))
    elif effect == "Lima":
        return lima_effect(image, grain_amount=grain_amount_slider.get())
    
def open_image():
    global input_image, output_image, input_img_label, output_img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = Image.open(file_path)
        update_output_image()

def save_image():
    global output_image
    if output_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
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
    elif effect == "Mosaic":
        return mosaic_effect(image, block_size=block_size_slider.get())
    elif effect == "Halftone":
        return halftone_effect(image, dot_size=dot_size_slider.get())
    elif effect == "Posterize":
        return posterize_image(image, levels=levels_slider.get())
    elif effect == "Voronoi":
        return voronoi_prism_effect(image, num_points=num_points_slider.get())
    elif effect == "Blur":
        return blur_image(image, radius=blur_radius_slider.get())
    elif effect == "Acrylic Overlay":
        return acrylic_overlay_effect(image, blur_radius=blur_radius_slider.get(), overlay_color=(255, 255, 255, 128))
    elif effect == "Lima":
        return lima_effect(image, grain_amount=grain_amount_slider.get())
    elif effect == "Movie Film":
        return movie_film_effect(image)
    elif effect == "Polaroid":
        return polaroid_effect(image)
    elif effect == "Sepia":
        return sepia_filter(image)
    elif effect == "Cool":
        return cool_filter(image)
    elif effect == "Warm":
        return warm_filter(image)
    elif effect == "Vintage":
        return vintage_filter(image)
    else:
        return image

def update_sliders(*args):
    effect = effect_var.get()
    block_size_slider.pack_forget()
    levels_slider.pack_forget()
    num_points_slider.pack_forget()
    blur_radius_slider.pack_forget()
    dot_size_slider.pack_forget()
    grain_amount_slider.pack_forget()
    if effect in ["Pixel Prism", "Mosaic"]:
        block_size_slider.pack(side=tk.TOP, pady=10)
    elif effect == "Posterize":
        levels_slider.pack(side=tk.TOP, pady=10)
    elif effect == "Voronoi":
        num_points_slider.pack(side=tk.TOP, pady=10)
    elif effect == "Blur" or effect == "Acrylic Overlay":
        blur_radius_slider.pack(side=tk.TOP, pady=10)
    elif effect == "Halftone":
        dot_size_slider.pack(side=tk.TOP, pady=10)
    elif effect == "Lima":
        grain_amount_slider.pack(side=tk.TOP, pady=10)
    update_output_image()

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
effect_menu = tk.OptionMenu(root, effect_var, "Pixel Prism", "Halftone", "Posterize", "Voronoi", "Blur", "Acrylic Overlay", "Lima", "Movie Film", "Polaroid", "Sepia", "Cool", "Warm", "Vintage", command=update_sliders)
effect_menu.pack(side=tk.TOP, pady=10)

# Sliders for adjustable parameters
block_size_slider = Scale(root, from_=5, to=50, orient=tk.HORIZONTAL, label="Block Size", command=update_output_image)
block_size_slider.set(25)

levels_slider = Scale(root, from_=2, to=256, orient=tk.HORIZONTAL, label="Levels (Posterize)", command=update_output_image)
levels_slider.set(4)

num_points_slider = Scale(root, from_=10, to=500, orient=tk.HORIZONTAL, label="Number of Points (Voronoi)", command=update_output_image)
num_points_slider.set(100)

blur_radius_slider = Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="Blur Radius", command=update_output_image)
blur_radius_slider.set(2)

dot_size_slider = Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, label="Dot Size (Halftone)", command=update_output_image)
dot_size_slider.set(10)

grain_amount_slider = Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Grain Amount (Lima)", command=update_output_image)
grain_amount_slider.set(50)

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


