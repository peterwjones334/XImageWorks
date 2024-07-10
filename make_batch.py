from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import os
import effects_aggregator

def apply_effects(image, effects, **kwargs):
    """
    Apply a list of effects to an image.
    
    :param image: PIL Image object.
    :param effects: List of effect names to apply.
    :param kwargs: Additional arguments for the effects.
    :return: Modified image.
    """
    for effect in effects:
        if effect in effects_aggregator.effects:
            image = effects_aggregator.effects[effect](image, **kwargs)
        else:
            print(f"Effect '{effect}' not found in effects_aggregator.")
    return image

def resize_image(image, target_size):
    """
    Resize the image to the target size while maintaining aspect ratio.
    
    :param image: PIL Image object.
    :param target_size: Tuple (width, height) for resizing.
    :return: Resized image.
    """
    image.thumbnail(target_size, Image.LANCZOS)
    return image

def add_border(image, border_size=50, border_color=(255, 255, 255), bottom_border_factor=1.5):
    """
    Add a Polaroid-style border to an image.
    
    :param image: PIL Image object.
    :param border_size: Size of the border around the image.
    :param border_color: Color of the border.
    :param bottom_border_factor: Factor to increase the bottom border size for Polaroid effect.
    :return: Image with Polaroid border.
    """
    width, height = image.size
    if width > height:
        new_size = width
        left = 0
        top = (width - height) // 2
    else:
        new_size = height
        left = (height - width) // 2
        top = 0

    new_image = Image.new("RGB", (new_size, new_size), border_color)
    new_image.paste(image, (left, top))

    final_width = new_size + border_size * 2
    final_height = new_size + border_size * 2 + int(border_size * bottom_border_factor)

    final_image = Image.new("RGB", (final_width, final_height), border_color)
    final_image.paste(new_image, (border_size, border_size))

    return final_image

def process_images_in_folder(input_folder, output_folder, effects, target_size=(800, 800), border_size=50, border_color=(255, 255, 255), bottom_border_factor=1.5):
    """
    Process all images in a folder: apply effects, resize, add border, and save.
    
    :param input_folder: Path to the input folder.
    :param output_folder: Path to the output folder.
    :param effects: List of effect names to apply.
    :param target_size: Tuple (width, height) for resizing.
    :param border_size: Size of the border around the image.
    :param border_color: Color of the border.
    :param bottom_border_factor: Factor to increase the bottom border size for Polaroid effect.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    allowed_extensions = {'.jpeg', '.jpg'}
    files = [file for file in sorted(os.listdir(input_folder)) if os.path.splitext(file)[1].lower() in allowed_extensions]

    for index, file in enumerate(files, start=1):
        input_image_path = os.path.join(input_folder, file)
        output_image_path = os.path.join(output_folder, f"{index:03d}{os.path.splitext(file)[1]}")
        kwargs = {}
        image = Image.open(input_image_path)

        # Apply effects
        image = apply_effects(image, effects, **kwargs)
        
        # Resize image
        image = resize_image(image, target_size)
        
        # Add border
        image = add_border(image, border_size, border_color, bottom_border_factor)
        
        # Save the result
        image.save(output_image_path)
        print(f"Processed and saved: {output_image_path}")

if __name__ == "__main__":
    input_folder = 'C:\\input'
    output_folder = 'C:\\output'
    effects = ['Polaroid', 'Color Grain']  # List of effects to apply
    process_images_in_folder(input_folder, output_folder, effects, target_size=(800, 800), border_size=50, border_color=(255, 255, 255), bottom_border_factor=1.5)
