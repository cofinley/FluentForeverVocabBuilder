import os

from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

from app import routes

cfg = app.config


def setup_temp_dir():
    if not os.path.exists(cfg["TEMP_DIR"]):
        os.makedirs(os.path.join(os.getcwd(), cfg["TEMP_DIR"]))


def remove_temp_files():
    for r, dirs, files in os.walk(os.path.join(os.getcwd(), cfg["TEMP_DIR"]), topdown=False):
        for name in files:
            os.remove(os.path.join(r, name))
        for name in dirs:
            os.rmdir(os.path.join(r, name))


remove_temp_files()
setup_temp_dir()


import logging
logging.basicConfig(format='%(levelname)-7s %(relativeCreated)9dms: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)  # module fully-qualified name
debug = logger.debug   # debug('xx %s', v)
info = logger.info
error = logger.error