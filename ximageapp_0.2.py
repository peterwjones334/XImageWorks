from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
import os
from PIL import Image
import effects_aggregator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROCESSED_FOLDER'] = 'processed/'
app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'jpg', 'png'}
app.secret_key = 'supersecretkey'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(input_image_path)
                
                # Save original filename in session
                session['filename'] = filename
                
                return render_template('upload.html', filename=filename, effects=effects_aggregator.effects.keys())

        if 'filename' in session:
            filename = session['filename']
            if 'effect' in request.form:
                selected_effect = request.form.get('effect')
                input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Process the image
                image = Image.open(input_image_path)
                
                if selected_effect in effects_aggregator.effects:
                    image = effects_aggregator.effects[selected_effect](image)
                
                output_image_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
                image.save(output_image_path)
                return render_template('upload.html', filename=filename, effects=effects_aggregator.effects.keys(), processed=True)

    return render_template('upload.html', effects=effects_aggregator.effects.keys())

@app.route('/save', methods=['POST'])
def save():
    if 'filename' in session:
        filename = session['filename']
        processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        save_path = os.path.join('saved_images', filename)
        if not os.path.exists('saved_images'):
            os.makedirs('saved_images')
        os.rename(processed_image_path, save_path)
        return redirect(url_for('upload_file'))
    return redirect(url_for('upload_file'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)


