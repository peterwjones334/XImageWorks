import numpy as np
from PIL import Image, ImageOps, ImageEnhance

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

# Export effects
noise_effects = {
    "Digital Noise": digital_noise_filter,
    "Spatial Noise": spatial_noise_filter,
    "Luminance Noise": luminance_noise_filter,
    "Fixed Pattern Noise": fpn_filter,
    "BW Grain": apply_bw_grain,
    "Color Grain": apply_color_grain,
    "Movie Film": movie_film_effect,
    "Polaroid": polaroid_effect,
    "Lomo": lomo_filter,
}
