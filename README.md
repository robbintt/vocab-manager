# Vocab Manager

A vocabulary manager that hooks into Anki flashcards and web resources.

Web resources automatically generate card definitions.


## Issues

- not sure about `ij` and any other special character usage: https://en.wikipedia.org/wiki/Dutch_orthography

- Anki stuff is pretty complicated, is there a quick import feature to add a card to a deck? 
- I can easily copy/paste from browser to anki mobile...
- Or maybe I can go from browser to other browser, if ankiweb allows adding a card...


## [Anki Manual](https://apps.ankiweb.net/docs/manual.html)


#### Anki Extensions

Anki is a free Python application - don't think of anki in terms of an API. 

Ankiweb is convenient, but needs to be accessed from a local application. You're supposed to use the sync for personal use.


#### Using Anki Sync

Ideally I can just add a card to a deck, then run a sync against ankiweb.

- docs: "the database": https://apps.ankiweb.net/docs/addons.html#the-database
- anki source code: https://github.com/dae/
  - anki sync source code: https://github.com/dae/anki/blob/master/anki/sync.py
    - mergemodels: https://github.com/dae/anki/blob/master/anki/sync.py#L328
    - mergedecks: https://github.com/dae/anki/blob/master/anki/sync.py#L348
    - mergetags:  https://github.com/dae/anki/blob/master/anki/sync.py#L379
    - mergerevlog: https://github.com/dae/anki/blob/master/anki/sync.py#L385
    - mergecards: https://github.com/dae/anki/blob/master/anki/sync.py#L404
    - mergenotes: https://github.com/dae/anki/blob/master/anki/sync.py#L410
- https://apps.ankiweb.net/docs/addons.html
- What data exactly does sync update? 
  - anki has a sqlite database, how exactly does an anki sync work?
- I want to use sync to essentially push new cards to ankiweb from my flask app
  - Also want to update cards without losing memorization data.
- Possible to build anki for linux... can I build it in my lambda and import it into Python? Then my flask app can sync...
  - yes can be built from source, lets give it a whirl, bring it into our flask app
  - maybe too many dependencies, i just need to be able to populate cards and do a "additive-only sync" of a new card + whatever associated data (deck?)
- Finally, it would be nice to snapshot sync data in s3 so that I can recover lost state.


- alternatively: someone wrote an anki sync server (BUT: seems to be python2): https://github.com/dsnopek/anki-sync-server
  - Someone forked it and upgraded to python3: issues seem more active - https://github.com/tsudoko/anki-sync-server/tree/anki_2_1

#### Anki Docker Container

here: https://hub.docker.com/r/txgio/anki/

need to use a linux machine, not clear if fargate will work or if i need some other method...


1. spin up docker container in aws
2. sync collection down from ankiweb
3. add card/whatever info
4. sync collection up to ankiweb
5. spin container down in aws

https://hub.docker.com/r/txgio/anki/

### Anki Collections, Notes (decks, card templates, cards)

#### Unknowns

- Where is card-specific memorization data stored and is it accessed across N decks that all have "some of the same cards"?

#### From The Manual

> Anyone who needs to remember things in their daily life can benefit from Anki. Since it is content-agnostic and supports images, audio, videos and scientific markup (via LaTeX)...

> Your collection is all the material stored in Anki – your cards, notes, decks, note types, deck options, and so on. Notes and note types are common to your whole collection rather than limited to an individual deck. 

> Decks can contain other decks, which allows you to organize decks into a tree. Anki uses “::” to show different levels. A deck called “Chinese::Hanzi” refers to a “Hanzi” deck, which is part of a “Chinese” deck. If you select “Hanzi” then only the Hanzi cards will be shown; if you select “Chinese” then all Chinese cards, including Hanzi cards, will be shown.  To place decks into a tree, you can either name them with “::” between each level, or drag and drop them from the deck list. Decks that have been nested under another deck (that is, that have at least one “::” in their names) are often called subdecks, and top-level decks are sometimes called superdecks or parent decks.

Anki has an abstraction for making cards out of question+answer+info called `notes`.

> In order for Anki to create cards based on our notes, we need to give it a blueprint that says which fields should be displayed on the front or back of each card. This blueprint is called a card type. Each type of note can have one or more card types; when you add a note, Anki will create one card for each card type.  Each card type has two templates, one for the question and one for the answer. In the above French example, we wanted the recognition card to look like this:

> Anki allows you to create different types of notes for different material. Each type of note has its own set of fields and card types. It’s a good idea to create a separate note type for each broad topic you’re studying. 

## MVP

Given a `Vocab Item`, `Vocab Type`, and `Language Usage Source`.

Generate an anki flash card for the `Vocab Item`

### MVP Workflow

#### CREATE

- create anki card probably in dynamodb
  - how easy to update and version dynamodb record? how much upfront architecture planning on the document (usually none...)
- Go to web page, paste into a multiline text box.
- Response is a preview of the anki card information with a submit button
- Ability to add tags for the card
- Submit action triggers:
  1. anki card saved in database as some string format or something
  2. anki card deployed to any tagged decks
    - avoid losing any existing memorization history
  3. store raw in database: `cleaned_words`, `response_text`, and `translations`, anki card, tags
    - unique on exact `cleaned_words` would be great, also need an id probably for futureproofing
    - don't want to be too unique so we can support phrases and sentences later with gcp google translate api
  4. forward to `read` page for object

#### READ

- index page with cards in order added
- ability to filter by 
  - list of substring tokens
  - tags - one or multiple, e.g. `lang-nl` and `loanwords`
- unique url per card, details specified elsewhere
  - probably something like `/cards/<id>`


#### UPDATE

- anki card ideally versioned, maybe using json diffs or a dynamodb document version history, blah
- would be pretty useful when adding features...
- regenerate anki card, replace old card without losing memorization data
- probably not MVP
- *major* difference in ANKI: we want to keep the anki card memorization data
- since we are generating everything from `cleaned_words`, this process is closer like DELETE+CREATE on the db side


#### DELETE

- probably not MVP
- need to remove the anki card from any decks, will lose any associated memorization data...
- drop the database record


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

## Similar Works

- [anki card maker](https://www.reddit.com/r/Anki/comments/61rxks/ankimaker_automatically_generate_anki_decks/)
