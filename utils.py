import os
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename
import effects_aggregator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file, folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(folder, filename)
    file.save(file_path)
    return filename, file_path

def process_image(input_image_path, effect):
    image = Image.open(input_image_path)
    if effect in effects_aggregator.effects:
        image = effects_aggregator.effects[effect](image)
    output_image_path = os.path.join(current_app.config['PROCESSED_FOLDER'], os.path.basename(input_image_path))
    image.save(output_image_path)
    return output_image_path
