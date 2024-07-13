from PIL import Image, ImageOps, ImageEnhance, ImageFilter

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

def raw_image(image):
    return image

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

def posterize_image(image, levels=4):
    levels = max(2, min(256, levels))
    return ImageOps.posterize(image, 8 - levels.bit_length())

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

# Export effects
basic_effects = {
    "Default": raw_image,
    "Sepia": sepia_filter,
    "Grayscale": grayscale_filter,
    "Invert": invert_filter,
    "Brightness": brightness_filter,
    "Contrast": contrast_filter,
    "Sharpen": sharpen_filter,
    "Edge": edge_filter,
    "Emboss": emboss_filter,
    "Posterize": posterize_image,
    "Cool": cool_filter,
    "Warm": warm_filter,
}
