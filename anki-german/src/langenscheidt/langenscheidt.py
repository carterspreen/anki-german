from bs4 import BeautifulSoup, SoupStrainer
import requests_cache
#import re #python regex
import time

def localclean(output_filename):
    corpus = open('1m-words.txt', 'r') #open the corpus
    unfiltered_lines = corpus.readlines() #read lines into a list
    corpus.close() #close the corpus

    lines = [line.split() for line in unfiltered_lines] # split the lines into lists
    # find all the lines containing only one word (multiword lines have len == 3)
    #and words used at least 10 times in 1 million sentences
    words = [line[1] for line in lines if len(line) == 3 and int(line[-1]) >= 10] 
    alphabetic_words = [word + '\n' for word in words if word.isalpha()] # find all the words containing only alphabetic characters

    cleancorpus = open(output_filename, 'w')
    cleancorpus.writelines(alphabetic_words)
    cleancorpus.close()


def webclean(output_filename):
    #store urls needed for web searching
    netzverb_url = 'https://www.verbformen.com/?w='
    langenscheidt_url = 'https://en.langenscheidt.com/german-english/'

    #read pre-cleaned words from file
    infile = open('localcleaned-words.txt', 'r')
    words = []
    for line in infile:
        words.append(line.strip())
    infile.close()

    #open a html requests cache
    session = requests_cache.CachedSession('langenscheidt-cache')

    #parse only what we need
    netzverb_strainer = SoupStrainer('article') 

    rank = 1 #used to count the frequency ranking
    accepted_words = [] #used to store the accepted words
    failed_words = []

    for word in words:
        #if len(accepted_words) >= 10000:
        #    break
        print('searching langenscheidt for ' + word)
        langenscheidt_search_url = langenscheidt_url + word
        langenscheidt_response = session.get(langenscheidt_search_url)
        #langen_soup = BeautifulSoup(langenscheidt_response.content, 'lxml')
        if 'search?term=' not in langenscheidt_response.url:
            print('found on Langenscheidt')
            #add current word, rank, url, source to list of accepted words
            accepted_words.append(word + ' ' + str(rank) + ' ' + langenscheidt_response.url + ' langenscheidt\n') 
            print('saved ' + word + ' with rank ' + str(rank))
            rank += 1
        else:
            failed_words.append(word)
            print('not found')
                

    session.close()

    #write cleaned words to file
    of = open('webcleaned-words2.txt', 'w')
    for accepted_word in accepted_words:
        of.write(accepted_word)
    of.close()

    failfile = open('failed-words2.txt', 'w')
    for failed_word in failed_words:
        failfile.write(failed_word + '\n')
    failfile.close()

localclean('localcleaned-words.txt')
webclean('webcleaned-words.txt')