# Vocab Manager

A vocabulary manager that hooks into Anki flashcards and web resources.

Web resources automatically generate card definitions.


## MVP


If we use a store of web resources and how to query them


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
