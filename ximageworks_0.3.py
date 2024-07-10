# ximageworks_0.3.py

import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import effects_aggregator
import slider_handling
import file_handling

class ScrollableImage(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, width=800, height=600)  # Set larger size for canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.image = None
        self.image_id = None
        self.zoom_level = 1.0

    def on_button_press(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def on_mouse_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom(1.1)
        else:
            self.zoom(0.9)

    def zoom(self, factor):
        self.zoom_level *= factor
        self.update_image(self.original_image)

    def update_image(self, img):
        if img is None:
            print("Error: No image to update")
            return
        self.original_image = img
        width, height = img.size
        width = int(width * self.zoom_level)
        height = int(height * self.zoom_level)
        resized_image = img.resize((width, height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)
        
        if self.image_id:
            self.canvas.delete(self.image_id)

        self.image_id = self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(self.image_id))
        self.canvas.xview_moveto(0.5 - self.canvas.canvasx(0) / self.canvas.winfo_width())
        self.canvas.yview_moveto(0.5 - self.canvas.canvasy(0) / self.canvas.winfo_height())

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
        try:
            output_image = effects_aggregator.effects[effect](input_image, **kwargs)
            if output_image is None:
                raise ValueError(f"Effect '{effect}' returned None")
            output_frame.update_image(output_image)
        except Exception as e:
            print(f"Error applying effect '{effect}': {e}")

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