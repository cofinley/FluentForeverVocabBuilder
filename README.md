# Fluent Forever Vocab Builder

This is a tkinter program that searches and scrapes info for a vocab word and builds a card for your anki deck, based off the FF model deck.
- Tkinter because Anki add-ons are not well documented and this separates concerns a bit.

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
    - Occurs on review, repeats words over and over
- I found I like having editable notes that I have full control over.
- App is still worth it ($10/mo) with content, grammar difficulty levels, and hopes of tutors, but other than that, Anki is much more mature. 
- We can also use Google Images here over Bing b/c of small scale.

## Requirements

- `pip install -r requirements.txt`
- ffmpeg installed and added to system PATH
- [Model deck](http://www.fluent-forever.com/wp-content/uploads/2014/05/Model-Deck-May-2014.apkg) from FF imported into Anki
  - This program only creates the "2. Picture Words" note type at the moment
    - Will generate the spelling (optional), production, and comprehension cards automatically
- [AnkiConnect add-on](https://foosoft.net/projects/anki-connect/) (code 2055492159)
- Anki needs to be open


## Usage

1. `python app.py`
2. Enter word to search
3. Select destination deck
4. Search
5. Tweak any values
6. Select pic(s)
7. Enter any notes you want
8. Submit
9. Repeat

## Todo

- Dynamic languages; no French hard-coding
- Custom images
  - Ideally drag/drop
- More recordings from Forvo, maybe
- Better layout, padding
- Less main GUI thread blocking on network requests
  - And progress bars
- Config
- Other note types in the model deck (i.e. grammar)
