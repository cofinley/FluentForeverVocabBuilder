import os
import tkinter as tk
from tkinter import ttk

from pydub import AudioSegment
from playsound import playsound

import gallery
import wiktionary
from anki_connect import AnkiConnect
import config as cfg

root = tk.Tk()

cwd = os.getcwd()

ac = AnkiConnect()


class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        remove_temp_files()
        setup_temp_dir()
        self.parent = parent
        self.create_widgets()

    def create_deck_names_combo(self):
        self.deck_name_decision = tk.StringVar()
        self.deck_names = ac.get_deck_names()
        self.deck_names_combo = ttk.Combobox(self, textvariable=self.deck_name_decision, values=self.deck_names)
        self.deck_names_combo.pack()

    def create_query_entry(self):
        self.query = tk.StringVar()
        self.query_entry = ttk.Entry(self.parent, textvariable=self.query, name="search", text="Word:")
        self.query_entry.pack()

    def create_search_button(self):
        self.search_button = ttk.Button(self)
        self.search_button["text"] = "Search"
        self.search_button["command"] = self.search
        self.search_button.pack(side="top")
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset, name="reset")
        self.reset_button.pack()

    def reset(self):
        widgets_to_keep = [
            self.reset_button,
            self.search_button,
            self.query_entry,
            self.deck_names_combo
        ]
        for widget in self.winfo_children():
            if widget not in widgets_to_keep:
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
        self.sound_button = ttk.Button(self, text="Play Pronunciation", command=self.play_pronunciation).pack()

        self.create_image_gallery(query)
        self.create_notes_area()
        self.create_test_spelling_checkbox()
        self.create_submit_button()

    def create_ipa_label(self):
        self.ipa_label = ttk.Label(self, text="IPA:")
        self.ipa_label.pack()
        self.ipa_text_var = tk.StringVar()
        self.ipa_field = ttk.Entry(self, textvariable=self.ipa_text_var)
        self.ipa_text_var.set(self.ipa_text)
        self.ipa_field.pack()

    def create_definition_choices_combo(self, choices):
        self.definition_decision = tk.StringVar()
        self.definition_combo = ttk.Combobox(self, textvariable=self.definition_decision, values=choices)
        self.definition_combo.set(choices[0])
        self.definition_combo.pack()

    def create_image_gallery(self, query):
        self.gallery = gallery.Gallery(self, query)

    def create_test_spelling_checkbox(self):
        self.test_spelling = tk.BooleanVar()
        self.test_spelling_cb = ttk.Checkbutton(self, text="Test Spelling?", variable=self.test_spelling)
        self.test_spelling.set(False)
        self.test_spelling_cb.pack()

    def search(self):
        if hasattr(self, "result_label"):
            self.result_label.destroy()
        query = self.query_entry.get()
        search_result = wiktionary.search(query)
        self.create_search_result_widgets(query, search_result)

    def create_submit_button(self):
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit).pack()

    def submit(self):
        word = self.query_entry.get()
        deck_name = self.deck_name_decision.get()
        selected_images = self.gallery.get_selected()
        gender = self.definition_decision.get()
        notes = self.notes.get("1.0", tk.END)
        test_spelling = self.test_spelling.get()
        result = ac.add_note(deck_name, word, selected_images, gender, notes, self.audio_filename, self.ipa_text, test_spelling)
        if result:
            self.reset()
            self.result_label = tk.Label(self, text="Added!")
            self.result_label.pack()

    def create_notes_area(self):
        self.notes = tk.Text(self, height=2, width=30)
        self.notes.pack()


def setup_temp_dir():
    if not os.path.exists(cfg.TEMP_DIR):
        os.makedirs(os.path.join(os.getcwd(), cfg.TEMP_DIR))


def remove_temp_files():
    for r, dirs, files in os.walk(os.path.join(cwd, cfg.TEMP_DIR), topdown=False):
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
