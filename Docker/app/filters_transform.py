from PIL import Image, ImageOps
import numpy as np

def extract_palette(image, num_colors=256):
    """
    Extract the color palette from an image.
    
    :param image: PIL Image object.
    :param num_colors: Number of colors to extract for the palette.
    :return: List of palette colors.
    """
    image = image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)
    palette = image.getpalette()
    palette = palette[:num_colors * 3]
    return [tuple(palette[i:i + 3]) for i in range(0, len(palette), 3)]

def apply_palette(image, palette):
    """
    Apply a new palette to the image.
    
    :param image: PIL Image object.
    :param palette: List of RGB tuples representing the new palette.
    :return: Image with the new palette applied.
    """
    image = image.convert("RGB")
    palette_image = Image.new("P", (1, 1))
    flat_palette = [value for color in palette for value in color]
    palette_image.putpalette(flat_palette + [0] * (768 - len(flat_palette)))
    
    # Quantize image to the new palette
    new_image = image.quantize(palette=palette_image)
    return new_image.convert("RGB")

def transform_palette(palette, transform_fn):
    """
    Apply a transformation function to each color in the palette.
    
    :param palette: List of RGB tuples representing the palette.
    :param transform_fn: Function to apply to each color.
    :return: Transformed palette.
    """
    return [transform_fn(color) for color in palette]

def lighten_transform(color):
    """
    Example color transformation function: Increase brightness.
    
    :param color: RGB tuple.
    :return: Transformed RGB tuple.
    """
    r, g, b = color
    r = min(255, int(r * 1.5))
    g = min(255, int(g * 1.5))
    b = min(255, int(b * 1.5))
    return (r, g, b)

def darken_transform(color):
    """
    Example color transformation function: Decrease brightness.
    
    :param color: RGB tuple.
    :return: Transformed RGB tuple.
    """
    r, g, b = color
    r = max(0, int(r * 0.5))
    g = max(0, int(g * 0.5))
    b = max(0, int(b * 0.5))
    return (r, g, b)

def increase_contrast_transform(color):
    """
    Example color transformation function: Increase contrast.
    
    :param color: RGB tuple.
    :return: Transformed RGB tuple.
    """
    factor = 1.5
    r, g, b = color
    r = min(255, max(0, int(128 + factor * (r - 128))))
    g = min(255, max(0, int(128 + factor * (g - 128))))
    b = min(255, max(0, int(128 + factor * (b - 128))))
    return (r, g, b)

def decrease_contrast_transform(color):
    """
    Example color transformation function: Decrease contrast.
    
    :param color: RGB tuple.
    :return: Transformed RGB tuple.
    """
    factor = 0.5
    r, g, b = color
    r = min(255, max(0, int(128 + factor * (r - 128))))
    g = min(255, max(0, int(128 + factor * (g - 128))))
    b = min(255, max(0, int(128 + factor * (b - 128))))
    return (r, g, b)

def sepia_transform(color):
    """
    Example color transformation function: Apply sepia effect.
    
    :param color: RGB tuple.
    :return: Transformed RGB tuple.
    """
    r, g, b = color
    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
    return (min(255, tr), min(255, tg), min(255, tb))

def invert_colors_transform(color):
    """
    Example color transformation function: Invert colors.
    
    :param color: RGB tuple.
    :return: Transformed RGB tuple.
    """
    r, g, b = color
    return (255 - r, 255 - g, 255 - b)

def process_image(image, transform_fn, num_colors=256):
    """
    Process an image: Extract palette, transform it, and reapply it.
    
    :param image: PIL Image object.
    :param transform_fn: Function to apply to each color in the palette.
    :param num_colors: Number of colors to use in the palette.
    :return: PIL Image object with transformed palette.
    """
    # Extract the palette
    palette = extract_palette(image, num_colors)
    
    # Transform the palette
    transformed_palette = transform_palette(palette, transform_fn)
    
    # Apply the transformed palette to the image
    new_image = apply_palette(image, transformed_palette)

    return new_image

# Export effects
transform_effects = {
    "tr_Lighten": lambda img: process_image(img, lighten_transform),
    "tr_Darken": lambda img: process_image(img, darken_transform),
    "tr_Increase Contrast": lambda img: process_image(img, increase_contrast_transform),
    "tr_Decrease Contrast": lambda img: process_image(img, decrease_contrast_transform),
    "tr_Sepia": lambda img: process_image(img, sepia_transform),
    "tr_Invert Colors": lambda img: process_image(img, invert_colors_transform),
}
