# OEShare

**Simple. Fast. Secure Sharing.**

Share files and text with anyone using a unique 6-digit code. No account needed. Content auto-deletes after 24 hours.

---

## Features

- 📁 Upload files (PDF, PPT, Excel, JPG, PNG) up to 50MB
- 📝 Share plain text / code snippets
- 🔢 Unique 6-digit numeric codes
- ⏱ Auto-expires after 24 hours
- 📥 Download counter
- 📋 Copy-to-clipboard support
- 📱 Mobile responsive
- 🔒 No sign-up required

---

## Project Structure

```
oeshare/
├── app.py               # Flask application (main entry point)
├── requirements.txt     # Python dependencies
├── oeshare.db           # SQLite database (auto-created on first run)
├── uploads/             # Uploaded files (auto-created)
├── templates/
│   ├── base.html        # Base layout with navbar & footer
│   ├── index.html       # Home page
│   ├── send_file.html   # File upload page
│   ├── send_text.html   # Text sharing page
│   └── receive.html     # Receive / retrieve page
└── static/
    ├── css/
    │   └── style.css    # All styling
    └── js/
        └── main.js      # Drag-drop, clipboard, UI interactions
```

---

## Installation & Setup

### 1. Clone / Download the project

```bash
cd oeshare
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

```
http://localhost:5000
```

---

## How It Works

1. **Send a File** — Upload a file, receive a 6-digit code
2. **Send Text** — Paste text, receive a 6-digit code
3. **Receive** — Enter any 6-digit code to download or view content

All content is automatically deleted after **24 hours**.

---

## Configuration

Edit these values at the top of `app.py`:

| Variable | Default | Description |
|---|---|---|
| `MAX_FILE_SIZE` | 50MB | Maximum upload size |
| `ALLOWED_EXTENSIONS` | pdf, ppt, pptx, xls, xlsx, jpg, jpeg, png | Allowed file types |
| `timedelta(hours=24)` | 24 hours | Expiry time |

---

## Tech Stack

- **Backend**: Python + Flask
- **Database**: SQLite (via Python's built-in `sqlite3`)
- **Frontend**: Plain HTML + CSS + Vanilla JS
- **Storage**: Local filesystem (`/uploads`)
- **Fonts**: DM Sans + DM Mono (Google Fonts)
