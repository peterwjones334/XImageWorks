from flask import Blueprint, request, render_template, redirect, url_for, send_from_directory, session, current_app
import os
from utils import allowed_file, save_file, process_image
import effects_aggregator
from werkzeug.utils import secure_filename
from PIL import Image

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                input_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(input_image_path)
                session['filename'] = filename
                return render_template('upload.html', filename=filename, effects=effects_aggregator.effects.keys())
        if 'filename' in session:
            filename = session['filename']
            if 'effect' in request.form:
                selected_effect = request.form.get('effect')
                input_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                output_image_path = process_image(input_image_path, selected_effect)
                return render_template('upload.html', filename=filename, effects=effects_aggregator.effects.keys(), processed=True)
    return render_template('upload.html', effects=effects_aggregator.effects.keys())

@main.route('/save', methods=['POST'])
def save():
    if 'filename' in session:
        filename = session['filename']
        processed_image_path = os.path.join(current_app.config['PROCESSED_FOLDER'], filename)
        save_path = os.path.join('saved_images', filename)
        if not os.path.exists('saved_images'):
            os.makedirs('saved_images')
        os.rename(processed_image_path, save_path)
        return redirect(url_for('main.upload_file'))
    return redirect(url_for('main.upload_file'))

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)

