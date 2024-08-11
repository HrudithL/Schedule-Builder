import csv
from scraper.scraper import SchoolScraper
import scraper.constants as const
from autocorrect import Speller


class Writer:
    scraper = None

    def get_data(self):
        headless = input('Headless? ').__contains__('y' or 'Y')
        self.scraper = SchoolScraper(options=(const.HEADLESS() if headless else None), debug=False)
        self.scraper.run()

    def write(self):
        with open(const.FILE_NAME, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=const.FIELDNAMES)
            writer.writeheader()

            spell_check = Speller(lang='en')
            # run through every course
            for course_index in range(self.scraper.course_count()):
                course_data = {}
                # run through all types of data for that course
                for fieldname in const.FIELDNAMES:
                    # iterate over list and get each value and set it to a dictionary value
                    val = self.scraper.get_value(fieldname)[course_index]
                    if fieldname != ('schools' and 'tag' and 'id' and 'name'):
                        spell_check(val)
                    course_data[fieldname] = val
                # Write the dictionary
                writer.writerow(course_data)
