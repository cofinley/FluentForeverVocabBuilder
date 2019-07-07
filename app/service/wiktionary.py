import tempfile
from urllib.request import urlopen
import os

from wiktionaryparser import WiktionaryParser

from app import app

cfg = app.config

parser = WiktionaryParser()


def download_audio(url):
    temp_dir = os.path.join(os.getcwd(), cfg["TEMP_DIR"])
    data = urlopen(url).read()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".ogg", dir=temp_dir) as f:
        f.write(data)
        return f


def search(query, language):
    parser.set_default_language(language)
    query = parser.fetch(query)[0]
    pronunciation = query["pronunciations"]
    if len(pronunciation["text"]):
        ipa = pronunciation["text"][0].replace("IPA: ", "")
    else:
        ipa = ""
    if len(pronunciation["audio"]):
        audio_url = "https:" + pronunciation["audio"][0]
        audio_filename = download_audio(audio_url).name
    else:
        audio_filename = ""
    definition_choices = [(d["partOfSpeech"], d["text"][0]) for d in query["definitions"]]
    return {
        "ipa": ipa,
        "audio_filename": audio_filename,
        "definitions": definition_choices
    }
