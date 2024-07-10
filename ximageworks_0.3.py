# ximageworks_0.3.py

import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import effects_aggregator
import slider_handling
import file_handling

class ScrollableImage(tk.Frame):
    # ... (same as before)
    pass

def set_input_image(image):
    global input_image
    input_image = image

def open_image():
    global input_image
    input_image = file_handling.open_image(input_frame, update_output_image)

def save_image():
    global output_image
    file_handling.save_image(output_image)

# Initialize the main window
root = tk.Tk()
root.title("Image Effects")

# Create frames for input and output images using the ScrollableImage class
input_frame = ScrollableImage(root)
input_frame.pack(side=tk.LEFT, padx=10, pady=10)

output_frame = ScrollableImage(root)
output_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Option menu to select effect
effect_var = tk.StringVar(root)
effect_var.set("Default")

# Initialize callbacks
def update_output_image(*args):
    global output_image, input_image
    if input_image:
        effect = effect_var.get()
        kwargs = {}
        if effect in sliders:
            for param, slider in sliders[effect].items():
                kwargs[param] = slider.get()
        
        output_image = effects_aggregator.effects[effect](input_image, **kwargs)
        output_frame.update_image(output_image)

# Create sliders
sliders = slider_handling.create_sliders(root, update_output_image)

# Update callbacks with proper sliders
update_sliders_callback = slider_handling.update_sliders(effect_var, sliders, update_output_image)

effect_menu = tk.OptionMenu(root, effect_var, *effects_aggregator.effects.keys(), command=update_sliders_callback)
effect_menu.pack(side=tk.TOP, pady=10)

# Buttons to open and save images
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(side=tk.TOP, pady=10)

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(side=tk.TOP, pady=10)

# Initialize global variables
input_image = None
output_image = None

# Run the main loop
root.mainloop()
