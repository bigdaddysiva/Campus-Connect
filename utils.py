import os
from datetime import datetime

def save_uploaded_file(file, upload_dir='uploads'):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    filepath = os.path.join(upload_dir, file.filename)
    file.save(filepath)
    return filepath, datetime.now().isoformat()