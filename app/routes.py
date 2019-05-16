from flask import render_template

from app import app, anki_connect


ac = anki_connect.AnkiConnect()


@app.route('/')
@app.route('/index')
def index():
    decks = ac.get_deck_names()
    return render_template("index.html", decks=decks)
