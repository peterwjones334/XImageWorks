from PIL import Image
import os
import effects_aggregator

def add_border(image, border_size=50, border_color=(255, 255, 255), bottom_border_factor=1.5):
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

def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    allowed_extensions = {'.jpeg', '.jpg'}
    files = [file for file in sorted(os.listdir(input_folder)) if os.path.splitext(file)[1].lower() in allowed_extensions]

    for index, file in enumerate(files, start=1):
        input_image_path = os.path.join(input_folder, file)
        output_image_path = os.path.join(output_folder, f"{index:03d}{os.path.splitext(file)[1]}")
        kwargs = {}
        image = Image.open(input_image_path)
        
        # Apply effects sequentially and update the image
        image = effects_aggregator.effects['Polaroid'](image, **kwargs)
        # image = effects_aggregator.effects['BW Grain'](image, **kwargs)  # Uncomment to apply BW Grain effect
        image = effects_aggregator.effects['Color Grain'](image, **kwargs)
        image = add_border(image)
        
        # Save the result
        image.save(output_image_path)
        print(f"Processed and saved: {output_image_path}")

if __name__ == "__main__":
    input_folder = 'C:\\input'
    output_folder = 'C:\\output'
    process_images_in_folder(input_folder, output_folder)
