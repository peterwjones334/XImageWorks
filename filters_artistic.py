from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np

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

def acrylic_overlay_effect(image, blur_radius=10, overlay_color=(255, 255, 255, 128)):
    blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    overlay = Image.new("RGBA", image.size, overlay_color)
    combined = Image.alpha_composite(blurred_image.convert("RGBA"), overlay)
    return combined.convert("RGB")

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

def outline_drawing(image):
    # Apply edge detection filter
    edges_image = image.filter(ImageFilter.FIND_EDGES)
    # Invert the colors of the edge-detected image
    inverted_image = ImageOps.invert(edges_image)
    grayscale_image = inverted_image.convert("L")
    return grayscale_image

def sketch_effect(image):
    # ... (same as before)
    pass

def oil_painting_effect(image):
    # ... (same as before)
    pass

def watercolor_effect(image):
    # ... (same as before)
    pass

def cartoon_effect(image):
    # ... (same as before)
    pass

# Export effects
artistic_effects = {
    "Rosy Tint": rosy_spectacle_filter,
    "Studio": Studio_filter,
    "HDR": hdr_filter,
    "xpro2": xpro2_filter,
    "Vintage1": vintage_filter_1,
    "Vintage2": vintage_filter_2,
    "Acrylic Overlay": acrylic_overlay_effect,
    "Mosaic": mosaic_effect,
    "Line Drawing": outline_drawing,
    "Sketch": sketch_effect,
    "Oil Painting": oil_painting_effect,
    "Watercolor": watercolor_effect,
    "Cartoon": cartoon_effect, 
}
