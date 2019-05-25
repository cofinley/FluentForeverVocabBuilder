import os
import re
from urllib.parse import unquote
import json

from PIL import Image
from google_images_download import google_images_download

from app import app
cfg = app.config

cwd = os.getcwd()
save_path_pat = r".*(temp.*)"


def download_images(query):
    response = google_images_download.googleimagesdownload()  # class instantiation

    paths = response.download({
        "keywords": query,
        "language": cfg["GOOGLE_IMAGES_LANGUAGE"],
        "output_directory": cfg["TEMP_DIR"],
        "limit": cfg["NUM_GOOGLE_IMAGES"],
        "format": "jpg"
    })
    relative_paths = [re.findall(save_path_pat, p)[0].replace(os.sep, '/') for p in paths[query] if p]
    return relative_paths


def generate_thumbnail(path):
    filename = os.path.splitext(path)[0]
    ext = os.path.splitext(path)[1]

    thumb_filename = filename + ".thumb" + ext
    thumbnail_img = Image.open(path)
    thumbnail_img.thumbnail(cfg["MAX_IMAGE_SIZE"], Image.ANTIALIAS)
    thumbnail_img.save(thumb_filename, format=thumbnail_img.format)
    return thumb_filename


def format_json_image_paths(json_paths):
    parsed_json_paths = json.loads(json_paths)
    image_paths_relative_to_temp_dir = [re.findall(save_path_pat, p)[0] for p in parsed_json_paths]
    unquoted_image_paths = [unquote(p) for p in image_paths_relative_to_temp_dir]
    absolute_image_paths = [os.path.join(app.root_path, p) for p in unquoted_image_paths]
    return absolute_image_paths
