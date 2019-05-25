import os


class Config(object):
    SECRET_KEY = "fluent-forever"
    GOOGLE_IMAGES_LANGUAGE = "French"
    WIKTIONARY_LANGUAGE = "french"
    NUM_GOOGLE_IMAGES = 5
    TEMP_DIR = os.path.join(os.getcwd(), "app", "temp")
    MAX_IMAGE_SIZE = (400, 400)
    SIMPLE_WORDS_NOTE_TYPE = "2. Picture Words"
    AVAILABLE_LANGUAGES = [
        "Arabic",
        "Chinese",
        "Czech",
        "Danish",
        "Dutch",
        "English",
        "Estonian",
        "Finnish",
        "French",
        "German",
        "Greek",
        "Hebrew",
        "Hungarian",
        "Icelandic",
        "Italian",
        "Japanese",
        "Korean",
        "Latvian",
        "Lithuanian",
        "Norwegian",
        "Portuguese",
        "Polish",
        "Romanian",
        "Russian",
        "Spanish",
        "Swedish",
        "Turkish"
    ]
