import os
import secrets
from PIL import Image
from flask import url_for, current_app

def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(picture.filename)
    filename = random_hex + extension
    path = os.path.join(current_app.root_path, 'static/profile_pics', filename)
    picture.save(path)
    return filename
