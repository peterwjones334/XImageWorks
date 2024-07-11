# Image Processing Application

This Flask application allows users to upload images, apply various effects, and compare the original and processed images side by side. Users can also save the processed images.

## Directory Structure

```text
your_project/
│
├── static/
│ ├── css/
│ │ └── styles.css
│ └── js/
│ └── scripts.js
├── templates/
│ └── upload.html
└── ximageapp.py
```

## Prerequisites

- Python 3.x
- Flask
- Pillow (PIL)
- `effects_aggregator` module (this contains your image effects functions)

## Installation

1. Clone the repository or download the files.

2. Install the required Python packages:

```sh
    pip install Flask Pillow
```

3. Ensure your `effects_aggregator` module is in the project directory or install it if it is a separate package.

## Running the Application

1. Navigate to the project directory.

2. Run the Flask application:

```sh
    python ximageapp_0x.py
```

3. Open your web browser and go to `http://127.0.0.1:5000`.

## Project Files

### `xiamgeapp.py`

This is the main application file that sets up the Flask server, handles file uploads, applies image effects, and serves the processed images.

### `templates/upload.html`

This is the main HTML template for the application. It provides the user interface for uploading files, selecting effects, and comparing images.

### `static/css/styles.css`
This file contains the styles for the application.

### `static/js/scripts.js`
This file contains the JavaScript functionality for the image comparison slider.

## How to Use

* **Upload an Image**: Click "Choose File" and select an image from your computer. Then click "Upload".
* **Apply an Effect**: Choose an effect from the drop-down menu and click "Apply Effect".
* **Compare Images**: Use the slider to compare the original and processed images.
* **Save the Processed Image**: Click the "Save" button to save the processed image to the predefined directory.