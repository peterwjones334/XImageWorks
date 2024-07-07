# PixelPrism_v0.12.py
import tkinter as tk
from PIL import ImageTk
import image_effects
import slider_handling
import file_handling

class ScrollableImage(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.v_scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.image_frame.bind("<Configure>", self.on_frame_configure)
        
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def update_image(self, img):
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        self.image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self.image_frame, image=self.image)
        self.image_label.image = self.image  # Keep a reference to avoid garbage collection
        self.image_label.pack()

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
effect_var.set("Pixel Prism")

# Initialize callbacks
def update_output_image(*args):
    global output_image, input_image
    if input_image:
        effect = effect_var.get()
        kwargs = {}
        if effect in sliders:
            for param, slider in sliders[effect].items():
                kwargs[param] = slider.get()
        
        output_image = image_effects.process_image(input_image, effect, **kwargs)
        output_frame.update_image(output_image)

# Create sliders
sliders = slider_handling.create_sliders(root, update_output_image)

# Update callbacks with proper sliders
update_sliders_callback = slider_handling.update_sliders(effect_var, sliders, update_output_image)

effect_menu = tk.OptionMenu(root, effect_var, *image_effects.effects.keys(), command=update_sliders_callback)
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
