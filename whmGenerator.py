import bs4 as bs
import urllib.request
import csv
import xml.etree.ElementTree as ET
files = []
blank_file_names = []
episode_num_list = []
## another git test
###
###
###
### 1-5
### Need to remove word 'episode' to allow sorting --- this is done
### Remove word min from runtime
### Need to remove commas from titles --- this is done
### Allow multiple directors
### Something is off with the writers, they seem to be adding in blank spaces and people added to the end
### of a movie they don't belong to
### Add in description
###
###
###

def xml_generator():
    f = open('movie_year.csv')
    csv_f = csv.reader(f)
    key = '49f91ae0'

    for row in csv_f:
        try:
            title = row[0]
            year = row[1]
            episode_num = row[2]
            title = title.replace(" ", "_")


            if year == '':
                sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                               title + '&r=xml&apikey=' + key).read()
            else:
                sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                               title + '&y=' + year + '&r=xml&apikey=' + key).read()
            print(title)
            soup = bs.BeautifulSoup(sauce, 'xml')

            output = str(soup)

            if output == '':
                print(title, 'has an empty file')
                blank_file_names.append(title)


            #print(output)
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
    # files = ['Number_One_with_a_Bullet.xml', 'The_Pack.xml', 'Congo.xml', 'Psychomania.xml', 'The_Hand.xml', 'K-9.xml',
    # 'The_Wrong_Guys.xml', 'Dead_Heat.xml', 'Evilspeak.xml', "Gone_Fishin'.xml", 'The_Net.xml',
    # 'Superman_III_&_IV_Part_One.xml']
    ep_counter = 0
    for i in files:
        ep_num = episode_num_list[ep_counter]
        ep_counter = ep_counter + 1

    # temp = "Gone_Fishin'_1997.xml",
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
            ## Trim 'min' from end of string and blank space
            released = movie.get('released')
            writers = movie.get('writer')

            actor_list = actors.split(',')
            genre_list = genre.split(',')
            # director_list = director.split(',')
            # append title to the final list
            current_film.append(title)
            # create list for directos, then loop through.  Remove 3rd director if there is one?
            current_film.append(director)
            #current_film.append(genre)
            current_film.append(imdbRating)
            current_film.append(rated)
            current_film.append(runtime)
            current_film.append(released)
            current_film_list = ['title', 'director', 'imdb rating', 'rating', 'run time', 'release date']
            writer_list = writers.split(',')
            print(len(genre_list))
            if len(genre_list) < 6:
                for i in range(0, (6-len(genre_list))):
                    genre_list.append('')
            #add logic to handle two directors
            j = 0
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
            final_list = final_list + '\n'
            print('final list', final_list)
            f = open('movies_out.csv', 'a')
            f.write(final_list)

            # print(title + ': ' + actors, director, genre, 'IMDB Rating: ', imdbRating, rated, runtime, released,
            #       'writer(s): ', writers)
            # print(current_film)
            # for row in current_film:
            #     print(row)


def main():
    xml_generator()
    parse()


main()





