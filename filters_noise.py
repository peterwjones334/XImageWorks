import numpy as np
from PIL import Image

def digital_noise_filter(image, noise_level=30):
    # ... (same as before)
    pass

def spatial_noise_filter(image, random_noise_level=30, patterned_noise_level=20, pattern_frequency=10):
    # ... (same as before)
    pass

def luminance_noise_filter(image, noise_level=30):
    # ... (same as before)
    pass

def fpn_filter(image, noise_level=30):
    # ... (same as before)
    pass

# Export effects
noise_effects = {
    "Digital Noise": digital_noise_filter,
    "Spatial Noise": spatial_noise_filter,
    "Luminance Noise": luminance_noise_filter,
    "Fixed Pattern Noise": fpn_filter,
}
