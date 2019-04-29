import base64
import os
import html

import requests

import config as cfg


class AnkiConnect:
    URL = "http://localhost:8765/"
    VERSION = 6

    def invoke(self, action, params=None):
        payload = {"action": action, "version": self.VERSION}
        if params:
            payload["params"] = params
        response = requests.request("POST", self.URL, json=payload).json()
        if len(response) != 2:
            raise Exception("response has an unexpected number of fields")
        if "error" not in response:
            raise Exception("response is missing required error field")
        if "result" not in response:
            raise Exception("response is missing required result field")
        if response["error"] is not None:
            raise Exception(response["error"])
        return response["result"]

    def get_deck_names(self):
        return self.invoke("deckNames")

    def store_media_file(self, src_file_path, word):
        action = "storeMediaFile"
        sanitized_word = "".join([c for c in word if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
        ext = os.path.splitext(src_file_path)[1]
        dst = "{}{}".format(sanitized_word, ext)

        with open(src_file_path, 'rb') as f:
            b64_output = base64.b64encode(f.read()).decode('utf-8')
        params = {
            "filename": dst,
            "data": b64_output
        }

        self.invoke(action, params)
        return dst

    @staticmethod
    def format_notes(notes):
        html_notes = "<br>".join(html.escape(notes.strip()).split("\n"))
        return "<div>{}</div>".format(html_notes)

    def add_note(self, deck_name, word, image_paths, gender, notes, recording_file_path, ipa_text, test_spelling):
        stored_images = []
        for i, image_path in enumerate(image_paths):
            stored_images.append(self.store_media_file(image_path, "{}-{}".format(word, i)))

        picture_field = ""
        for stored_image in stored_images:
            picture_field += '<img src="{}">'.format(stored_image)

        escaped_gender_text = html.escape(gender)
        formatted_notes = self.format_notes(notes)
        gender_notes_field = escaped_gender_text + formatted_notes

        stored_audio_filename = self.store_media_file(recording_file_path, word)

        pronunciation_field = ipa_text + "[sound:{}]".format(stored_audio_filename)

        test_spelling = 'y' if test_spelling else ''

        params = {
            "note": {
                "deckName": deck_name,
                "modelName": cfg.SIMPLE_WORDS_NOTE_TYPE,
                "fields": {
                    "Word": word,
                    "Picture": picture_field,
                    "Gender, Personal Connection, Extra Info (Back side)": gender_notes_field,
                    "Pronunciation (Recording and/or IPA)": pronunciation_field,
                    "Test Spelling? (y = yes, blank = no)": test_spelling
                },
                "tags": []
            }
        }

        note_id = self.invoke("addNote", params)
        return note_id
