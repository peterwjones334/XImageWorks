# image_effects.py
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance
from scipy.spatial import Voronoi

def sepia_filter(image):
    width, height = image.size
    pixels = image.load()
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

def pixel_prism_window(image, block_size=25):
    small_image = image.resize((block_size, block_size), Image.LANCZOS)
    small_pixels = np.array(small_image)
    original_width, original_height = image.size
    output_image = Image.new("RGB", image.size)
    output_pixels = np.array(output_image)
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

def mosaic_effect(image, block_size=25):
    small_image = image.resize((block_size, block_size), Image.LANCZOS)
    small_pixels = np.array(small_image)
    original_width, original_height = image.size
    output_image = Image.new("RGB", image.size)
    output_pixels = np.array(output_image)
    block_width = original_width // block_size
    block_height = original_height // block_size
    for i in range(block_size):
        for j in range(block_size):
            tile_color = small_pixels[j, i]
            x_start = i * block_width
            y_start = j * block_height
            x_end = x_start + block_width
            y_end = y_start + block_height
            for x in range(x_start, min(x_end, original_width)):
                for y in range(y_start, min(y_end, original_height)):
                    output_pixels[y, x] = tile_color
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
    image = image.convert("RGB")
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    return image

def polaroid_effect(image):
    image = image.convert("RGB")
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 1.3)
    image = Image.merge("RGB", (r, g, b))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(0.8)
    green_overlay = Image.new("RGB", image.size, (0, 50, 0))
    image = Image.blend(image, green_overlay, alpha=0.2)
    return image

# List of available effects
effects = {
    "Pixel Prism": pixel_prism_window,
    "Mosaic": mosaic_effect,
    "Halftone": halftone_effect,
    "Posterize": posterize_image,
    "Voronoi": voronoi_prism_effect,
    "Blur": blur_image,
    "Acrylic Overlay": acrylic_overlay_effect,
    "Lima": lima_effect,
    "Movie Film": movie_film_effect,
    "Polaroid": polaroid_effect,
    "Sepia": sepia_filter,
    "Cool": cool_filter,
    "Warm": warm_filter,
    "Vintage": vintage_filter,
}

def process_image(image, effect, **kwargs):
    if effect in effects:
        return effects[effect](image, **kwargs)
    else:
        return image