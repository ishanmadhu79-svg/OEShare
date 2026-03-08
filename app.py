import os
import random
import string
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'oeshare-secret-key-2024'

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATABASE = os.path.join(BASE_DIR, 'oeshare.db')
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─── Database ──────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                content TEXT,
                file_path TEXT,
                original_name TEXT,
                download_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        db.commit()


def generate_code():
    """Generate a unique 6-digit code."""
    with get_db() as db:
        for _ in range(100):
            code = ''.join(random.choices(string.digits, k=6))
            existing = db.execute('SELECT id FROM shares WHERE code = ?', (code,)).fetchone()
            if not existing:
                return code
    raise Exception("Could not generate unique code")


def cleanup_expired():
    """Delete expired shares and their files."""
    with get_db() as db:
        expired = db.execute(
            'SELECT * FROM shares WHERE expires_at < ?', (datetime.now(),)
        ).fetchall()
        for row in expired:
            if row['file_path'] and os.path.exists(row['file_path']):
                os.remove(row['file_path'])
        db.execute('DELETE FROM shares WHERE expires_at < ?', (datetime.now(),))
        db.commit()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    cleanup_expired()
    return render_template('index.html')


@app.route('/send/file', methods=['GET', 'POST'])
def send_file_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('File type not allowed. Please upload PDF, PPT, Excel, JPG, or PNG.', 'error')
            return redirect(request.url)

        code = generate_code()
        ext = file.filename.rsplit('.', 1)[1].lower()
        original_name = secure_filename(file.filename)
        new_filename = f"{code}.{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)

        expires_at = datetime.now() + timedelta(hours=24)

        with get_db() as db:
            db.execute(
                'INSERT INTO shares (code, type, file_path, original_name, expires_at) VALUES (?, ?, ?, ?, ?)',
                (code, 'file', file_path, original_name, expires_at)
            )
            db.commit()

        return render_template('send_file.html', code=code, success=True, filename=original_name)

    return render_template('send_file.html')


@app.route('/send/text', methods=['GET', 'POST'])
def send_text():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if not text:
            flash('Please enter some text to share.', 'error')
            return redirect(request.url)

        if len(text) > 100000:
            flash('Text is too long (max 100,000 characters).', 'error')
            return redirect(request.url)

        code = generate_code()
        expires_at = datetime.now() + timedelta(hours=24)

        with get_db() as db:
            db.execute(
                'INSERT INTO shares (code, type, content, expires_at) VALUES (?, ?, ?, ?)',
                (code, 'text', text, expires_at)
            )
            db.commit()

        return render_template('send_text.html', code=code, success=True)

    return render_template('send_text.html')


@app.route('/receive', methods=['GET', 'POST'])
def receive():
    result = None
    error = None

    if request.method == 'POST':
        code = request.form.get('code', '').strip()

        if not code.isdigit() or len(code) != 6:
            error = 'Please enter a valid 6-digit code.'
        else:
            with get_db() as db:
                row = db.execute(
                    'SELECT * FROM shares WHERE code = ? AND expires_at > ?',
                    (code, datetime.now())
                ).fetchone()

                if row:
                    result = dict(row)
                    # Increment download count
                    db.execute('UPDATE shares SET download_count = download_count + 1 WHERE code = ?', (code,))
                    db.commit()
                else:
                    error = 'No content found for this code. It may have expired or never existed.'

    return render_template('receive.html', result=result, error=error)


@app.route('/download/<code>')
def download(code):
    with get_db() as db:
        row = db.execute(
            'SELECT * FROM shares WHERE code = ? AND type = ? AND expires_at > ?',
            (code, 'file', datetime.now())
        ).fetchone()

    if not row:
        flash('File not found or has expired.', 'error')
        return redirect(url_for('receive'))

    file_path = row['file_path']
    original_name = row['original_name'] or os.path.basename(file_path)

    if not os.path.exists(file_path):
        flash('File no longer exists on the server.', 'error')
        return redirect(url_for('receive'))

    return send_file(file_path, as_attachment=True, download_name=original_name)


@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 50MB.', 'error')
    return redirect(url_for('send_file_page'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
