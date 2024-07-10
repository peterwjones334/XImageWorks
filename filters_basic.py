from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def sepia_filter(image):
    # ... (same as before)
    pass

def grayscale_filter(image):
    return image.convert("L")

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

# Export effects
basic_effects = {
    "Sepia": sepia_filter,
    "Grayscale": grayscale_filter,
    "Invert": invert_filter,
    "Brightness": brightness_filter,
    "Contrast": contrast_filter,
    "Sharpen": sharpen_filter,
    "Edge": edge_filter,
    "Emboss": emboss_filter,
}
