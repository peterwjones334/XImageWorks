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

def xpro2_filter(image, **kwargs):
    width, height = image.size
    pixels = image.load()  # create the pixel map

    # Apply golden tint (similar to sepia, but more golden)
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.3588 * r + 0.7044 * g + 0.1368 * b)
            tg = int(0.299 * r + 0.587 * g + 0.114 * b)
            tb = int(0.2392 * r + 0.4696 * g + 0.0912 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    # Apply vignette effect
    vignette = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            # Distance to the center
            dx = x - width / 2
            dy = y - height / 2
            # Distance normalized to 0..1, then inverted and scaled to 0..255
            d = np.sqrt(dx*dx + dy*dy) / (np.sqrt(width*width + height*height) / 2)
            vignette.putpixel((x, y), int((1 - d) * 255))
    image = Image.composite(image, ImageOps.colorize(vignette, (0, 0, 0), (255, 255, 255)), vignette)

    # Apply blur to vignette
    image = image.filter(ImageFilter.GaussianBlur(radius=2))

    return image

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

def acrylic_overlay_effect(image, blur_radius=10, overlay_color=(255, 255, 255, 128)):
    blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    overlay = Image.new("RGBA", image.size, overlay_color)
    combined = Image.alpha_composite(blurred_image.convert("RGBA"), overlay)
    return combined.convert("RGB")

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

def lomo_filter(image):
    # Step 1: Increase saturation to create vivid colors
    image = ImageEnhance.Color(image).enhance(1.5)
    
    # Step 2: Increase overall contrast
    image = ImageEnhance.Contrast(image).enhance(1.5)
    
    # Step 3: Apply a vignette effect
    width, height = image.size
    vignette = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            dx = x - width / 2
            dy = y - height / 2
            # Distance normalized to 0..1, then inverted and scaled to 0..255
            d = np.sqrt(dx*dx + dy*dy) / (np.sqrt(width*width + height*height) / 2)
            vignette.putpixel((x, y), int((1 - d) * 255))
    image = Image.composite(image, ImageOps.colorize(vignette, (0, 0, 0), (255, 255, 255)), vignette)
    
    # Step 4: Slightly adjust the hue to mimic Lomo camera color cast
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))
    
    return image

# Grey scale + grain
def lima_effect(image, grain_amount=50):
    grayscale_image = image.convert("L")
    np_image = np.array(grayscale_image)
    noise = np.random.normal(0, grain_amount, np_image.shape).astype(np.uint8)
    noisy_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

def raw_image(image):
    return image

def grayscale_filter(image):
    return image.convert("L")

def posterize_image(image, levels=4):
    levels = max(2, min(256, levels))
    return ImageOps.posterize(image, 8 - levels.bit_length())

def blur_image(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))
 
def invert_filter(image):
    return ImageOps.invert(image)

def brightness_filter(image, factor=1.5):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def contrast_filter(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def sharpen_filter(image):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(2.0)

def edge_filter(image):
    return image.filter(ImageFilter.FIND_EDGES)

def emboss_filter(image):
    return image.filter(ImageFilter.EMBOSS)

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

def vintage_filter_1(image):
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    return Image.merge("RGB", (r, g, b))

def vintage_filter_2(image):
    # Step 1: Reduce saturation to create a faded look
    image = ImageEnhance.Color(image).enhance(0.5)
    
    # Step 2: Adjust contrast to mimic older photo contrast
    image = ImageEnhance.Contrast(image).enhance(0.9)
    
    # Step 3: Apply a warm tint
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))
    
    # Step 4: Add a slight vignette effect
    width, height = image.size
    vignette = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            # Distance to the center
            dx = x - width / 2
            dy = y - height / 2
            # Distance normalized to 0..1, then inverted and scaled to 0..255
            d = np.sqrt(dx*dx + dy*dy) / (np.sqrt(width*width + height*height) / 2)
            vignette.putpixel((x, y), int((1 - d) * 255))
    image = Image.composite(image, ImageOps.colorize(vignette, (0, 0, 0), (255, 255, 255)), vignette)
    
    return image

def outline_drawing(image):
    # Apply edge detection filter
    edges_image = image.filter(ImageFilter.FIND_EDGES)
    # Invert the colors of the edge-detected image
    inverted_image = ImageOps.invert(edges_image)
    grayscale_image = inverted_image.convert("L")
    return grayscale_image

def adjust_rgb(image, r_factor, g_factor, b_factor):
    # Implementation for adjusting RGB values
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            r = min(int(r * r_factor), 255)
            g = min(int(g * g_factor), 255)
            b = min(int(b * b_factor), 255)
            pixels[i, j] = (r, g, b)
    return image

def add_grain(image, amount):
    # Implementation for adding grain
    width, height = image.size
    grain = np.random.normal(scale=amount*255, size=(height, width, 3))
    grain_image = Image.fromarray(np.clip(np.array(image) + grain, 0, 255).astype('uint8'))
    return grain_image

def combined_filter1(image, r_factor=1.1, g_factor=1.1, b_factor=0.9, grain_amount=0.1, blur_radius=2):
    # Adjust RGB
    image = adjust_rgb(image, r_factor, g_factor, b_factor)
    # Add grain
    image = add_grain(image, grain_amount)
    # Apply blur
    image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    return image

def Custom_filter1(image):
    # Assuming `image` is already an Image object
    filtered_image = combined_filter1(image)
    filtered_image.show()
    return filtered_image  # Return the filtered image if needed elsewhere

def combined_filter2(image, r_factor=1.0, g_factor=1.0, b_factor=1.0):
    # Adjust RGB Only
    image = adjust_rgb(image, r_factor, g_factor, b_factor)
    return image

def Custom_filter2(image):
    filtered_image = combined_filter2(image)
    filtered_image.show()
    return filtered_image  # Return the filtered image if needed elsewhere


def hdr_filter(image):
    # Step 1: Increase local contrast
    image = image.filter(ImageFilter.DETAIL)

    # Step 2: Increase overall contrast
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(1.5)

    # Step 3: Increase sharpness
    sharpness_enhancer = ImageEnhance.Sharpness(image)
    image = sharpness_enhancer.enhance(2.0)

    # Optional: Increase brightness slightly to simulate HDR brightness effect
    brightness_enhancer = ImageEnhance.Brightness(image)
    image = brightness_enhancer.enhance(1.1)

    return image


def digital_noise_filter(image, noise_level=30):
    # Convert the image to a numpy array
    np_image = np.array(image)
    
    # Generate random noise
    noise = np.random.randint(-noise_level, noise_level, np_image.shape, dtype='int16')
    
    # Add the noise to the image and clip the values to be in valid range [0, 255]
    np_image = np.clip(np_image + noise, 0, 255).astype('uint8')
    
    # Convert back to PIL Image
    noisy_image = Image.fromarray(np_image)
    
    return noisy_image

def spatial_noise_filter(image, random_noise_level=30, patterned_noise_level=20, pattern_frequency=10):
    # Convert the image to a numpy array
    np_image = np.array(image)
    
    # Generate random noise
    random_noise = np.random.randint(-random_noise_level, random_noise_level, np_image.shape, dtype='int16')
    
    # Generate patterned noise (e.g., sinusoidal pattern)
    patterned_noise = np.zeros_like(np_image, dtype='int16')
    rows, cols, _ = np_image.shape
    for row in range(rows):
        for col in range(cols):
            # Create a pattern frequency dependent noise
            patterned_noise[row, col] = int(patterned_noise_level * np.sin(2 * np.pi * (row / pattern_frequency) * np.sin(2 * np.pi * (col / pattern_frequency))))
    
    # Add the random noise and patterned noise to the image
    np_image = np.clip(np_image + random_noise + patterned_noise, 0, 255).astype('uint8')
    
    # Convert back to PIL Image
    noisy_image = Image.fromarray(np_image)
    
    return noisy_image

def luminance_noise_filter(image, noise_level=30):
    # Convert the image to grayscale (luminance channel)
    luminance = image.convert("L")
    np_luminance = np.array(luminance)
    
    # Generate random noise
    noise = np.random.randint(-noise_level, noise_level, np_luminance.shape, dtype='int16')
    
    # Add the noise to the luminance channel and clip the values to be in valid range [0, 255]
    np_luminance = np.clip(np_luminance + noise, 0, 255).astype('uint8')
    
    # Convert back to PIL Image
    noisy_luminance = Image.fromarray(np_luminance)
    
    # Merge the noisy luminance channel back with the original image's color channels
    if image.mode == 'RGB':
        # If the original image is in RGB mode
        r, g, b = image.split()
        noisy_image = Image.merge("RGB", (r, g, b)).convert("L")
        noisy_image = Image.merge("RGB", (noisy_luminance, noisy_luminance, noisy_luminance))
    else:
        # If the original image is in another mode (e.g., grayscale), just return the noisy luminance
        noisy_image = noisy_luminance
    
    return noisy_image

def fpn_filter(image, noise_level=30):
    # Convert the image to a numpy array
    np_image = np.array(image)
    
    # Generate fixed pattern noise
    rows, cols, _ = np_image.shape
    fpn_noise = np.random.randint(-noise_level, noise_level, (rows, cols, 1), dtype='int16')
    fpn_noise = np.repeat(fpn_noise, 3, axis=2)
    
    # Add the fixed pattern noise to the image and clip the values to be in valid range [0, 255]
    np_image = np.clip(np_image + fpn_noise, 0, 255).astype('uint8')
    
    # Convert back to PIL Image
    noisy_image = Image.fromarray(np_image)
    
    return noisy_image

def generate_grain_mask(img_width, img_height, grain_size, seed=None):
    """
    Generate a grain mask for adding film grain effect.
    """
    np.random.seed(seed)
    noise = np.random.normal(loc=0, scale=grain_size, size=(img_height, img_width))
    noise = np.clip(noise, -255, 255)  # Ensure the noise is within pixel value range
    noise = (noise - noise.min()) / (noise.max() - noise.min()) * 255  # Normalize noise to 0-255
    mask = Image.fromarray(noise.astype(np.uint8))
    return mask

def apply_bw_grain(image, grain_size=10, seed=None):
    """
    Apply black and white film grain to an image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    img_width, img_height = image.size
    grain_mask = generate_grain_mask(img_width, img_height, grain_size, seed)
    
    # Merge the image and grain mask
    grain_image = Image.blend(image, grain_mask, alpha=0.5)
    
    return grain_image

def apply_color_grain(image, grain_size=10, seed=None):
    """
    Apply color film grain to an image.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    img_width, img_height = image.size
    grain_mask = generate_grain_mask(img_width, img_height, grain_size, seed)
    
    # Convert the grain mask to RGB
    grain_mask = grain_mask.convert('RGB')
    
    # Blend the image with the grain mask
    grain_image = Image.blend(image, grain_mask, alpha=0.5)
    
    return grain_image

def Studio_filter(image):
    """
    Apply a high-contrast black and white filter to an image to mimic the style
    of New York studio photos.
    """
    # Convert image to black and white
    bw_image = ImageOps.grayscale(image)
    
    # Increase contrast
    contrast_enhancer = ImageEnhance.Contrast(bw_image)
    bw_image = contrast_enhancer.enhance(2.0)  # Adjust the factor to achieve the desired contrast
    
    # Reduce the dark and light range (clipping)
    bw_image = ImageOps.autocontrast(bw_image, cutoff=10)  # Adjust the cutoff to achieve the desired starkness
    
    return bw_image

def rosy_spectacle_filter(image, tint_color=(255, 182, 193), intensity=0.5):
    """
    Apply a rosy spectacle tint to an image.
    
    :param image: The original image to be filtered.
    :param tint_color: The RGB color of the tint (default is light pink).
    :param intensity: The intensity of the tint (0.0 to 1.0).
    :return: The tinted image.
    """
    # Create a solid color image with the tint color
    tint_overlay = Image.new('RGB', image.size, tint_color)
    
    # Blend the original image with the tint overlay
    tinted_image = Image.blend(image, tint_overlay, intensity)
    
    return tinted_image

# List of available effects

effects = {
    "Default": raw_image,
    "Mosaic": mosaic_effect,
    "Halftone": halftone_effect,
    "Posterize": posterize_image,
    "Voronoi": voronoi_prism_effect,
    "Acrylic Overlay": acrylic_overlay_effect,
    "Blur": blur_image,
    "Lima": lima_effect,
    "Grayscale": grayscale_filter,
    "Movie Film": movie_film_effect,
    "Polaroid": polaroid_effect,
    "Lomo": lomo_filter,
    "Sepia": sepia_filter,
    "Vintage1": vintage_filter_1,
    "Vintage2": vintage_filter_2,
    "Cool": cool_filter,
    "Warm": warm_filter,
    "Invert": invert_filter,
    "Brightness": brightness_filter,
    "Contrast": contrast_filter,
    "Sharpen": sharpen_filter,
    "Edge": edge_filter,
    "Emboss": emboss_filter,
    "Pixel Prism": pixel_prism_window,
    "Grain Blur": Custom_filter1,
    "RGB - ": Custom_filter2,
    "Line Drawing": outline_drawing,
    "xpro2": xpro2_filter,
    "HDR": hdr_filter,
    "Digital Noise": digital_noise_filter,
    "Spacial Noise": spatial_noise_filter,
    "Luminance Noise": luminance_noise_filter,
    "Fixed Pattern Noise": fpn_filter,
    "BW Grain": apply_bw_grain,
    "Color Grain": apply_color_grain,
    "Studio": Studio_filter,
    "Rosy Tint": rosy_spectacle_filter,
}    

def process_image(image, effect, **kwargs):

    if effect in effects:
        if effect == "Blur":
            return effects[effect](image, radius=kwargs.get("blur_radius", 2))
        elif effect == "Acrylic Overlay":
            return effects[effect](image, blur_radius=kwargs.get("blur_radius", 10), overlay_color=(255, 255, 255, 128))
        else:
            return effects[effect](image, **kwargs)
    else:
        return image
