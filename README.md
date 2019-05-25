# Fluent Forever Vocab Builder

This is a web app that searches and scrapes info for a vocab word and builds a card for your anki deck, based off the FF model deck.
- Web app because Anki add-ons are not well documented and this separates concerns a bit. Was tkinter but it's not great to work with long-term.

Basically a quick way to do [the vocab step](https://blog.fluent-forever.com/simple-word-flashcards/) step in the FF method.

Decreases card creation time from 6+ minutes to 30 seconds.

Gathers the following info:
- IPA
- Pronunciation recording
- Gender
- Images
- Personal notes

## Rationale

- Because the app is in disarray right now (v1.0.0, April 2019) and review sessions are a pain.
    - Words are repeated over and over, sometimes endlessly
    - Update, May 2019: Bugs are fixed, but I think I like this better anyway.
- I found I like having editable notes that I have full control over.
- App is maybe worth it ($10/mo) for its pre-made content, grammar difficulty levels, and hopes of tutors. But other than that, Anki is much more mature and flexible. 
- We can also use Google Images here over Bing b/c of small scale.

## Requirements

- Python 3
- `pip install -r requirements.txt`
- ffmpeg installed and added to system PATH (for previewing pronunciation audio)
- [Model deck](http://www.fluent-forever.com/wp-content/uploads/2014/05/Model-Deck-May-2014.apkg) from FF imported into Anki
  - This program only creates the "2. Picture Words" note type at the moment
    - Will generate the spelling (optional), production, and comprehension cards automatically
- [AnkiConnect add-on](https://foosoft.net/projects/anki-connect/) (code 2055492159)
- Anki needs to be open before starting the app


## Usage

1. Open Anki
1. For Windows, `set FLASK_APP=ff.py`
    - For Linux/Mac, `export FLASK_APP=ff.py`
1. `flask run`
1. Go to 127.0.0.1:5000 in your browser
1. Select language
   - This is saved in the browser
1. Select destination deck
   - Also saved in the browser
1. Enter word to search
1. Search (takes time to download images)
1. Tweak any values
1. Select pic(s)
1. Enter any notes you want
1. Submit (takes time to store everything into Anki)
1. Repeat

## Known Issues

- Phrases are not supported; currently used for single words that you could find in Wiktionary
  - Can still use program, just no IPA, audio, or definition choices if Wiktionary doesn't have it.

## Todo

- [x] Labels because I'm lost
- [x] Dynamic languages; no French hard-coding
  - See `config.py`
- [x] Config
- [ ] Custom images
  - Ideally drag/drop
- [ ] More recordings from Forvo, maybe
- [x] Better layout, padding
- [x] Less main GUI thread blocking on network requests
  - [ ] ~~And progress bars~~
- [ ] Other note types in the model deck (i.e. grammar, minimal pairs)
