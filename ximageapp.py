from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image
import effects_aggregator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'
app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'jpg', 'png'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def apply_effects(image, effects, **kwargs):
    for effect in effects:
        if effect in effects_aggregator.effects:
            image = effects_aggregator.effects[effect](image, **kwargs)
        else:
            print(f"Effect '{effect}' not found in effects_aggregator.")
    return image

def resize_image(image, target_size):
    image.thumbnail(target_size, Image.LANCZOS)
    return image

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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_image_path)
            
            # Process the image
            image = Image.open(input_image_path)
            effects = request.form.getlist('effects')
            target_size = (800, 800)  # Example size, can be adjusted or made dynamic
            border_size = int(request.form.get('border_size', 50))
            border_color = (255, 255, 255)  # White border
            bottom_border_factor = float(request.form.get('bottom_border_factor', 1.5))
            
            image = apply_effects(image, effects)
            image = resize_image(image, target_size)
            image = add_border(image, border_size, border_color, bottom_border_factor)
            
            output_image_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            image.save(output_image_path)
            return redirect(url_for('processed_file', filename=filename))
    return render_template('upload.html', effects=effects_aggregator.effects.keys())

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
