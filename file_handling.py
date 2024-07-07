# file_handling.py
from tkinter import filedialog
from PIL import Image

def open_image(input_frame, update_output_image_callback):
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = Image.open(file_path)
        input_frame.update_image(input_image)
        update_output_image_callback()
        return input_image
    return None

def save_image(output_image):
    if output_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            output_image.save(save_path)
