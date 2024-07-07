# Filters

## Color Filters

Common color filters used in image processing and photography to achieve various visual effects include:

- Sepia: Gives images a warm, brownish tone, mimicking old photographs.
- Black and White (Grayscale): Converts images to shades of gray, removing all color.
- Vintage/Retro: Applies a faded look with warm or cool tints to mimic older photos.
- Cool Filter: Adds a blue tint to images, creating a cooler look.
- Warm Filter: Adds a red or yellow tint to images, creating a warmer look.
- Red Filter: Enhances red tones and can make other colors appear darker or more intense.
- Green Filter: Enhances green tones, useful for nature photography.
- Blue Filter: Enhances blue tones, useful for skies and water.
- High Contrast: Increases the difference between light and dark areas, making images appear more dynamic.
- Low Contrast: Decreases the difference between light and dark areas, creating a softer look.
- Brightness: Adjusts the overall lightness or darkness of the image.
- Saturation: Adjusts the intensity of colors in the image.
- Lomo: Mimics the look of Lomo cameras with high contrast, vignette, and saturated colors.
- Negative: Inverts the colors of the image, similar to photo negatives.
- HDR (High Dynamic Range): Enhances the range of light and dark areas, creating a more detailed image.
- Duotone: Uses two colors to create a unique effect, often used in graphic design.
- Color Pop: Keeps one color while converting the rest of the image to black and white.
- Gotham: A high-contrast, blue-toned filter.
- Kelvin: Adds a warm, yellowish tint.
- X-Pro II: A cross-processing filter with strong vignette, high contrast, and a golden tint.

## Code

Let's implement a few of these common filters in our application:

- Sepia
- Cool Filter
- Warm Filter
- Vintage/Retro
- Movie
- Polaroid

```Python

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

def movie_film_effect(image):
    image = image.convert("RGB")
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2)
    g = g.point(lambda i: i * 1.1)
    b = b
    b = b.point(lambda i: i * 0.9)
    image = Image.merge("RGB", (r, g, b))
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    return image

def polaroid_effect(image):
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
    green_overlay = Image.new("RGB", image.size, (0, 50, 0))
    image = Image.blend(image, green_overlay, alpha=0.2)
    
    return image
```
