# Summary of the Code and Functions

**sepia_filter(image):**

Applies a sepia tone to the image, giving it a warm, brownish tint.
**xpro2_filter(image, kwargs):**

Applies an X-Pro II-like filter with a golden tint, increased contrast, and vignette effect.
**pixel_prism_window(image, block_size=25):**

Applies a pixel prism window effect by resizing and averaging colors in blocks.
**mosaic_effect(image, block_size=25):**

Creates a mosaic effect by resizing and replicating color blocks.
**halftone_effect(image, dot_size=10):**

Converts the image to a halftone effect with dots of varying sizes.
**voronoi_prism_effect(image, num_points=100):**

Applies a Voronoi prism effect using random points for a geometric pattern.
acrylic_overlay_effect(image, blur_radius=10, overlay_color=(255, 255, 255, 128)):

Adds an acrylic overlay with a blur effect and an optional color tint.
**movie_film_effect(image):**

Simulates a movie film look by adjusting RGB channels and contrast.
**polaroid_effect(image):**

Applies a Polaroid-like effect with adjusted RGB channels and contrast, along with a green overlay.
**lomo_filter(image):**

Mimics the look of a Lomo camera with increased saturation, contrast, and a vignette effect.
**lima_effect(image, grain_amount=50):**

Applies a grayscale filter with added grain for a vintage look.
**raw_image(image):**

Returns the original image without any modifications.
**grayscale_filter(image):**

Converts the image to grayscale.
**posterize_image(image, levels=4):**

Reduces the number of colors in the image to create a posterized effect.
**blur_image(image, radius=2):**

Applies a Gaussian blur to the image.
**invert_filter(image):**

Inverts the colors of the image.
**brightness_filter(image, factor=1.5):**

Adjusts the brightness of the image.
**contrast_filter(image, factor=1.5):**

Adjusts the contrast of the image.
**sharpen_filter(image):**

Sharpens the image.
**edge_filter(image):**

Applies an edge detection filter to the image.
**emboss_filter(image):**

Embosses the image.
**cool_filter(image):**

Applies a cool (blue) filter to the image.
**warm_filter(image):**

Applies a warm (red) filter to the image.
**vintage_filter_1(image):**

Applies a vintage filter with adjusted RGB channels.
**vintage_filter_2(image):**

Applies a vintage filter with reduced saturation, adjusted contrast, and a warm tint.
**outline_drawing(image):**

Converts the image to an outline drawing.
**adjust_rgb(image, r_factor, g_factor, b_factor):**

Adjusts the RGB channels of the image.
**add_grain(image, amount):**

Adds grain to the image.
**combined_filter1(image, r_factor=1.1, g_factor=1.1, b_factor=0.9, grain_amount=0.1, blur_radius=2):**

Applies a combined filter that adjusts RGB, adds grain, and applies blur.
**Custom_filter1(image):**

Applies the custom combined filter 1.
**combined_filter2(image, r_factor=1.0, g_factor=1.0, b_factor=1.0):**

Applies a combined filter that adjusts RGB only.
**Custom_filter2(image):**

Applies the custom combined filter 2.
**hdr_filter(image):**

Applies an HDR (High Dynamic Range) filter to the image.
digital_noise_filter(image, noise_level=30):**
**
Adds digital noise to the image.
**spatial_noise_filter(image, random_noise_level=30, patterned_noise_level=20, pattern_frequency=10):**

Adds spatial noise to the image.
**luminance_noise_filter(image, noise_level=30):**

Adds luminance noise to the image.
**fpn_filter(image, noise_level=30):**

Adds fixed pattern noise to the image.
**generate_grain_mask(img_width, img_height, grain_size, seed=None):**

Generates a grain mask for adding film grain effect.
**apply_bw_grain(image, grain_size=10, seed=None):**

Applies black and white film grain to an image.
**apply_color_grain(image, grain_size=10, seed=None):**

Applies color film grain to an image.
**Studio_filter(image):**

Applies a high-contrast black and white filter to mimic the style of New York studio photos.
**rosy_spectacle_filter(image, tint_color=(255, 182, 193), intensity=0.5):**

Applies a rosy spectacle tint to an image.

**process_image(image, effect, kwargs):**

Applies the specified effect to the image based on the provided effect name and parameters

## Code

```Python

# image_effects.py
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance
from scipy.spatial import Voronoi

def sepia_filter(image):
    """
    Apply a sepia filter to the image.

    :param image: The original image.
    :return: The sepia-filtered image.
    """
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
    """
    Apply an X-Pro II-like filter to the image.

    :param image: The original image.
    :return: The X-Pro II-filtered image.
    """
    width, height = image.size
    pixels = image.load()

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
            dx = x - width / 2
            dy = y - height / 2
            d = np.sqrt(dx * dx + dy * dy) / (np.sqrt(width * width + height * height) / 2)
            vignette.putpixel((x, y), int((1 - d) * 255))
    image = Image.composite(image, ImageOps.colorize(vignette, (0, 0, 0), (255, 255, 255)), vignette)

    # Apply blur to vignette
    image = image.filter(ImageFilter.GaussianBlur(radius=2))

    return image

def pixel_prism_window(image, block_size=25):
    """
    Apply a pixel prism window effect to the image.

    :param image: The original image.
    :param block_size: The size of the blocks.
    :return: The image with a pixel prism window effect.
    """
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
    """
    Apply a mosaic effect to the image.

    :param image: The original image.
    :param block_size: The size of the mosaic blocks.
    :return: The image with a mosaic effect.
    """
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
    """
    Apply a halftone effect to the image.

    :param image: The original image.
    :param dot_size: The size of the halftone dots.
    :return: The image with a halftone effect.
    """
    width, height = image.size
    output_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(output_image)
    for x in range(0, width, dot_size):
        for y in range(0, height, dot_size):
            box = image.crop((x, y, x + dot_size, y + dot_size))
            average_luminance = int(np.mean(box.convert("L")))
            radius = (average_luminance / 255) * (dot_size / 2)
            center = (x + dot_size // 2, y + dot_size // 2)
            draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), fill=box.getpixel((dot_size // 2, dot_size // 2)))
    return output_image

def voronoi_prism_effect(image, num_points=100):
    """
    Apply a Voronoi prism effect to the image.

    :param image: The original image.
    :param num_points: The number of points for the Voronoi diagram.
    :return: The image with a Voronoi prism effect.
    """
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
    """
    Apply an acrylic overlay effect to the image.

    :param image: The original image.
    :param blur_radius: The radius for the Gaussian blur.
    :param overlay_color: The RGBA color for the overlay.
    :return: The image with an acrylic overlay effect.
    """
    blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    overlay = Image.new("RGBA", image.size, overlay_color)
    combined = Image.alpha_composite(blurred_image.convert("RGBA"), overlay)
    return combined.convert("RGB")

def movie_film_effect(image):
    """
    Apply a movie film effect to the image.

    :param image: The original image.
    :return: The image with a movie film effect.
    """
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
    """
    Apply a Polaroid-like effect to the image.

    :param image: The original image.
    :return: The image with a Polaroid effect.
    """
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
    """
    Apply a Lomo camera effect to the image.

    :param image: The original image.
    :return: The image with a Lomo effect.
    """
    image = ImageEnhance.Color(image).enhance(1.5)
    image = ImageEnhance.Contrast(image).enhance(1.5)

    width, height = image.size
    vignette = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            dx = x - width / 2
            dy = y - height / 2
            d = np.sqrt(dx * dx + dy * dy) / (np.sqrt(width * width + height * height) / 2)
            vignette.putpixel((x, y), int((1 - d) * 255))
    image = Image.composite(image, ImageOps.colorize(vignette, (0, 0, 0), (255, 255, 255)), vignette)

    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))

    return image

def lima_effect(image, grain_amount=50):
    """
    Apply a grayscale filter with added grain.

    :param image: The original image.
    :param grain_amount: The amount of grain to add.
    :return: The image with a grayscale and grain effect.
    """
    grayscale_image = image.convert("L")
    np_image = np.array(grayscale_image)
    noise = np.random.normal(0, grain_amount, np_image.shape).astype(np.uint8)
    noisy_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

def raw_image(image):
    """
    Return the original image without any modifications.

    :param image: The original image.
    :return: The original image.
    """
    return image

def grayscale_filter(image):
    """
    Apply a grayscale filter to the image.

    :param image: The original image.
    :return: The grayscale image.
    """
    return image.convert("L")

def posterize_image(image, levels=4):
    """
    Apply a posterize effect to the image.

    :param image: The original image.
    :param levels: The number of levels to posterize the image.
    :return: The posterized image.
    """
    levels = max(2, min(256, levels))
    return ImageOps.posterize(image, 8 - levels.bit_length())

def blur_image(image, radius=2):
    """
    Apply a Gaussian blur to the image.

    :param image: The original image.
    :param radius: The radius of the Gaussian blur.
    :return: The blurred image.
    """
    return image.filter(ImageFilter.GaussianBlur(radius))

def invert_filter(image):
    """
    Apply an invert filter to the image.

    :param image: The original image.
    :return: The inverted image.
    """
    return ImageOps.invert(image)

def brightness_filter(image, factor=1.5):
    """
    Adjust the brightness of the image.

    :param image: The original image.
    :param factor: The factor by which to adjust the brightness.
    :return: The brightness-adjusted image.
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def contrast_filter(image, factor=1.5):
    """
    Adjust the contrast of the image.

    :param image: The original image.
    :param factor: The factor by which to adjust the contrast.
    :return: The contrast-adjusted image.
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def sharpen_filter(image):
    """
    Sharpen the image.

    :param image: The original image.
    :return: The sharpened image.
    """
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(2.0)

def edge_filter(image):
    """
    Apply an edge detection filter to the image.

    :param image: The original image.
    :return: The image with edges detected.
    """
    return image.filter(ImageFilter.FIND_EDGES)

def emboss_filter(image):
    """
    Apply an emboss filter to the image.

    :param image: The original image.
    :return: The embossed image.
    """
    return image.filter(ImageFilter.EMBOSS)

def cool_filter(image):
    """
    Apply a cool (blue) filter to the image.

    :param image: The original image.
    :return: The image with a cool filter applied.
    """
    r, g, b = image.split()
    r = r.point(lambda i: i * 0.9)
    b = b.point(lambda i: i * 1.2)
    return Image.merge("RGB", (r, g, b))

def warm_filter(image):
    """
    Apply a warm (red) filter to the image.

    :param image: The original image.
    :return: The image with a warm filter applied.
    """
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    b = b.point(lambda i: i * 0.9)
    return Image.merge("RGB", (r, g, b))

def vintage_filter_1(image):
    """
    Apply a vintage filter to the image (version 1).

    :param image: The original image.
    :return: The image with a vintage filter applied.
    """
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.1)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    return Image.merge("RGB", (r, g, b))

def vintage_filter_2(image):
    """
    Apply a vintage filter to the image (version 2).

    :param image: The original image.
    :return: The image with a vintage filter applied.
    """
    image = ImageEnhance.Color(image).enhance(0.5)
    image = ImageEnhance.Contrast(image).enhance(0.9)

    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    g = g.point(lambda i: i * 1.1)
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))

    width, height = image.size
    vignette = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            dx = x - width / 2
            dy = y - height / 2
            d = np.sqrt(dx * dx + dy * dy) / (np.sqrt(width * width + height * height) / 2)
            vignette.putpixel((x, y), int((1 - d) * 255))
    image = Image.composite(image, ImageOps.colorize(vignette, (0, 0, 0), (255, 255, 255)), vignette)

    return image

def outline_drawing(image):
    """
    Apply an outline drawing effect to the image.

    :param image: The original image.
    :return: The image with an outline drawing effect.
    """
    edges_image = image.filter(ImageFilter.FIND_EDGES)
    inverted_image = ImageOps.invert(edges_image)
    grayscale_image = inverted_image.convert("L")
    return grayscale_image

def adjust_rgb(image, r_factor, g_factor, b_factor):
    """
    Adjust the RGB values of the image.

    :param image: The original image.
    :param r_factor: The factor by which to adjust the red channel.
    :param g_factor: The factor by which to adjust the green channel.
    :param b_factor: The factor by which to adjust the blue channel.
    :return: The RGB-adjusted image.
    """
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
    """
    Add grain to the image.

    :param image: The original image.
    :param amount: The amount of grain to add.
    :return: The image with grain added.
    """
    width, height = image.size
    grain = np.random.normal(scale=amount * 255, size=(height, width, 3))
    grain_image = Image.fromarray(np.clip(np.array(image) + grain, 0, 255).astype('uint8'))
    return grain_image

def combined_filter1(image, r_factor=1.1, g_factor=1.1, b_factor=0.9, grain_amount=0.1, blur_radius=2):
    """
    Apply a combined filter that adjusts RGB, adds grain, and applies blur.

    :param image: The original image.
    :param r_factor: The factor to adjust the red channel.
    :param g_factor: The factor to adjust the green channel.
    :param b_factor: The factor to adjust the blue channel.
    :param grain_amount: The amount of grain to add.
    :param blur_radius: The radius of the Gaussian blur.
    :return: The image with the combined filter applied.
    """
    image = adjust_rgb(image, r_factor, g_factor, b_factor)
    image = add_grain(image, grain_amount)
    image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    return image

def Custom_filter1(image):
    """
    Apply the custom combined filter 1.

    :param image: The original image.
    :return: The filtered image.
    """
    filtered_image = combined_filter1(image)
    filtered_image.show()
    return filtered_image

def combined_filter2(image, r_factor=1.0, g_factor=1.0, b_factor=1.0):
    """
    Apply a combined filter that adjusts RGB only.

    :param image: The original image.
    :param r_factor: The factor to adjust the red channel.
    :param g_factor: The factor to adjust the green channel.
    :param b_factor: The factor to adjust the blue channel.
    :return: The image with the combined filter applied.
    """
    image = adjust_rgb(image, r_factor, g_factor, b_factor)
    return image

def Custom_filter2(image):
    """
    Apply the custom combined filter 2.

    :param image: The original image.
    :return: The filtered image.
    """
    filtered_image = combined_filter2(image)
    filtered_image.show()
    return filtered_image

def hdr_filter(image):
    """
    Apply an HDR (High Dynamic Range) filter to the image.

    :param image: The original image.
    :return: The HDR-filtered image.
    """
    image = image.filter(ImageFilter.DETAIL)
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(1.5)
    sharpness_enhancer = ImageEnhance.Sharpness(image)
    image = sharpness_enhancer.enhance(2.0)
    brightness_enhancer = ImageEnhance.Brightness(image)
    image = brightness_enhancer.enhance(1.1)
    return image

def digital_noise_filter(image, noise_level=30):
    """
    Apply digital noise to the image.

    :param image: The original image.
    :param noise_level: The level of noise to add.
    :return: The image with digital noise added.
    """
    np_image = np.array(image)
    noise = np.random.randint(-noise_level, noise_level, np_image.shape, dtype='int16')
    np_image = np.clip(np_image + noise, 0, 255).astype('uint8')
    noisy_image = Image.fromarray(np_image)
    return noisy_image

def spatial_noise_filter(image, random_noise_level=30, patterned_noise_level=20, pattern_frequency=10):
    """
    Apply spatial noise to the image.

    :param image: The original image.
    :param random_noise_level: The level of random noise to add.
    :param patterned_noise_level: The level of patterned noise to add.
    :param pattern_frequency: The frequency of the pattern noise.
    :return: The image with spatial noise added.
    """
    np_image = np.array(image)
    random_noise = np.random.randint(-random_noise_level, random_noise_level, np_image.shape, dtype='int16')
    patterned_noise = np.zeros_like(np_image, dtype='int16')
    rows, cols, _ = np_image.shape
    for row in range(rows):
        for col in range(cols):
            patterned_noise[row, col] = int(patterned_noise_level * np.sin(2 * np.pi * (row / pattern_frequency) * np.sin(2 * np.pi * (col / pattern_frequency))))
    np_image = np.clip(np_image + random_noise + patterned_noise, 0, 255).astype('uint8')
    noisy_image = Image.fromarray(np_image)
    return noisy_image

def luminance_noise_filter(image, noise_level=30):
    """
    Apply luminance noise to the image.

    :param image: The original image.
    :param noise_level: The level of noise to add.
    :return: The image with luminance noise added.
    """
    luminance = image.convert("L")
    np_luminance = np.array(luminance)
    noise = np.random.randint(-noise_level, noise_level, np_luminance.shape, dtype='int16')
    np_luminance = np.clip(np_luminance + noise, 0, 255).astype('uint8')
    noisy_luminance = Image.fromarray(np_luminance)

    if image.mode == 'RGB':
        r, g, b = image.split()
        noisy_image = Image.merge("RGB", (r, g, b)).convert("L")
        noisy_image = Image.merge("RGB", (noisy_luminance, noisy_luminance, noisy_luminance))
    else:
        noisy_image = noisy_luminance

    return noisy_image

def fpn_filter(image, noise_level=30):
    """
    Apply fixed pattern noise to the image.

    :param image: The original image.
    :param noise_level: The level of fixed pattern noise to add.
    :return: The image with fixed pattern noise added.
    """
    np_image = np.array(image)
    rows, cols, _ = np_image.shape
    fpn_noise = np.random.randint(-noise_level, noise_level, (rows, cols, 1), dtype='int16')
    fpn_noise = np.repeat(fpn_noise, 3, axis=2)
    np_image = np.clip(np_image + fpn_noise, 0, 255).astype('uint8')
    noisy_image = Image.fromarray(np_image)
    return noisy_image

def generate_grain_mask(img_width, img_height, grain_size, seed=None):
    """
    Generate a grain mask for adding film grain effect.

    :param img_width: The width of the image.
    :param img_height: The height of the image.
    :param grain_size: The size of the grain.
    :param seed: The random seed for grain generation.
    :return: The grain mask.
    """
    np.random.seed(seed)
    noise = np.random.normal(loc=0, scale=grain_size, size=(img_height, img_width))
    noise = np.clip(noise, -255, 255)
    noise = (noise - noise.min()) / (noise.max() - noise.min()) * 255
    mask = Image.fromarray(noise.astype(np.uint8))
    return mask

def apply_bw_grain(image, grain_size=10, seed=None):
    """
    Apply black and white film grain to an image.

    :param image: The original image.
    :param grain_size: The size of the grain.
    :param seed: The random seed for grain generation.
    :return: The image with black and white film grain added.
    """
    if image.mode != 'L':
        image = image.convert('L')

    img_width, img_height = image.size
    grain_mask = generate_grain_mask(img_width, img_height, grain_size, seed)
    grain_image = Image.blend(image, grain_mask, alpha=0.5)
    return grain_image

def apply_color_grain(image, grain_size=10, seed=None):
    """
    Apply color film grain to an image.

    :param image: The original image.
    :param grain_size: The size of the grain.
    :param seed: The random seed for grain generation.
    :return: The image with color film grain added.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    img_width, img_height = image.size
    grain_mask = generate_grain_mask(img_width, img_height, grain_size, seed)
    grain_mask = grain_mask.convert('RGB')
    grain_image = Image.blend(image, grain_mask, alpha=0.5)
    return grain_image

def Studio_filter(image):
    """
    Apply a high-contrast black and white filter to an image to mimic the style of New York studio photos.

    :param image: The original image.
    :return: The filtered image.
    """
    bw_image = ImageOps.grayscale(image)
    contrast_enhancer = ImageEnhance.Contrast(bw_image)
    bw_image = contrast_enhancer.enhance(2.0)  # Adjust the factor to achieve the desired contrast
    bw_image = ImageOps.autocontrast(bw_image, cutoff=10)  # Adjust the cutoff to achieve the desired starkness
    return bw_image

def rosy_spectacle_filter(image, tint_color=(255, 182, 193), intensity=0.5):
    """
    Apply a rosy spectacle tint to an image.

    :param image: The original image.
    :param tint_color: The RGB color of the tint (default is light pink).
    :param intensity: The intensity of the tint (0.0 to 1.0).
    :return: The tinted image.
    """
    tint_overlay = Image.new('RGB', image.size, tint_color)
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
    """
    Apply the specified effect to the image.

    :param image: The original image.
    :param effect: The effect to apply.
    :param kwargs: Additional keyword arguments for specific effects.
    :return: The image with the effect applied.
    """
    if effect in effects:
        if effect == "Blur":
            return effects[effect](image, radius=kwargs.get("blur_radius", 2))
        elif effect == "Acrylic Overlay":
            return effects[effect](image, blur_radius=kwargs.get("blur_radius", 10), overlay_color=(255, 255, 255, 128))
        else:
            return effects[effect](image, **kwargs)
    else:
        return image
```