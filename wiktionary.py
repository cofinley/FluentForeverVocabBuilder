import tempfile
from urllib.request import urlopen
import os
import re

from wiktionaryparser import WiktionaryParser

import config as cfg

parser = WiktionaryParser()


def download_audio(url):
    temp_dir = os.path.join(os.getcwd(), cfg.TEMP_DIR)
    data = urlopen(url).read()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".ogg", dir=temp_dir) as f:
        f.write(data)
        return f


def search(query):
    query = parser.fetch(query, cfg.WIKTIONARY_LANGUAGE)[0]
    pronunciation = query["pronunciations"]
    ipa = pronunciation["text"][0].replace("IPA: ", "")
    audio_url = "https:" + pronunciation["audio"][0]
    audio_filename = download_audio(audio_url).name
    definition_choices = query["definitions"]
    formatted_choices = get_formatted_definition_choices(definition_choices)
    return {
        "ipa": ipa,
        "audio_filename": audio_filename,
        "definitions": formatted_choices
    }


def get_formatted_definition_choices(definition_choices):
    choices = []
    for i in definition_choices:
        text = i["text"][0]
        gender_match = re.search(r"(.*)\s(\w)\s\(.*", text)
        if gender_match:
            word = gender_match[1]
            gender_letter = gender_match[2]
            if gender_letter == "m":
                gender = "le "
            else:
                gender = "la "
            result = gender + word
            if word.startswith(("a", "e", "i", "o", "u")):
                result += " -> l'" + word
            choices.append(result)
        else:
            choices.append(text)
    return choices
