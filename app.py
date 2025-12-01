from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import uuid
from io import BytesIO
from qr_generator import generate_qr_code

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for logo uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        data = request.form.get('data')
        if not data:
            flash('Please enter data for the QR code', 'error')
            return redirect(url_for('index'))
        
        # Handle file upload
        logo_path = None
        if 'logo' in request.files:
            file = request.files['logo']
            if file.filename != '' and allowed_file(file.filename):
                filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(logo_path)
        
        # Generate unique filename
        output_file = f"qrcode_{uuid.uuid4()}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file)
        
        # Generate QR code
        generate_qr_code(
            data=data,
            output_file=output_path,
            style=request.form.get('style', 'default'),
            fill_color=request.form.get('fill_color', '#000000'),
            back_color=request.form.get('back_color', '#FFFFFF'),
            logo_path=logo_path,
            size=(
                int(request.form.get('width', 300)),
                int(request.form.get('height', 300))
            ) if request.form.get('width') and request.form.get('height') else (None, None)
        )
        
        return render_template('result.html', qr_code=output_file)
    
    except Exception as e:
        app.logger.error(f"Error generating QR code: {str(e)}")
        flash(f'Error generating QR code: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        as_attachment=True,
        download_name=f"qrcode_{filename}"
    )

if __name__ == '__main__':
    app.run(debug=True)
