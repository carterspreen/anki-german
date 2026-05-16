import time
import requests_cache
from bs4 import BeautifulSoup, SoupStrainer

#corpus download link
#https://wortschatz.uni-leipzig.de/en/download/German

def get_words_from_corpus(num_of_words = None):
    corpus_file = open('1m-words.txt', 'r')
    corpus_lines = [line.split() for line in corpus_file]
    corpus_file.close()

    word_set = set()
    word_list = []

    limited = type(num_of_words) == int

    for line in corpus_lines:
        if limited and len(word_list) == num_of_words:
            break
        elif len(line) == 3 and line[1].isalpha():
            word = line[1].lower()
            if word not in word_set:
                word_list.append(word)
                word_set.add(word)

    print(len(word_list))
    return word_list

def search_linguee(wordlist = []):

    def get_linguee_response(word, cache, delay=0): #get linguee http response  for a given word and rate limit requests
        linguee_url = 'https://www.linguee.com/english-german/search?source=german&query=' #linguee base url
        search_url = linguee_url + word #linguee search query

        response = cache.get(search_url) #get http response from url
        if not response.from_cache: #time delay to avoid ip banning
            time.sleep(delay)

        print(search_url) #scaffolding
        return response
    
    def get_dictionary_entries(response): #get dictionary tag from http response content
        dictionary_strainer = SoupStrainer('div', id='dictionary') #parse only the element with id 'dictionary'
        soup = BeautifulSoup(response.content, 'lxml', parse_only=dictionary_strainer) #parse html content
        dictionary = soup.find('div', attrs={'data-source-lang': 'DE'}).find('div', class_='exact') #find the element containing exact translations 

        if dictionary: #if translations found
            dictionary_entries = dictionary.find_all('div', class_='lemma', recursive=False) #find all the lemmas
            return dictionary_entries

#    def get_translations(translation_body):
#        result_translations = []
#        translations_tags = translation_body.find_all('div', class_='translation', recursive=False)
#        tag_trans = []
#        for translation_tag in translations_tags:
#            tag_trans.append(translation_tag.find('span', class_='tag_trans'))
#        for tag in tag_trans:
#            translation = tag.find('a', class_='dictLink').string
#            result_translations.append(translation)
#        return result_translations

    def get_translations(translation_body):
        translations = []
        translations_tags = translation_body.find_all('div', class_='translation', recursive=False)
        if translations_tags:
            dictlinks = [tag.find('a', class_='dictLink') for tag in translations_tags]
            for link in dictlinks:
                translations.append(' '.join([tag.string for tag in link.find_all(string=True)]))
            print(translations)
            return translations

    #def get_uncommon_translations(translation_body):
    #    extra_translations = translation_body.find('div', class_='translation_group')
    #    if extra_translations:
    #        result_extra_translations = []
    #        extra_tag_trans = extra_translations.find_all('span', class_='tag_trans')
    #        for tag in extra_tag_trans:
    #            extra_translation = tag.find('a', class_='dictLink').string
    #            result_extra_translations.append(extra_translation)
    #        return result_extra_translations
    
    def get_uncommon_translations(translation_body):
        translation_groups = translation_body.find_all('div', class_='translation_group') #possibly change this to find instead of find all
        if len(translation_groups) > 1: #scaffolding, possibly remove this
            raise Exception
        if translation_groups:
            uncommon_translations = []
            dictlinks = translation_groups[0].find_all('a', class_='dictLink') #will have to change this if changing to find instead of find all
            for link in dictlinks:
                uncommon_translations.append(' '.join([tag.string for tag in link.find_all(string=True)]))
            print(uncommon_translations)
            return uncommon_translations


        

#    def get_other_forms(translation_header):
#                tag_forms = translation_header.find_next_sibling('span', class_='tag_forms')
#
#                inflection_info = translation_header.find()
#                if tag_forms:
#                    other_forms = tag_forms.find_all('a', class_='formLink')
#                    result_forms = [other_form.string for other_form in other_forms]
#                    return result_forms

    def get_other_forms(dictionary_entry):
        translation_header = dictionary_entry.find('span', class_='tag_lemma') #needed for get_word_id, get_wordtype, and get_other_forms
        tag_forms = translation_header.find_next_sibling('span', class_='tag_forms')
        form_strings = []

        inflection_info = dictionary_entry.find('div', class_='inflectioninfo')
        if inflection_info:
            form_strings.append(' '.join([ tag.string for tag in inflection_info.find_all(string=True)]))

        if tag_forms:
            other_forms = ' '.join([ tag.string for tag in tag_forms.find_all(string=True) ])
            form_strings.append(other_forms)
        return form_strings
    
    def get_wordtype(translation_header):
        wordtype_tag = translation_header.find('span', class_='tag_wordtype')
        if wordtype_tag:
            wordtype_string = wordtype_tag.string.replace('\xa0', ' ')
            return wordtype_string
    
    def get_word_title(translation_header):
        lemma_title = translation_header.find('a', class_='dictLink').find_all(string=True)
        title_list = []
        for tag in lemma_title:
            title_list.append(tag.string)

        word_title = ' '.join(title_list)

        print(word_title)
        return word_title

    def word_factory(word_id, other_forms, translations, uncommon_translations):
        word_result = {}

        if word_id:
            word_result['word_id'] = word_id
        if other_forms:
            word_result['other_forms'] = other_forms
        if translations:
            word_result['translations'] = translations
        if uncommon_translations:
            word_result['uncommon_translations'] = uncommon_translations

        return word_result

    cache = requests_cache.CachedSession('linguee-cache') #persistent http cache
    results_dict = dict() #used to store dictionary entries

    for word in wordlist:

        try:
            dictionary_entries = get_dictionary_entries(get_linguee_response(word, cache, delay=1))
        except:
            print('You were IP banned :(')
            break

        if dictionary_entries:

            for entry in dictionary_entries:

                translation_header = entry.find('span', class_='tag_lemma') #needed for get_word_id, get_wordtype, and get_other_forms
                translation_body = entry.find('div', class_='translation_lines') #needed for get_translations and get_uncommon_translations

                word_title = get_word_title(translation_header)
                wordtype = get_wordtype(translation_header)

                if wordtype:
                    result_id = word_title + ' (' + wordtype + ')'
                else:
                    print(word_title + ' has no wordtype')
                    continue #throw out words without part of speech information

                result = word_factory(word_id = result_id,
                                      other_forms = get_other_forms(entry),
                                      translations = get_translations(translation_body),
                                      uncommon_translations = get_uncommon_translations(translation_body))

                if result_id not in results_dict:
                    results_dict[result_id] = result

    cache.close()
    return results_dict

def write_linguee_data(filename, linguee_dict=None):
    outfile = open(filename + '.txt', 'w')
    for result_id in linguee_dict:
        word = linguee_dict[result_id]
        other_forms = None
        uncommon_translations = None
        translations = None
        if 'other_forms' in word:
            other_forms = word['other_forms']
        if 'uncommon_translations' in word:
            uncommon_translations = word['uncommon_translations']
        if 'translations' in word:
            translations = word['translations']

        string = result_id 
        if translations:
            string += ' ' + str(translations) 
        if uncommon_translations:
            string += ' ' + str(uncommon_translations) 
        if other_forms:
            string += ' ' + str(other_forms)
        string += '\n'
        outfile.write(string)
    outfile.close()

write_linguee_data('linguee-test', search_linguee(get_words_from_corpus(1000)))
#write_linguee_data('linguee-test2', search_linguee(['Orte']))