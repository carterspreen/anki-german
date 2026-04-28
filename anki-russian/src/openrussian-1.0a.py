from openrussianscraper import OpenRussianScraper

def interactive_scrape():
    print("\nWelcome to Carter's OpenRussian.org Flashcard Generator!\n")
    filename = input("Enter output filename: ")
    start_rank = input("Enter starting word's frequency: ")
    end_rank = input("Enter ending word's frequency: ")
    store_untranslated = True if input("Store untranslated words? Y/n: ") == 'Y' else False
    print(store_untranslated)
    print()
    try:
        start_rank = int(start_rank)
        end_rank = int(end_rank)
    except:
        print('Error: frequencies must be integers')
    else:
        scraper = OpenRussianScraper(filename, start_rank, end_rank, store_untranslated)
        scraper.write()
        print("All anki notes successfully written to: " + filename)
    finally:
        print("Exiting...\n")
    
def automatic_scrape():
    directory = 'outputs/'
    for start_index in range(1, 5000, 100):
        end_index = start_index + 99 
        filename = str(start_index) + '-' + str(end_index) + '.txt'
        file_path = directory + filename
        scraper = OpenRussianScraper(file_path, start_index, end_index)
        scraper.write()

automatic_scrape()