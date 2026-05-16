# anki-german

I put a lot of time into this back in 2022, when I was taking German and Russian classes.

At the time, there was no frequency-ranked list of German words available on the internet. The closest thing to it was a corpus released by Leipzig University. They had ranked the 1-million most frequently used words on websites hosted in Germany, but the problem was that a huge portion of these words weren't actually German. So I came up with this nightmare spaghetti:

I wrote a Python script to search each word on the Langenscheidt web dictionary, to figure out if it was actually German or not. I used Langenscheidt because that particular site behaved such that I could determine whether the word was German just by observing the HTTP redirect. That sped up the process a lot, because I didn't even have to download the HTML for this step.

But I did have to request, cache, and parse HTML to create the flashcards themselves. I wrote another script to search the Linguee web dictionary for the words I had determined to be German, and then parse the translation, part of speech, etc. from the response.

It turned out to be a very network-intensive problem to figure out which nouns were unique plural forms, and what their singular form was. It was impossible to get this information in a single HTTP request from any of the websites I tried. I used Linguee in particular because their content formatting made it possible to reliably solve this problem, but it required a huge number of HTTP requests.

This project turned out to be a huge time sink, so I stopped working on it, but it taught me a lot about web scraping.
