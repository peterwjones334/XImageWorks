# slider_handling.py
import tkinter as tk
from tkinter import Scale
import image_effects

# Dictionary to map effects to their corresponding sliders
effect_sliders = {
    "Pixel Prism": {"block_size": {"from_": 5, "to": 50, "label": "Block Size"}},
    "Mosaic": {"block_size": {"from_": 5, "to": 50, "label": "Block Size"}},
    "Halftone": {"dot_size": {"from_": 1, "to": 50, "label": "Dot Size"}},
    "Posterize": {"levels": {"from_": 2, "to": 256, "label": "Levels"}},
    "Voronoi": {"num_points": {"from_": 10, "to": 500, "label": "Number of Points"}},
    "Blur": {"blur_radius": {"from_": 1, "to": 10, "label": "Blur Radius"}},
    "Acrylic Overlay": {"blur_radius": {"from_": 1, "to": 10, "label": "Blur Radius"}},
    "Lima": {"grain_amount": {"from_": 0, "to": 100, "label": "Grain Amount"}},
}

def create_sliders(root, update_output_image_callback):
    sliders = {}
    for effect, params in effect_sliders.items():
        sliders[effect] = {}
        for param, options in params.items():
            slider = Scale(root, from_=options["from_"], to=options["to"], orient=tk.HORIZONTAL, label=options["label"], command=update_output_image_callback)
            slider.pack_forget()
            sliders[effect][param] = slider
    return sliders

def update_output_image(effect_var, sliders, output_frame):
    def _update(input_image=None, *args):
        if input_image:
            effect = effect_var.get()
            kwargs = {}
            if effect in sliders:
                for param, slider in sliders[effect].items():
                    kwargs[param] = slider.get()
            
            output_image = image_effects.process_image(input_image, effect, **kwargs)
            output_frame.update_image(output_image)
    
    return _update

def update_sliders(effect_var, sliders, update_output_image_callback):
    def _update(*args):
        effect = effect_var.get()
        for effect_sliders in sliders.values():
            for slider in effect_sliders.values():
                slider.pack_forget()
        if effect in sliders:
            for slider in sliders[effect].values():
                slider.pack(side=tk.TOP, pady=10)
        update_output_image_callback()
    
    return _update
