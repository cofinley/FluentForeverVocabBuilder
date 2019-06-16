import os
import re
from urllib.parse import unquote
from tempfile import NamedTemporaryFile
from mimetypes import guess_extension
import base64
from typing import List

from PIL import Image
from google_images_download import google_images_download

from app import app

cfg = app.config

cwd = os.getcwd()
save_path_pat = r".*(temp.*)"


def download_images(query: str, page: int) -> List[str]:
    response = google_images_download.googleimagesdownload()

    num_images = cfg["NUM_GOOGLE_IMAGES"]
    end = num_images * (page + 1)
    offset = num_images * page
    if page > 0:
        offset += 1

    paths = response.download({
        "keywords": query,
        "language": cfg["GOOGLE_IMAGES_LANGUAGE"],
        "output_directory": cfg["TEMP_DIR"],
        "limit": end,
        "format": "jpg",
        "offset": offset
    })
    relative_paths = [re.findall(save_path_pat, p)[0].replace(os.sep, '/') for p in paths[0][query] if p]
    return relative_paths


def generate_thumbnail(path: str) -> str:
    filename = os.path.splitext(path)[0]
    ext = os.path.splitext(path)[1]

    thumb_filename = filename + ".thumb" + ext
    thumbnail_img = Image.open(path)
    thumbnail_img.thumbnail(cfg["MAX_IMAGE_SIZE"], Image.ANTIALIAS)
    thumbnail_img.save(thumb_filename, format=thumbnail_img.format)
    return thumb_filename


def format_json_image_path(json_path: str) -> str:
    if json_path.startswith("data:image"):
        absolute_image_path = save_base64_image_data(json_path)
    else:
        image_path_relative_to_temp_dir = re.findall(save_path_pat, json_path)[0]
        unquoted_image_path = unquote(image_path_relative_to_temp_dir)
        absolute_image_path = os.path.join(app.root_path, unquoted_image_path)
    return absolute_image_path


def save_base64_image_data(data_string: str) -> str:
    data_pat = r"data:(image\/.*);base64,(.*)"
    match = re.search(data_pat, data_string)
    if len(match.groups()) > 1:
        ext = guess_extension(match[1])
        data = match[2].encode()
        with NamedTemporaryFile(mode='wb', dir=os.path.join(app.root_path, "temp"), suffix=ext, delete=False) as f:
            f.write(base64.decodebytes(data))
            return f.name
