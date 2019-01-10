import bs4 as bs
import urllib.request
import pandas as pd
import csv
import xml.etree.ElementTree as ET
files = []


def json_generator():
    f = open('movie_list.csv')
    csv_f = csv.reader(f)
    key = '49f91ae0'
    for row in csv_f:
        try:
            title = row[0]
            year = row[1]

            title = title.replace(" ", "+")
            sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                           title + '&y=' + year + '&r=json&apikey=' + key).read()

            soup = bs.BeautifulSoup(sauce, 'lxml')
            print(title, year)
            output = str(soup)
            file_name = title.replace("+", "_")
            f = open('json/' + file_name + '_' + year + '.json', 'w+')
            f.write(output)
            f.close()
            files.append(file_name + "_" + year + '.json')

        except:
            print('oops....')


def parse():

    files = ['Number_One_with_a_Bullet_1987.xml', 'The_Pack_1977.xml', 'Congo_1995.xml', 'Psychomania_1973.xml', 'The_Hand_1981.xml', 'K-9_1989.xml', 'The_Wrong_Guys_1988.xml', 'Dead_Heat_1988.xml', 'Evilspeak_1981.xml', "Gone_Fishin'_1997.xml", 'The_Net_1995.xml', 'Superman_III_1983.xml', 'Superman_IV_1987.xml', 'Boys_and_Girls_2000.xml', 'Fuzz_1972.xml', 'Deep_Impact_1998.xml', 'Captain_America_1990.xml', 'Deadlock_1970.xml']

    for i in files:
        tree = ET.parse('xml/' + i)

        root = tree.getroot()
        #print(root)
        movie_data = open('movies.csv', 'w')

        csvwriter = csv.writer(movie_data)

        for movie in root.findall('movie'):
            year = movie.find('movie')
            print(year)


        #print('hi!')


def main():
    json_generator()
    #parse()
    # print(files)


main()





