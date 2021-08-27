# Fluent Forever Vocab Builder

[Video demo](https://raw.githubusercontent.com/cofinley/FluentForeverVocabBuilder/master/demo.webm)

This is a web app that searches and scrapes info for a vocab word and builds a card for your anki deck, based off the FF model deck.
- Web app because Anki add-ons are not well documented and this separates concerns a bit. Was tkinter but it's not great to work with long-term.

Basically a quick way to do [the vocab step](https://blog.fluent-forever.com/simple-word-flashcards/) step in the FF method.

Decreases card creation time from 6+ minutes to 30 seconds.

Gathers the following info:
- IPA (Wiktionary)
- Pronunciation recording (Wiktionary)
- Gender/Word Usage (Wiktionary)
- Images (Google)
    - Resized automatically to reduce AnkiWeb sync time
- Personal notes (you)

## Rationale

- Because the app is in disarray right now (v1.0.0, April 2019) and review sessions are a pain.
    - Words are repeated over and over, sometimes endlessly
    - Update, May 2019: Bugs are fixed, but I think I like this better anyway.
- I found I like having editable notes that I have full control over.
- App is maybe worth it ($10/mo) for its pre-made content, grammar difficulty levels, and hopes of tutors. But other than that, Anki is much more mature and flexible. 
- We can also use Google Images here over Bing b/c of small scale.

## Requirements

- Python 3
- ffmpeg installed and added to system PATH (for previewing pronunciation audio)
- [Model deck](http://www.fluent-forever.com/wp-content/uploads/2014/05/Model-Deck-May-2014.apkg) from FF imported into Anki
  - This program only creates the "2. Picture Words" note type at the moment
    - Will generate the spelling (optional), production, and comprehension cards automatically
- [AnkiConnect add-on](https://foosoft.net/projects/anki-connect/) (code 2055492159)
- Anki needs to be open before starting the app

## Installation

- `git clone https://github.com/cofinley/FluentForeverVocabBuilder.git`
- Go into the project's directory
- `python3 -m venv venv`
  - Python 3
- `venv\Scripts\activate`
  - on Linux/Mac  `source venv/bin/activate`
- `pip3 install --upgrade wheel pip`
- `pip3 install -r requirements.txt`


## Usage

1. Open Anki in the background
1. Go into project's directory
1. Click on (or run in command line) the start program for your OS
   - `start.bat` for Windows
   - `start.sh` for Linux/Mac
      - Might have to run `chmod +x ./start.sh` if it's not executable
1. Go to [127.0.0.1:5000](127.0.0.1:5000) in your browser
1. Select language
   - This is saved for the next session
1. Select destination deck
   - Also saved
1. Enter word to search
1. Search (takes time to download images)
1. Tweak any values
1. Select pic(s)
   - You can paste images from your clipboard into the selected images area with Ctrl+V
   - You can also drag files in to the area
1. Enter any notes you want
1. Submit (takes time to store everything into Anki)
1. Repeat

## Updating

- Go to the installation directory for the project
- `git pull`
- `pip3 install -r requirements.txt`

## Development

`pip3 install pip-tools`

Specify major (not exact) package versions in file `requirements.in` then compile `requirements.txt` from it.
`pip-compile requirements.in`

`requirements.txt` holds exact versions

## Known Issues

- Phrases are not supported; currently used for single words that you could find in Wiktionary
  - Can still use program, just no IPA, audio, or definition choices if Wiktionary doesn't have it.

## Todo

- [ ] Easier installation and startup
    - Batch/bash files created, a whole installer would be nice
- [ ] More recordings from Forvo, maybe
- [ ] Other note types in the model deck (i.e. grammar, minimal pairs)


Image was not working
see https://github.com/hardikvasa/google-images-download/pull/298
solutions:
- now, see `requirements.in` (may need to update from time to time)
- maybe try fix it by using https://github.com/RiddlerQ/simple_image_download  
