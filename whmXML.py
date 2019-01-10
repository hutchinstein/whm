import bs4 as bs
import urllib.request
import csv
import xml.etree.ElementTree as ET
files = []
episode_num_list = []


def xml_generator():
    f = open('movie_list.csv')
    csv_f = csv.reader(f)
    key = '49f91ae0'
    for row in csv_f:
        try:
            title = row[0]
            year = row[1]
            #episode_num = row[2]

            title = title.replace(" ", "+")
            sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                           title + '&y=' + year + '&r=xml&apikey=' + key).read()
            print(title, year)
            soup = bs.BeautifulSoup(sauce, 'xml')

            output = str(soup)

            file_name = title.replace("+", "_")
            f = open('xml/' + file_name + '_' + year + '.xml', 'w+', encoding='utf-8')
            f.write(output)
            f.close()
            files.append(file_name + "_" + year + '.xml')
            #episode_num_list.append(episode_num)

        except:
            print('oops....')


def parse():

    # files = ['Number_One_with_a_Bullet.xml', 'The_Pack.xml', 'Congo.xml']
    # temp = "Gone_Fishin'_1997.xml",
    for i in files:
        parser = ET.XMLParser(encoding='utf-8')
        tree = ET.parse('xml/' + i, parser=parser)

        root = tree.getroot()
        ep_counter = 0
        for movie in root.findall('movie'):
            ep_num = episode_num_list[ep_counter]
            ep_counter = ep_counter + 1

            current_film = []
            actors = str(movie.get('actors'))

            title = movie.get('title')
            director = movie.get('director')
            genre = movie.get('genre')
            imdbRating = movie.get('imdbRating')
            rated = movie.get('rated')
            runtime = movie.get('runtime')
            released = movie.get('released')
            writers = movie.get('writer')

            ###
            ### Creating a list of actors and writers
            ### When moving data to csv file loop current_film
            ### Then loop the writers and actors
            ### This will allow each individual to have their own cell
            ###

            actor_list = actors.split(',')
            actor_count = len(actor_list)
            # if actor_count > 0:
            #     print(title, 'has', actor_count, 'actors.')
            #current_film.append(actors)

            current_film.append(title)
            current_film.append(director)
            current_film.append(genre)
            current_film.append(imdbRating)
            current_film.append(rated)
            current_film.append(runtime)
            current_film.append(released)
            #current_film.append(writers)
            current_film_list = ['title', 'director', 'genre', 'imdb rating', 'rating', 'run time', 'release date']
            writer_list = writers.split(',')
            writers_count = len(writer_list)
            # if writers_count > 0:
            #     print(title, 'has', writers_count, 'writers.')
            #     print(title, 'writers: ', writer_list)
            j = 0
            for i in current_film:
                print(title, ep_num,current_film_list[j], ':', i)
                j = j + 1



            for i in actor_list:
                print(title, 'actor :', i)

            for i in writer_list:
                print(title, 'writer :', i)
            # print(title + ': ' + actors, director, genre, 'IMDB Rating: ', imdbRating, rated, runtime, released,
            #       'writer(s): ', writers)
            # print(current_film)
            # for row in current_film:
            #     print(row)


def main():
    xml_generator()
    parse()
    #print(files)


main()





