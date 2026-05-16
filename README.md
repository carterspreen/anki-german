# anki-german

Anki flashcard generator for German vocabulary.

I put a lot of time into this back in 2022, when I was taking German classes. 

Unfortunately there was no good open-source German dictionary to source data from, so I came up with this nightmare spaghetti:

I got a free corpus from Leipzig University, that had ranked the 1-million most frequently used words on the German web. However, it contained a lot of non-German words. So I wrote a Python script to search each word on the Langenscheidt web dictionary, to figure out if it was actually German or not. I used Langenscheidt because the site behaved in such a way that I could determine whether the word was German just by observing whether I got an http redirect to the "german-english" dictionary rather than some other one. I didn't have to do any HTML parsing. Then, I made a list of all the German words, and wrote another script to search them on the Linguee web dictionary and parse the translation and part of speech from the HTML. I can't remember exactly why I used Linguee for this, but it had something to do with figuring out which nouns were unique plural forms, and what their singular form was. This project turned out to be a huge time sink, so I gave up on it. However, it taught me a lot about web scraping.
