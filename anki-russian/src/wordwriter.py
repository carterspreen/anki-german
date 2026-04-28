class WordWriter:
    def __init__(self, filename, wordlist):
        self.filename = filename
        self.wordlist = wordlist

    def write(self):
        file = open(self.filename, 'w')
        file.write('#separator:Tab\n#tags column:16\n')
        for word in self.wordlist:
            file.write(str(word))
        file.close()