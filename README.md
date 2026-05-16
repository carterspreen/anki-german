# anki-german

Generates flashcards for studying German vocabulary.

I put a lot of time into this back in 2022, when I was taking German and Russian classes. 

At the time, there was no frequency-ranked list of German words available on the internet. The closest thing to it was a corpus released by Leipzig University. They had ranked the 1-million most frequently used words on websites hosted in Germany, but the problem was that a huge portion of these words weren't actually German. So I came up with this nightmare spaghetti:

I wrote a Python script to search each word on the Langenscheidt web dictionary, to figure out if it was actually German or not. I used Langenscheidt because that particular site behaved in such a way that I could determine whether the word was German just by observing whether I got an http redirect to the "german-english" dictionary rather than some other one. That sped up the process a lot, because I didn't even have to download the HTML. 

Then, I made a list of all the German words, and wrote another script to search them on the Linguee web dictionary, and then parse the translation, part of speech, etc. from the HTML. I can't remember exactly why I used Linguee for this, but it had something to do with figuring out which nouns were unique plural forms, and what their singular form was. This project turned out to be a huge time sink, so I gave up on it. However, it taught me a lot about web scraping. 

Eventually I found dict.cc, which is open source. When I get some time, I may revisit this project using their dataset.
