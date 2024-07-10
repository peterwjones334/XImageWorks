from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from scipy.spatial import Voronoi
import cv2
from skimage import io, filters, color, exposure
import matplotlib.pyplot as plt

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

# Grey scale + grain
def lima_effect(image, grain_amount=50):
    grayscale_image = image.convert("L")
    np_image = np.array(grayscale_image)
    noise = np.random.normal(0, grain_amount, np_image.shape).astype(np.uint8)
    noisy_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

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

def cartoon_effect_opencv(image_path):
    """
    Apply a cartoon effect to an image using OpenCV.

    :param image_path: Path to the input image.
    :return: The image with a cartoon effect.
    """
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur
    gray = cv2.medianBlur(gray, 5)
    
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, 9, 9)
    
    # Apply bilateral filter to reduce color palette
    color = cv2.bilateralFilter(img, 9, 300, 300)
    
    # Combine edges and color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    return cartoon

def oil_painting_effect_skimage(image_path):
    """
    Apply an oil painting effect to an image using scikit-image.

    :param image_path: Path to the input image.
    :return: The image with an oil painting effect.
    """
    image = io.imread(image_path)
    
    # Convert to grayscale
    gray_image = color.rgb2gray(image)
    
    # Apply median filter to simulate oil painting
    oil_painting_image = filters.rank.median(gray_image, np.ones((5, 5)))
    
    return oil_painting_image

# Export effects
custom_effects = {
    "Grain Blur": Custom_filter1,
    "RGB - ": Custom_filter2,
    "Lima": lima_effect,
    "Halftone": halftone_effect,  
    "Voronoi": voronoi_prism_effect,
    "Pixel Prism": pixel_prism_window, 
    #"Ocv_Cartoon": cartoon_effect_opencv,
    #"Ski_Oil": oil_painting_effect_skimage,
}
