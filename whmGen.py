import bs4 as bs
import urllib.request
import csv
import xml.etree.ElementTree as ET
files = []
blank_file_names = []
episode_num_list = []


def xml_generator():
    f = open('movie_year.csv')
    csv_f = csv.reader(f)
    key = '49f91ae0'

    for row in csv_f:
        try:
            title = row[0]
            year = row[1]
            episode_num = row[2]
            title = title.replace(" ", "+")

            if year == '':
                sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                               title + '&plot=full&r=xml&apikey=' + key).read()
            else:
                sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                               title + '&y=' + year + '&plot=full&r=xml&apikey=' + key).read()
            print(title)
            soup = bs.BeautifulSoup(sauce, 'xml')

            output = str(soup)

            if output == '':
                print(title, 'has an empty file')
                blank_file_names.append(title)

            title = title.replace(":", " ")
            title = title.replace(',', '-')
            file_name = title.replace("+", "_")
            f = open('xml/' + file_name + '.xml', 'w+', encoding='utf-8')
            f.write(output)
            f.close()
            files.append(file_name + '.xml')
            episode_num_list.append(episode_num)


        except:
            print('Error')
    print(blank_file_names)
    print(files)


def parse():
    # files = ['Number_One_with_a_Bullet.xml', 'The_Pack.xml', 'Congo.xml', 'Psychomania.xml', 'The_Hand.xml', 'K-9.xml']

    ep_counter = 0
    for i in files:
        ep_num = episode_num_list[ep_counter]
        ep_counter = ep_counter + 1

        parser = ET.XMLParser(encoding='utf-8')
        tree = ET.parse('xml/' + i, parser=parser)

        root = tree.getroot()

        for movie in root.findall('movie'):

            current_film = []
            final_list = ''
            actors = str(movie.get('actors'))

            title = movie.get('title')
            title = title.replace(',', ' ')
            director = movie.get('director')
            genre = movie.get('genre')
            imdbRating = movie.get('imdbRating')
            rated = movie.get('rated')
            runtime = movie.get('runtime')
            runtime = runtime[:3]
            released = movie.get('released')
            writers = movie.get('writer')
            plot = movie.get('plot')
            plot = plot.replace(',', '')
            poster = movie.get('poster')
            imdbID = movie.get('imdbID')
            awards = movie.get('awards')
            metascore = movie.get('metascore')
            actor_list = actors.split(',')
            genre_list = genre.split(',')
            director_list = director.split(',')
            current_film.append(imdbRating)
            current_film.append(rated)
            current_film.append(runtime)
            current_film.append(released)
            final_list = final_list + title
            if len(director_list) > 2:
                del director_list[2:]
            if len(director_list) < 2:
                director_list.append('')
            for i in director_list:
                print(final_list)
                print(title, 'Director(s):', i)
                final_list = final_list + ',' + i
            current_film_list = ['imdb rating', 'rating', 'run time', 'release date']
            writer_list = writers.split(',')
            if len(writer_list) > 4:
                del writer_list[4:]
            if len(writer_list) < 4:
                for i in (range(0, 4-len(writer_list))):
                    writer_list.append('')
            if len(actor_list) > 4:
                del actor_list[4:]
            if len(actor_list) < 4:
                for i in (range(0, 4-len(actor_list))):
                    actor_list.append('')
            print(len(genre_list))
            if len(genre_list) > 4:
                del genre_list[4:]
            if len(genre_list) < 4:
                for i in range(0, (4-len(genre_list))):
                    genre_list.append('')
            j = 0
            ep_num = ep_num[-3:]
            final_list = final_list + ',' + ep_num
            for i in current_film:
                print(title, ep_num, current_film_list[j], ':', i)
                j = j + 1
                final_list = final_list + ',' + i

            for i in genre_list:
                print(title, 'genre:', i)
                final_list = final_list + ',' + i

            for i in actor_list:
                print(title, 'actor:', i)
                final_list = final_list + ',' + i

            for i in writer_list:
                print(title, 'writer:', i)
                final_list = final_list + ',' + i
            final_list = final_list + ',' + plot + ',' + poster + ',' + imdbID + ',' + awards + ',' + metascore
            final_list = final_list + '\n'
            print('final list', final_list)
            f = open('movies_out.csv', 'a')
            f.write(final_list)


def main():
    xml_generator()
    parse()


main()



