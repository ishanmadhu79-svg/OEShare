// ─── Copy to Clipboard ───────────────────────────────────────────────────────

function copyCode(code) {
    navigator.clipboard.writeText(code).then(() => {
        const btn = document.querySelector('.copy-btn');
        if (btn) {
            const orig = btn.textContent;
            btn.textContent = 'Copied!';
            btn.style.background = '#16a34a';
            setTimeout(() => {
                btn.textContent = orig;
                btn.style.background = '';
            }, 2000);
        }
    });
}

function copyText() {
    const el = document.getElementById('textContent');
    if (!el) return;
    navigator.clipboard.writeText(el.textContent).then(() => {
        const btn = document.querySelector('.copy-btn-sm');
        if (btn) {
            const orig = btn.textContent;
            btn.textContent = '✓ Copied!';
            setTimeout(() => btn.textContent = orig, 2000);
        }
    });
}

// ─── Character Counter ────────────────────────────────────────────────────────

function updateCount(el) {
    const counter = document.getElementById('charCount');
    if (counter) counter.textContent = el.value.length.toLocaleString();
}

// ─── File Upload Handling ─────────────────────────────────────────────────────

function handleFileSelect(input) {
    const file = input.files[0];
    if (!file) return;
    showPreview(file);
}

function showPreview(file) {
    const preview = document.getElementById('filePreview');
    const nameEl = document.getElementById('previewName');
    const sizeEl = document.getElementById('previewSize');
    const iconEl = document.getElementById('previewIcon');
    const submitBtn = document.getElementById('submitBtn');
    const dropZone = document.getElementById('dropZone');

    if (!preview) return;

    const ext = file.name.split('.').pop().toLowerCase();
    const icons = { pdf: '📕', ppt: '📊', pptx: '📊', xls: '📗', xlsx: '📗', jpg: '🖼️', jpeg: '🖼️', png: '🖼️' };
    iconEl.textContent = icons[ext] || '📄';

    nameEl.textContent = file.name;
    sizeEl.textContent = formatSize(file.size);

    dropZone.style.display = 'none';
    preview.style.display = 'block';
    if (submitBtn) submitBtn.disabled = false;
}

function removeFile() {
    const input = document.getElementById('fileInput');
    const preview = document.getElementById('filePreview');
    const submitBtn = document.getElementById('submitBtn');
    const dropZone = document.getElementById('dropZone');

    if (input) input.value = '';
    if (preview) preview.style.display = 'none';
    if (submitBtn) submitBtn.disabled = true;
    if (dropZone) dropZone.style.display = 'block';
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// ─── Drag & Drop ──────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    if (!dropZone || !fileInput) return;

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (!file) return;

        const allowed = ['pdf', 'ppt', 'pptx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'];
        const ext = file.name.split('.').pop().toLowerCase();

        if (!allowed.includes(ext)) {
            alert('File type not allowed. Please upload PDF, PPT, Excel, JPG, or PNG.');
            return;
        }

        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;

        showPreview(file);
    });

    dropZone.addEventListener('click', () => fileInput.click());
});

// ─── Code Input Auto-Format ────────────────────────────────────────────────── 

document.addEventListener('DOMContentLoaded', () => {
    const codeInput = document.getElementById('codeInput');
    if (!codeInput) return;

    codeInput.addEventListener('paste', (e) => {
        setTimeout(() => {
            codeInput.value = codeInput.value.replace(/\D/g, '').slice(0, 6);
        }, 0);
    });
});
