import requests_cache
from bs4 import BeautifulSoup as bs

from word import Word
from wordwriter import WordWriter
from counter import Counter

class OpenRussianScraper:

    def __init__(self, filename, start_rank=1, end_rank=None, store_untranslated=False):
        self.filename = filename
        self.start_rank = start_rank
        self.end_rank = end_rank
        self.store_untranslated = store_untranslated
        self.wordlist = iterate_get_words(self.start_rank, self.end_rank, self.store_untranslated)
        self.writer = WordWriter(self.filename, self.wordlist)

    def write(self):
        self.writer.write()

#return a list of Word objects, ranked by frequency 
def get_words(cached_session, starting_rank=1, store_untranslated=False, fail_counter=None):

    #make a list of words
    saved_words = []

    #openrussian database urls
    url = 'https://en.openrussian.org'
    list_ext = '/list/all'
    paging_ext = '?start='
    start_ext = str(starting_rank - 1)

    #open a requests cache
    #get initial response from url or cache
    response = cached_session.get(url + list_ext + paging_ext + start_ext)

    #parse response content with beautifulsoup
    soup = bs(response.content, 'html.parser')

    #find the table with class="wordlist"
    wordlist = soup.find(name='table', class_='wordlist')
    #get the body of the table (we don't want the header)
    wordlist_body = wordlist.tbody
    #get all the data from each table row
    for row in wordlist_body.find_all(name='tr'):
        #get the tag containing the word ranking
        rank_tag = row.find(class_='rank')
        word_rank = rank_tag.string
        #get the tag containing the word and its url
        name_url_tag = row.find(href=True)
        if name_url_tag:
            word_name = name_url_tag.string
            word_url = url + name_url_tag['href']
            translated = True
        else:
            name_tag = row.find(class_='ru no-link')
            word_name = name_tag.string
            word_url = ''
            translated = False
            if type(fail_counter) == Counter: fail_counter.count_one()
        #get all the english translations for the word
        translation_tags = row.find_all(class_='tl')
        word_translations = [tag.get_text().strip() for tag in translation_tags]
        #save this word as a word object
        if store_untranslated or translated:
            saved_words.append(Word(rank=word_rank, word=word_name, url=word_url, translations=word_translations))

    return saved_words

def iterate_get_words(starting_rank=1, ending_rank=None, store_untranslated=False):
    cached_session = requests_cache.CachedSession('openrussian_cache')
    saved_words = []

    if ending_rank:
        expected_len = int(ending_rank) - (int(starting_rank) - 1)
    else:
        expected_len = 'Unknown'
    
    print('Number of cards to generate: ' + str(expected_len))
        
    fail_counter = Counter()
    while not ending_rank or len(saved_words) < expected_len:
        print('Progress: ' + str(len(saved_words)) + '/' + str(expected_len))
        current_start = int(starting_rank) + len(saved_words) + fail_counter.get_count()
        fail_counter.clear()
        new_words = get_words(cached_session, current_start, store_untranslated, fail_counter)
        expected_len -= fail_counter.get_count()
        if new_words:
            saved_words.extend(new_words)
        else: break

    if expected_len != 'Unknown' and len(saved_words) > expected_len:
        saved_words = saved_words[:expected_len]

    print('Progress: ' + str(len(saved_words)) + '/' + str(expected_len))
    
    cached_session.close()
    return saved_words