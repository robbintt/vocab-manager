# Vocab Manager

A vocabulary manager that hooks into Anki flashcards and web resources.

Web resources automatically generate card definitions.


## Issues

- not sure about `ij` and any other special character usage: https://en.wikipedia.org/wiki/Dutch_orthography


## MVP

Given a `Vocab Item`, `Vocab Type`, and `Language Usage Source`.

Generate an anki flash card for the `Vocab Item`


### MVP Concessions

- Lets hardcode the `Vocab Type` to whatever interglot accepts.
  - Interglot provides google and bing machine translations...
  - Interglot search URL example: `https://www.interglot.com/dictionary/nl/en/search?q=op+het+strand&m=`

- For now, try out the interglot definition and store for private use.
  - beautiful soup 4 to grab the right section, then output a text format dump
  - In the future, just parse the whole `.dict.dz` format lexicon from freedict.org and contribute back to that...


### Nederlands Language Resources

Remember the concept of `headwords` or root words.  Headwords must be mapped onto derivatives like plurals or conjugations (is there a name for these derivatives?)

Ideally there is a tool I can draw from and contribute back to. FreeDict might be a good tool.

- FreeDict: free dictionary files
  - Actively maintained on github: https://github.com/freedict/fd-dictionaries
  - All dictionaries are encoded in TEI (version 5) which is a flexible XML format to encode human speech.
    - How can the ANKI card also have an attached computer generated speech?
    - Can I recruit Nederlanders to also pronounce words and contribute them?
  - TEI XML format
    - `nl->en`: 22747 headwords
    - `en->nl`: 7714 headwords
  - https://freedict.org/
  - metadata API: https://freedict.org/freedict-database.json
    - Good way to check for dict updates
    - This project is slow and I would probably be the only person updating these two dictionaries
    - While it would be nice to have a round trip contribution and update method, it's out of scope right now

- Interglot
  - Seems great, how to query?
- Google Translate Output
  - Free < 500k characters (assume per month?)
  - GCP API: https://cloud.google.com/translate/docs/intro-to-v3



### Vocab Items, Vocab Types & Language Usage Sources

A vocab item is any coherent definable composition of letters/sounds. It isn't limited to one word or one line.

Vocab items require multiline fields. Anki supports this.

Vocab types are Words, phrases, sentences, compositions.


#### Language Usage Sources

- Conversations on Nederlands language subreddits
  - `/r/TheNetherlands`
  - `/r/utrecht`
- Kindle books
- Nederlands Language Movies & TV
- Existing anki flashcards
- [OPUS: a growing collection of translated texts from the web](http://opus.nlpl.eu/)
  - i think `nl <> en` has a bunch of words and phrases that I can use as sources.
    - It's a bidirectional map so `en <> nl` provided the same results (i only spot checked).


### Future Proofing

Since our mvp is nederlands language definitions, lets add a `nl` tag on every card as a hook for later remapping.


### Web Resource Mapping

Should we map resources at the deck, tag, or card level?

- A mapping of web resources per flash card allows for maximum flexibility in deck composition.
  - Any change to the card will cause the card to be regenerated. So I guess we want card versioning.

A mapping of web resources per tag means we need to batch update if the resource<>tag mapping is updated.


### Card Format

Cards should use templates for sure.  We want multiple templates per deck, so the template should be based on the tag. But now we run into tag precedence issues.

We want to version cards, and also may want to update the card templates over time, so 


### Technologies

- DynamoDB, AWS Lambda, Zappa, Flask, flask-dynamo


## Initial Use Case

Record dutch language words easily and quickly from a variety of devices.


## Features

- Tag individual cards with multiple tags
  - use some id system per card
- Automatically generate an anki flashcard
- Update (or replace) an existing anki flashcard set
  - Need to determine how this works so I don't lose my set progress
- Select a word from a phrase and preview a card for that word, inheriting from the phrase.
  - If exists, show the card.
  - If not exists, offer a button to create the card.
  - Is there any reason to actually join a phrase to its decomposed cards? Might not be useful.


## Anki Deck Questions

- How does an anki deck store my progress?
- Can I insert a single card into an anki deck?
- How is an anki deck managed? Is it a simple format to work with?
- Can I use automation to perform operations on my anki dutch decks with a tagging system?
  - move cards between decks
  - deduplicate cards or run an identify duplicates function - complex
    - mvp feature is probably just a mapping of duplicate clusters between N decks
  - tag cards
  - reassign all cards in a tag group to a specific deck
  - update the decks on ankiweb
  - backup the decks automatically that exist on ankiweb today
    - some cron based operation, i could use a lambda cron with Zappa
