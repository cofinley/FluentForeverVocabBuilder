import os
from tkinter import *
from tkinter.ttk import *

from pydub import AudioSegment
from playsound import playsound

import gallery
import wiktionary
from anki_connect import AnkiConnect

TEMP_DIR = "temp"

root = Tk()

cwd = os.getcwd()

ac = AnkiConnect()


class Application(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        remove_temp_files()
        setup_temp_dir()
        self.parent = parent
        self.create_widgets()

    def create_deck_names_combo(self):
        self.deck_name_decision = StringVar()
        self.deck_names = ac.get_deck_names()
        self.deck_names_combo = Combobox(self, textvariable=self.deck_name_decision, values=self.deck_names)
        self.deck_names_combo.pack()

    def create_query_entry(self):
        self.query = StringVar()
        self.query_entry = Entry(self.parent, textvariable=self.query, name="search", text="Word:")
        self.query_entry.pack()

    def create_search_button(self):
        self.search_button = Button(self)
        self.search_button["text"] = "Search"
        self.search_button["command"] = self.search
        self.search_button.pack(side="top")
        self.reset_button = Button(self, text="Reset", command=self.reset, name="reset")
        self.reset_button.pack()

    def reset(self):
        keep = [
            self.reset_button,
            self.search_button,
            self.query_entry,
            self.deck_names_combo
        ]
        for widget in self.winfo_children():
            if widget not in keep:
                widget.destroy()
        self.query.set("")

    def create_widgets(self):
        self.create_deck_names_combo()
        self.create_query_entry()
        self.create_search_button()

    def play_pronunciation(self):
        ogg_version = AudioSegment.from_ogg(self.audio_filename)
        wav_filename = self.audio_filename.replace(".ogg", ".wav")
        if not os.path.exists(wav_filename):
            ogg_version.export(wav_filename, format="wav")
        playsound(wav_filename)

    def create_search_result_widgets(self, query, search_result):
        self.ipa_text = search_result["ipa"]
        self.create_ipa_label()
        self.create_definition_choices_combo(search_result["definitions"])

        self.audio_filename = search_result["audio_filename"]
        self.sound_button = Button(self, text="Play Pronunciation", command=self.play_pronunciation).pack()

        self.create_image_gallery(query)
        self.create_notes_area()
        self.create_test_spelling_checkbox()
        self.create_submit_button()

    def create_ipa_label(self):
        self.ipa_label = Label(self, text="IPA:").pack()
        ipa_text_var = StringVar(value=self.ipa_text)
        self.ipa_field = Entry(self, textvariable=ipa_text_var).pack()

    def create_definition_choices_combo(self, choices):
        self.definition_decision = StringVar()
        self.definition_combo = Combobox(self, textvariable=self.definition_decision, values=choices)
        self.definition_combo.set(choices[0])
        self.definition_combo.pack()

    def create_image_gallery(self, query):
        self.gallery = gallery.Gallery(self, query)

    def create_test_spelling_checkbox(self):
        self.test_spelling = BooleanVar()
        self.test_spelling_cb = Checkbutton(self, text="Test Spelling?", variable=self.test_spelling)
        self.test_spelling.set(False)
        self.test_spelling_cb.pack()

    def search(self):
        if hasattr(self, "result_label"):
            self.result_label.destroy()
        query = self.query_entry.get()
        self.search_progress_bar = Progressbar(self, orient=HORIZONTAL, mode="indeterminate")
        self.search_progress_bar.pack()
        self.search_progress_bar.start()
        search_result = wiktionary.search(query)
        self.create_search_result_widgets(query, search_result)
        self.search_progress_bar.stop()
        self.after(500, self.search_progress_bar.destroy)

    def create_submit_button(self):
        self.submit_button = Button(self, text="Submit", command=self.submit).pack()

    def submit(self):
        self.submit_progress_bar = Progressbar(self, orient=HORIZONTAL, mode="indeterminate")
        self.submit_progress_bar.pack()
        self.submit_progress_bar.start()
        word = self.query_entry.get()
        deck_name = self.deck_name_decision.get()
        selected_images = self.gallery.get_selected()
        gender = self.definition_decision.get()
        notes = self.notes.get("1.0", END)
        test_spelling = self.test_spelling.get()
        result = ac.add_note(deck_name, word, selected_images, gender, notes, self.audio_filename, self.ipa_text, test_spelling)
        self.submit_progress_bar.stop()
        self.after(200, self.submit_progress_bar.destroy)
        if result:
            self.reset()
            self.result_label = Label(self, text="Added!")
            self.result_label.pack()

    def create_notes_area(self):
        self.notes = Text(self, height=2, width= 60)
        self.notes.pack()


def setup_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(os.path.join(os.getcwd(), TEMP_DIR))


def remove_temp_files():
    for r, dirs, files in os.walk(os.path.join(cwd, TEMP_DIR), topdown=False):
        for name in files:
            os.remove(os.path.join(r, name))
        for name in dirs:
            os.rmdir(os.path.join(r, name))


def on_close():
    quit()


def run():
    app = Application(parent=root).pack(side="top", fill="both", expand=True)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
