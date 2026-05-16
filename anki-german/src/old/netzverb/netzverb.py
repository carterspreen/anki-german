
#check if netzverb has it
def search_netzverb():
    print('searching netzverb for ' + word)
    netzverb_search_url = netzverb_url + word #url to search for word on verbformen.com
    netzverb_response = session.get(netzverb_search_url) #get an html response
    netzverb_soup = BeautifulSoup(netzverb_response.content, 'lxml', parse_only=netzverb_strainer) #parse
    netzverb_found = netzverb_soup.find(class_='rAbschnitt') #find successful searches
    return netzverb_found
#if search_netzverb(): #if successful search
#    print('found ' + word + ' on netzverb!')
#    accepted_words.append(word + ' ' + str(rank) + ' ' + netzverb_response.url + ' netzverb\n') #add current word and rank to list of accepted words
#    print('saved ' + word + ' with rank ' + str(rank))
#    rank += 1
#else:
#    print(word + ' not found on netzverb')
#    print('searching langenscheidt for ' + word)
#    langenscheidt_search_url = langenscheidt_url + word
#    langenscheidt_response = session.get(langenscheidt_search_url)
#    #langen_soup = BeautifulSoup(langenscheidt_response.content, 'lxml')
#    if 'search?term=' not in langenscheidt_response.url:
#        print('found on Langenscheidt')
#        accepted_words.append(word + ' ' + str(rank) + ' ' + langenscheidt_response.url + ' langenscheidt\n') #add current word and rank to list of accepted words
#        print('saved ' + word + ' with rank ' + str(rank))
#        rank += 1
#    else:
#        print('not found at all :(((')