import bs4 as bs
import urllib.request
import pandas as pd
import csv
import xml.etree.ElementTree as ET
files = []


def xml_generator():
    f = open('movie_list.csv')
    csv_f = csv.reader(f)
    key = '49f91ae0'
    for row in csv_f:
        try:
            title = row[0]
            year = row[1]
            print(title, year)
            title = title.replace(" ", "+")
            sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                           title + '&y=' + year + '&r=xml&apikey=' + key).read()
            soup = bs.BeautifulSoup(sauce, 'xml')
            output = str(soup)
            file_name = title.replace("+", "_")
            f = open('xml/' + file_name + '_' + year + '.xml', 'w+')
            f.write(output)
            f.close()
            files.append(file_name + "_" + year + '.xml')

        except:
            print('oops....')


def parse():
    for i in files:
        tree = ET.parse('xml/' + i)
        root = tree.getroot()

        movie_data = open('movies.csv', 'w')

        csvwriter = csv.writer(movie_data)

        movie_head = []

        for movie in root.findall('movie'):
            year = movie.find('year')
            print(year)

        print('hi!')
def main():
    xml_generator()
    parse()
    print(files)


main()





