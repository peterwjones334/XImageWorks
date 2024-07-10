# README

## Image Effects Application

## Overview
This application allows users to apply various image effects to their photos using a graphical user interface (GUI). It leverages the tkinter library for the interface and the PIL library for image processing. Users can open images, apply different effects, adjust parameters using sliders, and save the processed images.

## Features
* Open and display images.
* Apply a variety of image effects.
* Adjust effect parameters using sliders.
* Save the processed images.
* Zoom and pan images for better viewing.

## Requirements
* Python 3.x
* tkinter
* Pillow (PIL)
* scipy (for some image effects)

## Installation
Install Python: Make sure you have Python installed. You can download it from python.org.

## Install Required Libraries:

```bash
pip install pillow scipy
```

## Clone the Repository: (If the code is hosted on a repository)

```bash
git clone https://github.com/yourusername/XImageWorks.git
cd XImageWorks
```

## Usage

Run the Application:

```bash
python ximageworks_0.2.py
```

Open an Image:

* Click the "Open Image" button.
* Browse and select the image file you want to process.

Select an Effect:

* Use the dropdown menu to select the desired effect from the list of available effects.

Adjust Parameters:

* If the selected effect has adjustable parameters, sliders will appear.
* Move the sliders to adjust the parameters as desired.

Save the Processed Image:

* Click the "Save Image" button.
* Choose the location and file name for the processed image.

## Code Structure

image_effects.py: Contains functions for various image effects.
slider_handling.py: Manages the creation and updating of sliders for effect parameters.
file_handling.py: Handles opening and saving image files.

## Customization
You can customize the effects by modifying the image_effects.py file and adding new functions or adjusting existing ones. The effects dictionary in image_effects.py maps effect names to their corresponding functions.

## Troubleshooting
Ensure all dependencies are installed: Make sure you have installed all the required libraries (tkinter, Pillow, and scipy).
Check file paths: Ensure that the paths to image files are correct when opening and saving images.

## License
This project is licensed under the MIT License.
